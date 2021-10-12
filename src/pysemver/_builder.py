# Copyleft (ɔ) 2021 Mauko Quiroga <mauko@pm.me>
#
# Licensed under the EUPL-1.2-or-later
# For details: https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
#

from __future__ import annotations

from typing import (
    Any,
    Callable,
    Generator,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Union,
    )

import ast
import functools
import pathlib

import deal
import typic

from ._fn import _
from ._models import ArgType, Argument, RetType, Signature, Suffix


@typic.klass(always = True, strict = True)
class SignatureBuilder(ast.NodeVisitor):
    """Builds signatures from the abstract syntax-tree of a revision.

    Attributes:
        files: The files to build signatures from.
        count: An iteration counter.
        signatures: The built signatures.

    Examples:
        >>> SignatureBuilder(["file.py"])
        SignatureBuilder(files=['file.py'], count=0, signatures=())

    .. versionadded:: 36.1.0

    """

    files: Sequence[str]
    count: int = 0
    signatures: Tuple[Signature, ...] = ()

    @property
    @deal.pure
    def total(self) -> int:
        """The total number of files to build signatures from.

        Returns:
            int: The number of files.

        Examples:
            >>> builder = SignatureBuilder(["file.py"])
            >>> builder.total
            1

        .. versionadded:: 36.1.0

        """

        return len(self.files)

    @deal.pure
    # @typic.al(strict = True)
    def __call__(self, source: str) -> None:
        """Builds all signatures from the passed source code.

        Arguments:
            source: The source code to build signatures from.

        Examples:
            >>> builder = SignatureBuilder(["file.py"])
            >>> source = [
            ...     "def function(n: List[int] = [1]) -> int:",
            ...     "    return next(iter(n))",
            ...     ]
            >>> builder("\\n".join(source))
            >>> signature = next(iter(builder.signatures))
            >>> argument = next(iter(signature.arguments))

            >>> builder.signatures
            (Signature(name='pysemver.file.function', file='file.py', a...

            >>> signature.name
            'pysemver.file.function'

            >>> signature.file
            'file.py'

            >>> signature.arguments
            (Argument(name='n', types=(ArgType(name='List'), ArgType(name='i...

            >>> argument.name
            'n'

            >>> argument.types
            (ArgType(name='List'), ArgType(name='int'))

            >>> argument.default
            ('1',)

            >>> signature.returns
            (RetType(name='int'),)

            >>> builder.count
            1

        .. versionadded:: 36.1.0

        """

        node = ast.parse(source, self.files[self.count], "exec")
        self.visit(node)
        self.count += 1

    @deal.pure
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """An :obj:`ast` node visitor."""

        file: str
        path: pathlib.Path
        name: str
        args: Sequence[ast.arg]
        kwds: Sequence[ast.arg]
        posargs: Tuple[Argument, ...]
        keyargs: Tuple[Argument, ...]
        returns: Tuple[RetType, ...]
        signature: Signature

        # We look for the corresponding ``file``.
        file = self.files[self.count]

        # We find the absolute path of the file.
        path = pathlib.Path(file).resolve()

        # We take the node name as a base for checks.
        name = node.name

        # We pass if its a private function.
        if name.startswith("_") and not name.endswith("_"):
            return

        # We pass if it is a special function not in __init__ or __call__.
        if name.startswith("__") and name not in ("__init__", "__call__"):
            return

        # We find a unique name for each signature.
        name = self._build_unique_name(path, node, iter(Suffix))

        # We build all positional arguments.
        args = node.args.args
        posargs = functools.reduce(self._build_posarg(node), args, ())

        # We build all keyword arguments.
        kwds = node.args.kwonlyargs
        keyargs = functools.reduce(self._build_keyarg(node), kwds, ())

        # We build the return types.
        returns = self._build_returns(node)

        # We build the signature.
        signature = Signature(name, file, posargs + keyargs, returns)

        # And we add it to the list of signatures.
        self.signatures = self.signatures + (signature,)

    @deal.pure
    # @typic.al(strict = True)
    def _build_unique_name(
            self,
            path: pathlib.Path,
            node: ast.FunctionDef,
            suffixes: Iterator[Suffix],
            ) -> str:
        """Builds an unique signature name."""

        module: str
        name: str
        decorator: ast.expr

        # We build the module name with the name of the parent path, a
        # folder, and the name of the file, without the extension.
        module = f"{path.parts[-2]}.{path.stem}"

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
        if self._is_unique(name):
            return name

        # Otherwise, we retry…
        return self._build_unique_name(path, node, suffixes)

    @deal.pure
    # @typic.al(strict = True)
    def _build_posarg(self, node: ast.FunctionDef) -> Callable[..., Any]:
        """Curryfies the positional arguments builder."""

        return functools.partial(
            self._build_argument,
            args = node.args.args,
            defaults = node.args.defaults,
            )

    @deal.pure
    # @typic.al(strict = True)
    def _build_keyarg(self, node: ast.FunctionDef) -> Callable[..., Any]:
        """Curryfies the keyword arguments builder."""

        return functools.partial(
            self._build_argument,
            args = node.args.kwonlyargs,
            defaults = node.args.kw_defaults,
            )

    @deal.pure
    # @typic.al(strict = True)
    def _build_argument(
            self,
            acc: Sequence[Argument],
            node: ast.arg,
            args: Sequence[Any],
            defaults: Sequence[Any],
            ) -> Sequence[Argument]:
        """Builds an argument."""

        types: Optional[Tuple[ArgType, ...]]
        default: Optional[str]
        argument: Argument

        types = self._build_arg_types(node)
        default = self._build_arg_default(len(acc), len(args), defaults)
        argument = Argument(node.arg, types, default)

        return (*acc, argument)

    @deal.pure
    # @typic.al(strict = True)
    def _build_arg_types(self, node: ast.arg) -> Optional[Tuple[ArgType, ...]]:
        """Builds the types of an argument."""

        # We try to build types from the type annotation of the node.
        types = self._build(node.annotation, ArgType)

        # We do always return a tuple of types, or None.
        if types is not None and not isinstance(types, tuple):
            return types,

        return types

    @deal.pure
    # @typic.al(strict = True)
    def _build_arg_default(
            self,
            n_acc: int,
            n_arg: int,
            defaults: Sequence[Any],
            ) -> Optional[str]:
        """Builds the default value of an argument."""

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

        return self._build(defaults[index])

    @deal.pure
    # @typic.al(strict = True)
    def _build_returns(self, node: ast.FunctionDef) -> Tuple[RetType, ...]:
        """Builds a return type."""

        # We try to build return types from the returns of the node.
        returns = self._build(node.returns, RetType)

        # We do always return a tuple of types, or None.
        if returns is not None and not isinstance(returns, tuple):
            returns = returns,

        return returns

    @deal.pure
    # @typic.al(strict = True)
    def _build(
            self,
            node: Optional[Union[ast.expr, ast.slice]],
            builder: Callable[..., Any] = _,
            ) -> Any:
        """Generic builder."""

        if node is None:
            return None

        if isinstance(node, ast.Ellipsis):
            return builder("...")

        if isinstance(node, ast.Attribute):
            return builder(str(node.attr))

        if isinstance(node, ast.Name):
            return builder(str(node.id))

        if isinstance(node, (ast.Constant, ast.NameConstant)):
            return builder(str(node.value))

        if isinstance(node, ast.Num):
            return builder(str(node.n))

        if isinstance(node, ast.Str):
            return builder(str(node.s))

        if isinstance(node, ast.Call):
            return self._build(node.func, builder)

        if isinstance(node, ast.Index):
            return self._build(node.value, builder)

        # If we get a sequence or collection, we have to traverse
        # each item recursively.
        if isinstance(node, (ast.List, ast.Set, ast.Tuple)):
            return tuple(self._build(item, builder) for item in node.elts)

        # Also, if we get something ``like[this]``, we have to recurse in order
        # to extract the values.
        if isinstance(node, ast.Subscript):
            return (
                self._build(node.value, builder),
                self._build(node.slice, builder),
                )

        # Finally, if we have a dict, we have to both traverse recursively
        # while building tuples for each key-value pair.
        if isinstance(node, ast.Dict):
            return tuple(
                (
                    self._build(key, builder),
                    self._build(value, builder),
                    )
                for key, value in tuple(zip(node.keys, node.values))
                )

        raise TypeError(ast.dump(node))

    @deal.pure
    # @typic.al(strict = True)
    def _is_unique(self, name: str) -> bool:
        """Check if a signature's name is unique or not."""

        # We add a default value to avoid a StopIteration.
        is_unique: bool = not next(self._find(name), False)

        return is_unique

    @deal.pure
    def _find(self, name: str) -> Generator[bool, None, None]:
        """Check if there is a signature with ``name``."""

        return (True for signature in self.signatures if signature.name == name)
