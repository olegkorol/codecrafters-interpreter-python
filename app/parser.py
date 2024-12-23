from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from app.tokenizer import TokenType

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
    """
    This class is an implementation of the visitor interface.
    It is used to print an AST in a human-readable Lisp-like format.
    """
    def print(self, expr: Expr) -> str:
        return expr.accept(self)
    
    def visit_binary(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self._parenthesize('group', expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value == 'nil':
            return 'nil'
        return str(expr.value)#.lower()

    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = [name]
        for expr in exprs:
            parts.append(expr.accept(self))
        print(parts)
        return f'({" ".join(parts)})'    


def parse_token(token: dict) -> Expr:
    if token["type"] == TokenType.EOF:
        return None
    elif token["type"] == TokenType.NUMBER or token["type"] == TokenType.STRING:
        expression = Literal(token["literal"])
        return expression
    else:
        expression = Literal(token["lexeme"])
        return expression

def parser(tokens: list[dict]) -> None:
    printer = AstPrinter()
    expression = None

    for token in tokens:
        expression = parse_token(token)
        if expression is not None:
            print(printer.print(expression))
        else:
            break

