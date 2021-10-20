# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

"""Signature builder.

.. versionadded:: 1.0.0

"""

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generator,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    )

import ast
import dataclasses
import functools
from pathlib import Path

import deal
import typic

from ..domain import Argument, Signature, Suffix, to_value


def _build_unique_name(
        path: Path,
        node: ast.FunctionDef,
        suffixes: Iterator[Suffix],
        signatures: Tuple[Signature, ...],
        ) -> str:
    """Builds an unique signature name."""

    module: str
    name: str
    decorator: ast.expr

    # We build the module name with the name of the parent path, a
    # folder, and the name of the file, without the extension.
    if len(path.parts) > 1:
        module = f"{path.parts[-2]}.{path.stem}"

    else:
        module = path.stem

    # We compose the name with the name of the module.
    name = f"{module}.{node.name}"

    # We suffix properties, othersise names would duplicate.
    for decorator in node.decorator_list:
        if "property" in ast.dump(decorator):
            name = f"{name}#getter"

        if "setter" in ast.dump(decorator):
            name = f"{name}#setter"

    # Finally we suffix all functions so as to catch the duplicated ones.
    name = f"{name}{next(suffixes).value}"

    # If there are no duplicates, we continue.
    if _is_unique(signatures, name):
        return name

    # Otherwise, we retry…
    return _build_unique_name(path, node, suffixes, signatures)


def _build_posarg(node: ast.FunctionDef) -> Callable[..., Any]:
    """Curryfies the positional arguments builder."""

    return functools.partial(
        _build_argument,
        args = node.args.args,
        defaults = node.args.defaults,
        )


def _build_keyarg(node: ast.FunctionDef) -> Callable[..., Any]:
    """Curryfies the keyword arguments builder."""

    return functools.partial(
        _build_argument,
        args = node.args.kwonlyargs,
        defaults = node.args.kw_defaults,
        )


def _build_argument(
        acc: Tuple[Argument, ...],
        node: ast.arg,
        args: Tuple[Any, ...],
        defaults: Tuple[Any, ...],
        ) -> Tuple[Argument, ...]:
    """Builds an argument.

    Args:
        acc: An accumulated tuple of arguments (from reduce).
        node: An argument node.
        args: A tuple of argument nodes.
        defaults: A tuple of default value nodes.

    Returns:
        A tuple with the arguments.

    Examples:
        >>> acc = []
        >>> node = ast.arg(arg = "arg")
        >>> args = [node]
        >>> defaults = []
        >>> _build_argument(acc, node, args, defaults)
        (Argument(name='arg', default=None),)

    .. versionadded:: 1.0.0

    """

    default: Optional[str]
    argument: Argument

    default = _build_arg_default(len(acc), len(args), defaults)
    argument = Argument(node.arg, default)

    return (*acc, argument)


def _build_arg_default(
        n_acc: int,
        n_arg: int,
        defaults: Tuple[Any, ...],
        ) -> Optional[str]:
    """Builds the default value of an argument.

    Args:
        n_acc: The index of the function argument we're working with.
        n_arg: The total number of a function's arguments.
        defaults: The tuple of a function's default values.

    Returns:
        A default argument value, or None.


    Examples:
        >>> n_acc = 1
        >>> n_arg = 2
        >>> defaults = []
        >>> _build_arg_default(n_acc, n_arg, defaults)
        None

        >>> defaults = [1]
        >>> _build_arg_default(n_acc, n_arg, defaults)
        '1'

        >>> n_acc = 2
        >>> _build_arg_default(n_acc, n_arg, defaults)
        Traceback (most recent call last):
        IndexError: list index out of range

    .. versionadded:: 1.0.0

    """

    n_def: int = len(defaults)
    index: int

    # If there are no default values, we move on.
    if n_def == 0:
        return None

    # Otherwise we would be out of index for defaults.
    if n_arg - n_def > n_acc:
        return None

    # We define the defaults index based on the current visited argument.
    index = n_def + n_acc - n_arg

    return _build(defaults[index])


@deal.raises(NotImplementedError)
@deal.has()
def _build(node: Optional[ast.expr]) -> Any:
    """Generic builder."""

    if node is None:
        return None

    return to_value(node)  # type: ignore


