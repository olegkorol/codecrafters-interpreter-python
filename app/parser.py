from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class Expr:
    """Base class for all expressions"""
    pass

class ExprVisitor(ABC):
    """Interface for the visitor pattern"""
    @abstractmethod
    def visit_binary(self, expr: 'Binary') -> str:
        pass

    @abstractmethod 
    def visit_grouping(self, expr: 'Grouping') -> str:
        pass

    @abstractmethod
    def visit_literal(self, expr: 'Literal') -> str:
        pass

    @abstractmethod
    def visit_unary(self, expr: 'Unary') -> str:
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: str  
    right: Expr

    def accept(self, visitor: ExprVisitor) -> str:
        return visitor.visit_binary(self)

@dataclass 
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor) -> str:
        return visitor.visit_grouping(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor) -> str:
        return visitor.visit_literal(self)

@dataclass
class Unary(Expr):
    operator: str
    right: Expr

    def accept(self, visitor: ExprVisitor) -> str:
        return visitor.visit_unary(self)

class AstPrinter(ExprVisitor):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self._parenthesize('group', expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value == 'nil':
            return 'nil'
        return str(expr.value).lower()

    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = [name]
        for expr in exprs:
            # parts.append(' ')
            parts.append(expr.accept(self))
        return f'({" ".join(parts)})'    
    
    # def _dumb_print(self, expr: Expr) -> str:
    #     if expr.value is None:
    #         return 'nil'
    #     if isinstance(expr.value, bool):
    #        return str(expr.value).lower()
    #     return str(expr.value)
