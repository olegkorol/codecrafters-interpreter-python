from dataclasses import dataclass
from abc import ABC, abstractmethod 
from typing import Any
from app.utils import pretty_print
from app.types import Token

"""
(5.1.3) A Grammar for Lox expressions

expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
"""

@dataclass
class Expr(ABC):
    """Base class for all expressions"""
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor') -> Any: ...

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_literal(self)

@dataclass 
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_grouping(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_unary(self)

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_binary(self)

class ExprVisitor(ABC):
    """
    Interface for the visitor pattern for expressions.
    """
    @abstractmethod
    def visit_binary(self, expr: 'Binary') -> Any: ...

    @abstractmethod 
    def visit_grouping(self, expr: 'Grouping') -> Any: ...

    @abstractmethod
    def visit_literal(self, expr: 'Literal') -> Any: ...

    @abstractmethod
    def visit_unary(self, expr: 'Unary') -> Any: ...
