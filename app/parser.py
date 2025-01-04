import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from app.tokenizer import TokenType, Token

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
    Interface for the visitor pattern, used in AstPrinter.
    """
    @abstractmethod
    def visit_binary(self, expr: 'Binary') -> Any: ...

    @abstractmethod 
    def visit_grouping(self, expr: 'Grouping') -> Any: ...

    @abstractmethod
    def visit_literal(self, expr: 'Literal') -> Any: ...

    @abstractmethod
    def visit_unary(self, expr: 'Unary') -> Any: ...

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
        if expr.value == 'nil':
            return 'nil'
        return str(expr.value)#.lower()

    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        parts = [name]
        for expr in exprs:
            parts.append(expr.accept(self))
        # print(f"-> {parts}")
        return f'({" ".join(parts)})'    


"""
(6.2) Recursive Descent Parsing

expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
"""

class Parser:
    current: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def parse(self):
        return self.expression()

    def _advance(self) -> Token:
        """
        Consumes current token and returns it
        """
        if not self._isAtEnd():
            self.current += 1
        
        return self._previous()

    def _match(self, *types: TokenType) -> bool:
        """
        Checks token type and consumes it if it matches.
        """
        for type in types:
            if self._check(type):
                self._advance()
                return True

        return False
    
    def _check(self, type: TokenType) -> bool:
        """
        Checks token type without consuming it.
        """
        if self._isAtEnd():
            return False
        
        return self._peek().type == type

    def _consume(self, type: TokenType, message: str):
        if self._check(type):
            return self._advance()
        
        return error(self._peek(), message)

    def _isAtEnd(self) -> bool:
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    # ----------

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self._previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self._match(TokenType.SLASH, TokenType.STAR):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()
    
    def primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal('false')
        if self._match(TokenType.TRUE):
            return Literal('true')
        if self._match(TokenType.NIL):
            return Literal('nil')
        
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        
        if self._match(TokenType.LEFT_PAREN):
            expr = self.expression()
            # Parenthesis expressions must always have a closing ")"
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        return error(self._peek(), "Expect expression.")

class ParseError(RuntimeError):
    ...

def error(token: Token, message: str):
    if (token.type == TokenType.EOF):
        print(f"[line {token.line}] at end: {message}", file=sys.stderr)
    else:
        print(f"[line {token.line}] at '{token.lexeme}': {message}", file=sys.stderr)
    
    raise ParseError()