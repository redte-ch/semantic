# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from types import ModuleType
from typing import Optional, Sequence, Set, TypeVar

import deal
import typic

from .. import infra
from ..domain import Exit, Signature
from ..types import What
from ._bump_version import Bumper
from ._check_signature import CheckSignature
from ._parse_files import ParseFiles

T = TypeVar("T", bound = "CheckVersion")

PARSER = ParseFiles(this = "HEAD")


# @typic.klass(always = True, slots = True, strict = True)
class CheckVersion:
    """Checks if the current version is acceptable.

    Attributes:
        bar: A progress bar.
        exit: An exit code.
        parser: A file parser.
        bump_version: A version bump_version.

    .. versionadded:: 36.1.0

    """

    logs: ModuleType
    exit: Exit
    parser: ParseFiles
    ignore: Sequence[str]
    bump_version: Bumper

    # @typic.al(strict = True)
    def __init__(
            self,
            logs: ModuleType,
            ignore: Sequence[str],
            parser: ParseFiles = PARSER) -> None:
        self.logs = logs
        self.ignore = ignore
        self.exit = Exit.OK
        self.parser = parser
        self.bump_version = Bumper()

    # @deal.pure
    def __call__(self) -> None:
        """Runs all the checks."""

        this: Set[Signature] = set(self._parse(self.parser, "this"))
        that: Set[Signature] = set(self._parse(self.parser, "that"))
        diff: Set[str] = set(self.parser.diff)

        (
            self
            ._check_files(self.bump_version, diff)
            ._check_funcs(self.bump_version, 2, this, that)
            ._check_funcs(self.bump_version, 3, that, this)
            ._check_version_acceptable(self.bump_version)
            .logs.then()
            )

    # @deal.pure
    # @typic.al(strict = True)
    def _parse(self, parser: ParseFiles, what: What) -> Sequence[Signature]:
        """Updates status while the parser builds signatures."""

        with parser(what = what) as parsing:
            self.logs.info(f"Parsing files from {parser.current}…\n")
            self.logs.init()

            for count, total in parsing:
                self.logs.push(count, total)

            self.logs.wipe()

        return parser.signatures

    # @deal.pure
    def _check_files(self: T, bump_version: Bumper, files: Set[str]) -> T:
        """Requires a bump if there's a diff in files."""

        what: int = 1
        total: int = len(files)

        self.logs.info("Checking for functional changes…\n")
        self.logs.init()

        for count, file in enumerate(files):
            if not self._is_functional(file):
                continue

            bump_version(what)
            self.exit = bump_version.required
            self.logs.wipe()
            self.logs.warn(f"{str(bump_version.what(what))} {file}\n")
            self.logs.push(count, total)

        self.logs.wipe()

        return self

    # @deal.pure
    def _check_funcs(
            self: T,
            bump_version: Bumper,
            what: str,
            *files: Set[Signature],
            ) -> T:
        """Requires a bump if there's a diff in functions."""

        # We first do a ``hash`` comparison, so it is still grosso modo.
        diff: Set[Signature] = files[0] ^ files[1] & files[0]
        total: int = len(diff)

        self.logs.info(f"Checking for {what} functions…\n")
        self.logs.init()

        for count, this in enumerate(diff):
            name: str
            that: Optional[Signature]
            checker: FuncChecker

            self.logs.push(count, total)

            # If it is not a functional change, we move on.
            if this is None or not self._is_functional(this.file):
                continue

            # We know we will fail already, but we still need to determine
            # the needed version bump.
            self.exit = bump_version.required

            # We will try to find a match between before/after signatures.
            name = this.name
            that = next((that for that in files[1] if that.name == name), None)

            # If we can't find a base signature with the same name, we can just
            # assume the function was added/removed, so minor/major.
            if that is None:
                bump_version(what)
                self.logs.wipe()
                self.logs.warn(
                    f"{str(bump_version.what(what))} {name} => {what}\n")
                self.exit = bump_version.required
                continue

            # Now we do a ``small-print`` comparison between signatures.
            f = FuncChecker(this, that)

            if f.score() == bump_version.what(what).value:
                bump_version(what)
                self.logs.wipe()
                self.logs.warn(
                    f"{str(bump_version.what(what))} {name}: {f.reason}\n")
                self.exit = bump_version.required
                continue

        self.logs.wipe()

        return self

    # @deal.pure
    def _check_version_acceptable(self: T, bump_version: Bumper) -> T:
        """Requires a bump if there current version is not acceptable."""

        self.logs.info(
            f"Version bump required: {bump_version.required.name}!\n")
        self.logs.okay(f"Current version: {bump_version.this}")

        if bump_version.is_acceptable():
            self.exit = Exit.OK
            return self

        self.logs.fail()

        return self

    # @deal.pure
    # @typic.al(strict = True)
    def _is_functional(self, file: str) -> bool:
        """Checks if a given ``file`` is whitelisted as functional."""

        return not any(exclude in file for exclude in self.ignore)
