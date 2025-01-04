import sys
from app.types import TokenType, Token
from app.grammar.expressions import Expr, Grouping, Binary, Unary, Literal
from app.grammar.statements import Stmt, Print, Expression

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

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self._isAtEnd():
            statements.append(self.statement())
        return statements
    
    def parse_expr(self) -> Expr:
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
    
    # ----- Handles statements -----

    def statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self.print_stmt()
        return self.expression_stmt()

    def print_stmt(self) -> Stmt:
        value: Expr = self.expression()
        # self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        self._match(TokenType.SEMICOLON)
        return Print(value) # Stmt.Print
    
    def expression_stmt(self) -> Stmt:
        expr: Expr = self.expression()
        # self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        self._match(TokenType.SEMICOLON)
        return Expression(expr) # Stmt.Expression

    # ----- Handles expressions -----

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
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)
        
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