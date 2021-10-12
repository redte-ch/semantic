# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from typing import Sequence

import ast
import pathlib
import textwrap

import deal
import typic

from ._bar import Bar
from ._models import Exit
from ._repo import Repo
from ._types import HasIndex

VERSION: str
VERSION = Repo.Version.last()

FILES: Sequence[str]
FILES = Repo.File.tree(VERSION)


@typic.klass(always = True, strict = True)
class CheckDeprecated(ast.NodeVisitor):
    """Prints the list of features marked as deprecated.

    Attributes:
        count:
            The index of the current ``node`` traversal. Defaults to ``0``.
        exit:
            The exit code for the task handler.
        files:
            The list of files to analyse.
        nodes:
            The corresponding :mod:`ast` of each ``file``.
        version:
            The version to use for the expiration check.

    Args:
        files:
            The list of files to analyse. Defaults to the list of ``.py`` files
            tracked by ``git``.
        version:
            The version to use for the expiration check. Defaults to the
            current version of :mod:`.openfisca_core`.

    .. versionadded:: 36.0.0

    """

    bar: Bar
    count: int
    exit: HasIndex
    files: Sequence[str]
    nodes: Sequence[ast.Module]
    total: int
    version: str

    @deal.pure
    # @typic.al(strict = True)
    def __init__(
            self,
            bar: Bar,
            files: Sequence[str] = FILES,
            version: str = VERSION,
            ) -> None:
        self.bar = bar
        self.exit = Exit.OK
        self.files = files
        self.nodes = [self._node(file) for file in self.files]
        self.total = len(self.nodes)
        self.version = version

    @deal.pure
    def __call__(self) -> None:
        self.bar.init()

        # We use ``count`` to link each ``node`` with the corresponding
        # ``file``.
        for count, node in enumerate(self.nodes):
            self.count = count
            self.visit(node)
            self.bar.push(self.count, self.total)

        self.bar.wipe()

    @deal.pure
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Defines the ``visit()`` function to inspect the ``node``.

        Args:
            node: The :mod:`ast` node to inspect.

        Attributes:
            keywords:
                The decorator's keywords, see :mod:`.decorators`.
            file:
                The path of a file containing a module.
            path:
                The resolved ``file`` path.
            module:
                The name of the module.
            lineno:
                The line number of each ``node``.
            since:
                The ``since`` keyword's value.
            expires:
                The ``expires`` keyword's value.
            message:
                The message we will print to the user.

        .. versionadded:: 36.0.0

        """

        keywords: Sequence[str]
        file: str
        path: pathlib.Path
        module: str
        lineno: int
        since: str
        expires: str
        message: Sequence[str]

        # We look for the corresponding ``file``.
        file = self.files[self.count]

        # We find the absolute path of the file.
        path = pathlib.Path(file).resolve()

        # We build the module name with the name of the parent path, a
        # folder, and the name of the file, without the extension.
        module = f"{path.parts[-2]}.{path.stem}"

        # We assume the function is defined just one line after the
        # decorator.
        lineno = node.lineno + 1

        for decorator in node.decorator_list:
            # We cast the ``decorator`` to ``callable``.
            if not isinstance(decorator, ast.Call):
                continue

            # We only print out the deprecated functions.
            if "deprecated" not in ast.dump(decorator):
                continue

            # We cast each keyword to ``str``.
            keywords = [
                kwd.value.s
                for kwd in decorator.keywords
                if isinstance(kwd.value, ast.Str)
                ]

            # Finally we assign each keyword to a variable.
            since, expires = keywords

            message = [
                f"{module}.{node.name}:{lineno} =>",
                f"Deprecated since: {since}.",
                f"Expiration status: {expires}",
                f"(current: {self.version}).",
                ]

            self.bar.warn(f"{' '.join(message)}")

            # If there is at least one expired deprecation, the handler
            # will exit with an error.
            if self._isthis(expires):
                self.exit = Exit.KO
                self.bar.fail()

            self.bar.then()

    @deal.pure
    # @typic.al(strict = True)
    def _isthis(self, version: str) -> bool:
        return self.version == version

    @deal.pure
    # @typic.al(strict = True)
    def _node(self, file: str) -> ast.Module:
        source: str

        with open(file) as f:
            source = textwrap.dedent(f.read())
            return ast.parse(source, file, "exec")
