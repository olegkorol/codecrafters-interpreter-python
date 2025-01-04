from dataclasses import dataclass
from abc import ABC, abstractmethod 
from typing import Any
from app.grammar.expressions import Expr

"""
(8.1) Statements

program        → statement* EOF ;
statement      → exprStmt
               | printStmt ;
exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
"""

@dataclass
class Stmt(ABC):
    """Base class for all statements"""
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor') -> Any: ...

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
    
class StmtVisitor(ABC):
    """
    Interface for the visitor pattern for statements.
    """
    @abstractmethod
    def visit_expression_stmt(self, stmt: Stmt) -> Any: ...

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt) -> Any: ...
