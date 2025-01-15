from dataclasses import dataclass
from abc import ABC, abstractmethod 
from typing import Any
from app.types import Token
from app.grammar.expressions import Expr

"""
(8.1) Statements
(8.2) Variable syntax [adds declarations]
(8.5.2) Block syntax semantics [adds blocks]
(9.2) Conditional execution [adds if statements]

program        → declaration* EOF ;
declaration    → varDecl
               | statement ;
statement      → exprStmt
               | ifStmt
               | printStmt
               | block ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;
exprStmt       → expression ";" ;
ifStmt         → "if" "(" expression ")" statement
               ( "else" statement )? ;
printStmt      → "print" expression ";" ;
block          → "{" declaration* "}" ;
"""

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

class StmtVisitor(ABC):
    """
    Interface for the visitor pattern for statements.
    """
    @abstractmethod
    def visit_expression_stmt(self, stmt: Stmt) -> Any: ...

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt) -> Any: ...

    @abstractmethod
    def visit_var_stmt(self, stmt: Stmt) -> Any: ...

    @abstractmethod
    def visit_block_stmt(self, stmt: Stmt) -> Any: ...

    @abstractmethod
    def visit_if_stmt(self, stmt: Stmt) -> Any: ...
