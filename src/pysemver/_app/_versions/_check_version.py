# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

from __future__ import annotations

from typing import Optional, Sequence, Set, TypeVar

import deal
import typic

from ._bar import Bar
from ._bumper import Bumper
from ._config import config
from ._parser import Parser
from ._types import HasIndex, What
from .domain import Exit, Signature
from .services.signatures import CheckSignature

T = TypeVar("T", bound = "CheckVersion")

PARSER = Parser(this = "HEAD")

IGNORE = config.ignore


@typic.klass(always = True, slots = True, strict = True)
class CheckVersion:
    """Checks if the current version is acceptable.

    Attributes:
        bar: A progress bar.
        exit: An exit code.
        parser: A file parser.
        bumper: A version bumper.

    .. versionadded:: 36.1.0

    """

    bar: Bar
    exit: HasIndex
    parser: Parser
    bumper: Bumper

    # @typic.al(strict = True)
    def __init__(self, bar: Bar, parser: Parser = PARSER) -> None:
        self.bar = bar
        self.exit = Exit.OK
        self.parser = parser
        self.bumper = Bumper()

    @deal.pure
    def __call__(self) -> None:
        """Runs all the checks."""

        this: Set[Signature] = set(self._parse(self.parser, "this"))
        that: Set[Signature] = set(self._parse(self.parser, "that"))
        diff: Set[str] = set(self.parser.diff)

        (
            self
            ._check_files(self.bumper, diff)
            ._check_funcs(self.bumper, 2, this, that)
            ._check_funcs(self.bumper, 3, that, this)
            ._check_version_acceptable(self.bumper)
            .bar.then()
            )

    @deal.pure
    # @typic.al(strict = True)
    def _parse(self, parser: Parser, what: What) -> Sequence[Signature]:
        """Updates status while the parser builds signatures."""

        with parser(what = what) as parsing:
            self.bar.info(f"Parsing files from {parser.current}…\n")
            self.bar.init()

            for count, total in parsing:
                self.bar.push(count, total)

            self.bar.wipe()

        return parser.signatures

    @deal.pure
    def _check_files(self: T, bumper: Bumper, files: Set[str]) -> T:
        """Requires a bump if there's a diff in files."""

        what: int = 1
        total: int = len(files)

        self.bar.info("Checking for functional changes…\n")
        self.bar.init()

        for count, file in enumerate(files):
            if not self._is_functional(file):
                continue

            bumper(what)
            self.exit = bumper.required
            self.bar.wipe()
            self.bar.warn(f"{str(bumper.what(what))} {file}\n")
            self.bar.push(count, total)

        self.bar.wipe()

        return self

    @deal.pure
    def _check_funcs(
            self: T,
            bumper: Bumper,
            what: str,
            *files: Set[Signature],
            ) -> T:
        """Requires a bump if there's a diff in functions."""

        # We first do a ``hash`` comparison, so it is still grosso modo.
        diff: Set[Signature] = files[0] ^ files[1] & files[0]
        total: int = len(diff)

        self.bar.info(f"Checking for {what} functions…\n")
        self.bar.init()

        for count, this in enumerate(diff):
            name: str
            that: Optional[Signature]
            checker: FuncChecker

            self.bar.push(count, total)

            # If it is not a functional change, we move on.
            if this is None or not self._is_functional(this.file):
                continue

            # We know we will fail already, but we still need to determine
            # the needed version bump.
            self.exit = bumper.required

            # We will try to find a match between before/after signatures.
            name = this.name
            that = next((that for that in files[1] if that.name == name), None)

            # If we can't find a base signature with the same name, we can just
            # assume the function was added/removed, so minor/major.
            if that is None:
                bumper(what)
                self.bar.wipe()
                self.bar.warn(f"{str(bumper.what(what))} {name} => {what}\n")
                self.exit = bumper.required
                continue

            # Now we do a ``small-print`` comparison between signatures.
            f = FuncChecker(this, that)

            if f.score() == bumper.what(what).value:
                bumper(what)
                self.bar.wipe()
                self.bar.warn(f"{str(bumper.what(what))} {name}: {f.reason}\n")
                self.exit = bumper.required
                continue

        self.bar.wipe()

        return self

    @deal.pure
    def _check_version_acceptable(self: T, bumper: Bumper) -> T:
        """Requires a bump if there current version is not acceptable."""

        self.bar.info(f"Version bump required: {bumper.required.name}!\n")
        self.bar.okay(f"Current version: {bumper.this}")

        if bumper.is_acceptable():
            self.exit = Exit.OK
            return self

        self.bar.fail()

        return self

    @deal.pure
    # @typic.al(strict = True)
    def _is_functional(self, file: str) -> bool:
        """Checks if a given ``file`` is whitelisted as functional."""

        return not any(exclude in file for exclude in IGNORE)
