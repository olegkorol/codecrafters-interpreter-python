from typing import Any
from app.grammar.expressions import Assign, ExprVisitor, Expr, Grouping, Binary, Logical, Unary, Literal, Variable
from app.utils import pretty_print

class AstPrinter(ExprVisitor):
    """
    This class is an implementation of the visitor interface.
    It is used to print an AST in a human-readable Lisp-like format.
    """
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self._parenthesize('group', expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value == None:
            return 'nil'
        if isinstance(expr.value, bool):
            return pretty_print(expr.value)
        return str(expr.value)
    
    def visit_logical(self, expr: Logical) -> Any:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)
    
    def visit_variable(self, expr: Variable) -> Any:
        return self._parenthesize(expr.name.lexeme)
    
    def visit_assign(self, expr: Assign) -> Any:
        return self._parenthesize(expr.name.lexeme, expr.value)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = [name]
        for expr in exprs:
            parts.append(expr.accept(self))
        # print(f"-> {parts}")
        return f'({" ".join(parts)})'