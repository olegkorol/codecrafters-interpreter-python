from dataclasses import dataclass
from abc import ABC, abstractmethod 
from typing import Any
from app.types import Token
from app.grammar.expressions import Expr

@dataclass
class Stmt(ABC):
    """Base class for all statements"""
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor') -> Any: ...

@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr | None = None

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_var_stmt(self)

@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_expression_stmt(self)

@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_print_stmt(self)

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_while_stmt(self)

@dataclass
class Block(Stmt):
    statements: list[Stmt]
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_block_stmt(self)
    
@dataclass
class If(Stmt):
    condition: Expr
    thenBranch: Stmt
    elseBranch: 'Stmt | None'

    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_if_stmt(self)
    
@dataclass
class Function(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_function_stmt(self)

class StmtVisitor(ABC):
    """
    Interface for the visitor pattern for statements.
    """
    @abstractmethod
    def visit_expression_stmt(self, stmt: 'Expression') -> Any: ...

    @abstractmethod
    def visit_print_stmt(self, stmt: 'Print') -> Any: ...

    @abstractmethod
    def visit_var_stmt(self, stmt: 'Var') -> Any: ...

    @abstractmethod
    def visit_block_stmt(self, stmt: 'Block') -> Any: ...

    @abstractmethod
    def visit_if_stmt(self, stmt: 'If') -> Any: ...

    @abstractmethod
    def visit_while_stmt(self, stmt: 'While') -> Any: ...

    @abstractmethod
    def visit_function_stmt(self, stmt: 'Function') -> Any: ...