@deal.pure
def _is_unique(seq: Tuple[Signature, ...], name: str) -> bool:
    """Check if a signature's name is unique or not.

    Args:
        seq: A sequence of signatures.
        name: The name of a specific function.

    Returns:
        bool: Is it?


    Examples:
        >>> signature = Signature("name", "file.py")
        >>> seq = [signature]
        >>> _is_unique(seq, "nom")
        True

        >>> _is_unique(seq, "name")
        False

    .. versionadded:: 1.0.0

    """

    is_unique: bool = not next(_where(seq, name), False)

    return is_unique


@deal.pure
def _where(
        seq: Tuple[Signature, ...],
        name: str,
        ) -> Generator[bool, None, None]:
    """Iterates over signatures to find the names named ``name``.

    Args:
        seq: A sequence of signatures.
        name: The name of a specific function.

    Returns:
        A generator to find a signature by name.

    Examples:
        >>> signature = Signature("name", "file.py")
        >>> seq = [signature]
        >>> list(_where(seq, "name"))
        [True]

        >>> list(_where(seq, "nom"))
        []

    .. versionadded:: 1.0.0

    """

    return (True for el in seq if el.name == name)


@typic.klass(always = True, strict = True)
@dataclasses.dataclass
class BuildSignatures(ast.NodeVisitor):
    """Builds signatures from the abstract syntax-tree of a revision.

    Attributes:
        files: The files to build signatures from.
        count: An iteration counter.
        signatures: The built signatures.

    Examples:
        >>> BuildSignatures(["file.py"])
        BuildSignatures(files=['file.py'], count=0, signatures=())

    .. versionadded:: 1.0.0

    """

    files: Union[List[str], Tuple[str, ...]]
    count: int = 0
    signatures: Tuple[Signature, ...] = ()

    @property
    def total(self) -> int:
        """The total number of files to build signatures from.

        Returns:
            int: The number of files.

        Examples:
            >>> builder = BuildSignatures(["file.py"])
            >>> builder.total
            1

        .. versionadded:: 1.0.0

        """

        return len(self.files)

    def __call__(self, source: str) -> None:
        """Builds all signatures from the passed source code.

        Arguments:
            source: The source code to build signatures from.

        Examples:
            >>> builder = BuildSignatures(["file.py"])
            >>> source = [
            ...     "def function(n: List[int] = [1]) -> int:",
            ...     "    return next(iter(n))",
            ...     ]
            >>> builder("\\n".join(source))
            >>> signature = next(iter(builder.signatures))
            >>> argument = next(iter(signature.arguments))

            >>> builder.signatures
            (Signature(name='...file.function', file='file.py', a...

            >>> signature.name
            '...file.function'

            >>> signature.file
            'file.py'

            >>> signature.arguments
            (Argument(name='n', default=('1',)),)

            >>> argument.name
            'n'

            >>> argument.default
            ('1',)

            >>> builder.count
            1

        .. versionadded:: 1.0.0

        """

        node = ast.parse(source, self.files[self.count], "exec")
        self.visit(node)
        self.count += 1

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """An :obj:`ast` node visitor."""

        file: str
        path: Path
        name: str
        args: Tuple[ast.arg, ...]
        kwds: Tuple[ast.arg, ...]
        posargs: Tuple[Argument, ...]
        keyargs: Tuple[Argument, ...]
        signature: Signature

        # We look for the corresponding ``file``.
        file = self.files[self.count]

        # We find the absolute path of the file.
        path = Path(file).resolve()

        # We take the node name as a base for checks.
        name = node.name

        # We pass if its a private function.
        if name.startswith("_") and not name.endswith("_"):
            return

        # We pass if it is a special function not in __init__ or __call__.
        if name.startswith("__") and name not in ("__init__", "__call__"):
            return

        # We find a unique name for each signature.
        name = _build_unique_name(path, node, iter(Suffix), self.signatures)

        # We build all positional arguments.
        args = tuple(node.args.args)
        posargs = functools.reduce(_build_posarg(node), args, ())

        # We build all keyword arguments.
        kwds = tuple(node.args.kwonlyargs)
        keyargs = functools.reduce(_build_keyarg(node), kwds, ())

        # We build the signature.
        signature = Signature(name, file, posargs + keyargs)

        # And we add it to the list of signatures.
        self.signatures = self.signatures + (signature,)
