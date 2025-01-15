from dataclasses import dataclass
from abc import ABC, abstractmethod 
from typing import Any
from app.utils import pretty_print
from app.types import Token

"""
(5.1.3) A Grammar for Lox expressions

expression     → literal
               | logical
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
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_logical(self)

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
class Variable(Expr):
    name: Token

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_variable(self)

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_binary(self)
    
@dataclass
class Assign(Expr):
    """
    We want the syntax tree to reflect that an l-value* isn't evaluated like a normal expression.
    That's why the Assign node has a Token for the left-hand side, not an Expr.

    *All of the expressions that we've seen so far that produce values are r-values.
     An l-value “evaluates” to a storage location that you can assign into.
    """
    name: Token
    value: Expr

    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_assign(self)

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

    @abstractmethod
    def visit_variable(self, expr: 'Variable') -> Any: ...

    @abstractmethod
    def visit_assign(self, expr: 'Assign') -> Any: ...

    @abstractmethod
    def visit_logical(self, expr: 'Logical') -> Any: ...
