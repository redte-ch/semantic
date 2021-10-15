# Copyright (c) 2018 Robin Hilliard
#
# Licensed under the MIT
# For details: https://opensource.org/licenses/MIT

"""Implements a @pipes decorator.

Adapted from `pipes`_.

.. versionadded:: 1.0.0

.. _pipes:
    https://github.com/robinhilliard/pipes/blob/master/pipeop/__init__.py

"""

import ast
import inspect
import itertools
import textwrap


class _PipeTransformer(ast.NodeTransformer):

    def visit_BinOp(self, node):
        if isinstance(node.op, (ast.LShift, ast.RShift)):
            # Convert function name / lambda etc without braces into call
            if not isinstance(node.right, ast.Call):
                return self.visit(ast.Call(
                    func = node.right,
                    args = [node.left],
                    keywords = [],
                    starargs = None,
                    kwargs = None,
                    lineno = node.right.lineno,
                    col_offset = node.right.col_offset
                    ))
            else:
                # Rewrite a >> b(...) as b(a, ...)
                node.right.args.insert(
                    0
                    if isinstance(node.op, ast.RShift)
                    else len(node.right.args),
                    node.left,
                    )

                return self.visit(node.right)

        else:
            return node


def pipes(func_or_class):
    """Implements a @pipes decorator.

    It converts the << and >> operators to mimic Elixir pipes.

    .. versionadded:: 1.0.0

    """

    if inspect.isclass(func_or_class):
        decorator_frame = inspect.stack()[1]
        ctx = decorator_frame[0].f_locals
        first_line_number = decorator_frame[2]

    else:
        ctx = func_or_class.__globals__
        first_line_number = func_or_class.__code__.co_firstlineno

    source = inspect.getsource(func_or_class)

    # AST data structure representing parsed function code
    tree = ast.parse(textwrap.dedent(source))

    # Fix line and column numbers so that debuggers still work
    ast.increment_lineno(tree, first_line_number - 1)
    source_indent = sum(1 for _ in itertools.takewhile(str.isspace, source))
    source_indent += 1

    for node in ast.walk(tree):
        if hasattr(node, "col_offset"):
            node.col_offset += source_indent

    # Update name of function or class to compile
    # tree.body[0].name = decorated_name

    # remove the pipe decorator so that we don't recursively
    # call it again. The AST node for the decorator will be a
    # Call if it had braces, and a Name if it had no braces.
    # The location of the decorator function name in these
    # nodes is slightly different.
    tree.body[0].decorator_list = [
        node for node in tree.body[0].decorator_list
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr != "pipes"
        or isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id != "pipes"
        or isinstance(node, ast.Name)
        and node.id != "pipes"
        ]

    # Apply the visit_BinOp transformation
    tree = _PipeTransformer().visit(tree)

    # now compile the AST into an altered function or class definition
    code = compile(
        tree,
        filename=(ctx['__file__'] if '__file__' in ctx else "repl"),
        mode="exec")

    # and execute the definition in the original context so that the
    # decorated function can access the same scopes as the original
    exec(code, ctx)

    # return the modified function or class - original is never called
    return ctx[tree.body[0].name]
