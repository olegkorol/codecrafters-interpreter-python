import sys
from app.types import TokenType, Token
from app.grammar.expressions import Expr, Grouping, Binary, Unary, Literal, Variable, Assign, Logical, Call
from app.grammar.statements import Stmt, Print, Expression, Var, Block, If, While, Function, Return

class Parser:
    current: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def parse(self) -> list[Stmt]:
        declarations: list[Stmt] = []
        while not self._isAtEnd():
            declarations.append(self.declaration())
        return declarations
    
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
        """
        Consumes token if it matches token type. Otherwise, raises an error.
        """
        if self._check(type):
            return self._advance()
        
        return error(self._peek(), message)

    def _isAtEnd(self) -> bool:
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def _finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []

        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    error(self._peek(), "Can't have more than 255 arguments.")

                arguments.append(self.expression())

                if not self._match(TokenType.COMMA):
                    break

        paren: Token = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return Call(callee, paren, arguments)

    # ----- Handles declarations and statements -----

    def declaration(self) -> Stmt:
        if self._match(TokenType.FUN):
            return self.function("function")
        if self._match(TokenType.VAR):
            return self.variable_declaration()
        return self.statement()
        # TODO: add `synchronize()` in an `except` clause for error handling

    def function(self, kind: str) -> Stmt:
        name: Token = self._consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self._consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        parameters: list[Token] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    error(self._peek(), "Can't have more than 255 parameters.")
                
                parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter name."))

                if not self._match(TokenType.COMMA):
                    break

        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters")

        self._consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body: list[Stmt] = self.block()

        return Function(name, parameters, body)
            
    
    def variable_declaration(self) -> Stmt:
        name: Token = self._consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer: Expr | None = None
        if self._match(TokenType.EQUAL):
            initializer = self.expression()

        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Var(name, initializer) # Stmt.Print

    def statement(self) -> Stmt:
        if self._match(TokenType.FOR):
            return self.for_stmt()
        if self._match(TokenType.IF):
            return self.if_stmt()
        if self._match(TokenType.PRINT):
            return self.print_stmt()
        if self._match(TokenType.RETURN):
            return self.return_stmt()
        if self._match(TokenType.WHILE):
            return self.while_stmt()
        if self._match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_stmt()
    
    def for_stmt(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Stmt | None = None
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self.variable_declaration()
        else:
            initializer = self.expression_stmt()

        condition: Expr | None = None
        if not self._check(TokenType.SEMICOLON):
            condition = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment: Expr | None = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt | list[Stmt] = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def if_stmt(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()

        elseBranch = None
        if self._match(TokenType.ELSE):
            elseBranch = self.statement()
        
        return If(condition, thenBranch, elseBranch)

    def print_stmt(self) -> Stmt:
        value: Expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        self._match(TokenType.SEMICOLON)
        return Print(value) # Stmt.Print
    
    def return_stmt(self) -> Stmt:
        keyword = self._previous()
        value: Expr | None = None
        if not self._check(TokenType.SEMICOLON):
            value = self.expression()
        
        self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")

        return Return(keyword, value)
    
    def while_stmt(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN,"Expect '(' after 'while'." )
        condition: Expr = self.expression()
        self._consume(TokenType.RIGHT_PAREN,"Expect '(' after 'while'." )
        body: Stmt = self.statement()
        return While(condition, body)
    
    def block(self) -> list[Stmt]:
        statements: list[Stmt] = []

        while not self._check(TokenType.RIGHT_BRACE) and not self._isAtEnd():
            statements.append(self.declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

        return statements
    
    def expression_stmt(self) -> Stmt:
        expr: Expr = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        self._match(TokenType.SEMICOLON)
        return Expression(expr) # Stmt.Expression

    # ----- Handles expressions -----

    def expression(self) -> Expr:
        return self.assignment()
    
    def assignment(self) -> Expr:
        expr = self.logic_or()

        while self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)
            
            # Right now, the only valid target is a simple variable expression, but we’ll add fields later.
            else:
                error(equals, "Invalid assignment target.")

        return expr
    
    def logic_or(self) -> Expr:
        expr = self.logic_and()
        
        while self._match(TokenType.OR):
            operator: Token = self._previous()
            right: Expr = self.logic_and()
            expr: Expr = Logical(expr, operator, right)
        
        return expr
    
    def logic_and(self) -> Expr:
        expr = self.equality()
        
        while self._match(TokenType.AND):
            operator: Token = self._previous()
            right: Expr = self.equality()
            expr: Expr = Logical(expr, operator, right)
        
        return expr

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

        return self.call()
    
    def call(self) -> Expr:
        expr: Expr = self.primary()

        while True: # this will make sense when we expand the parser to handle properties on objects
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            else:
                break

        return expr
    
    def primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)
        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
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