import time
from typing import Any
from abc import ABC, abstractmethod
from app.types import TokenType, Token
from app.utils import pretty_print, LoxRuntimeError
from app.grammar.expressions import Assign, Call, Expr, Grouping, Binary, Logical, Unary, Literal, ExprVisitor, Variable
from app.grammar.statements import Function, Stmt, Print, Expression, StmtVisitor, Var, Block, If, While
from app.environment import Environment

class Interpreter(ExprVisitor, StmtVisitor):
	def __init__(self):
		self._globals: Environment = Environment()
		self._environment: Environment = self._globals

		# We define native functions here
		self._globals.define("clock", ClockCallable())

	def interpret(self, statements: list[Stmt]) -> Any:
		for statement in statements:
			self.execute(statement)

	# def interpret_expr(self, expr: Expr) -> None:
	# 	value = self.evaluate(expr)
	# 	print(self._stringify(value))

	def evaluate(self, expr: Expr) -> Any:
		return expr.accept(self)
	
	def execute(self, stmt: Stmt) -> Any:
		stmt.accept(self)

	def execute_block(self, statements: list[Stmt], environment: Environment) -> Any:
		previous: Environment = self._environment

		try:
			self._environment = environment
			for statement in statements:
				self.execute(statement)
		finally:
			self._environment = previous
			return

	@staticmethod
	def _stringify(value: Any):
		if value == None:
			return 'nil'
		else:
			return pretty_print(value)
	
	@staticmethod
	def _isTruthy(value: Any):
		if value is None:
			return False
		if value == 'nil':
			return False
		if isinstance(value, bool):
			return value
		if value == 'true':
			return True
		if value == 'false':
			return False
		return True
	
	@staticmethod
	def _checkNumberOperands(operator: Token, left: Any, right: Any):
		if (
			(isinstance(left, (int, float)) and not isinstance(left, bool)) and
			(isinstance(right, (int, float)) and not isinstance(right, bool))
		):
			return
		else:
			raise LoxRuntimeError(operator, "Operands must be numbers.")
	
	# ----- Handles statements (StmtVisitor) -----

	def visit_function_stmt(self, stmt: Function) -> Any:
		function: LoxFunction = LoxFunction(stmt)
		self._environment.define(stmt.name.lexeme, function)
		return None

	def visit_var_stmt(self, stmt: Var) -> Any:
		value = None
		if stmt.initializer is not None:
			value = self.evaluate(stmt.initializer)
		self._environment.define(stmt.name.lexeme, value)
		return None
	
	def visit_expression_stmt(self, stmt: Expression) -> None:
		self.evaluate(stmt.expression)
	
	def visit_print_stmt(self, stmt: Print) -> None:
		value = self.evaluate(stmt.expression)
		print(self._stringify(value))

	def visit_block_stmt(self, stmt: Block) -> None:
		new_environment = Environment(self._environment)
		self.execute_block(stmt.statements, new_environment)

	def visit_if_stmt(self, stmt: If) -> Any:
		if self._isTruthy(self.evaluate(stmt.condition)):
			self.execute(stmt.thenBranch)
		elif stmt.elseBranch is not None:
			self.execute(stmt.elseBranch)
		else:
			return None

	def visit_while_stmt(self, stmt: While) -> Any:
		while self._isTruthy(self.evaluate(stmt.condition)):
			self.execute(stmt.body)
		return None

	# ----- Handles expressions (ExprVisitor) -----

	def visit_literal(self, expr: Literal) -> Any:
		return expr.value
	
	def visit_logical(self, expr: Logical) -> Any:
		left: Expr = self.evaluate(expr.left)

		match expr.operator.type:
			case TokenType.OR:
				if self._isTruthy(left):
					return left
			case TokenType.AND:
				if not self._isTruthy(left):
					return left
		
		return self.evaluate(expr.right)

	def visit_grouping(self, expr: Grouping) -> Any:
		return self.evaluate(expr.expression)
	
	def visit_unary(self, expr: Unary) -> Any:
		right = self.evaluate(expr.right)

		match expr.operator.type:
			case TokenType.MINUS:
				# bool is a subclass of int in Python, hence the explicit exclusion
				if isinstance(right, (int, float)) and not isinstance(right, bool):
					return -(right)
				else:
					raise LoxRuntimeError(expr.operator, "Operand must be a number.")
			case TokenType.BANG:
				return not self._isTruthy(right)
			case _:
				return "nil"
			
	def visit_call(self, expr: Call) -> Any:
		callee = self.evaluate(expr.callee)
		arguments = [self.evaluate(argument) for argument in expr.arguments]

		if not isinstance(callee, LoxCallable):
			raise RuntimeError(expr.paren, "Can only call functions and classes.")
		
		function: LoxCallable = callee

		if len(arguments) != function.arity():
			raise RuntimeError(
				expr.paren,
				f"Expected {function.arity()} arguments but got {len(arguments)}."
				)

		return function.call(self, arguments)
	
	def visit_variable(self, expr: Variable) -> Any:
		return self._environment.get(expr.name)
	
	def visit_binary(self, expr: Binary) -> Any:
		left = self.evaluate(expr.left)
		right = self.evaluate(expr.right)

		match expr.operator.type:
			case TokenType.PLUS:
				if isinstance(left, str) and isinstance(right, str):
					return left + right
				elif (
					(isinstance(left, (int, float)) and not isinstance(left, bool)) and
					(isinstance(right, (int, float)) and not isinstance(right, bool))
				):
					return left + right
				else:
					raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
			case TokenType.MINUS:
				self._checkNumberOperands(expr.operator, left, right)
				return left - right
			case TokenType.STAR:
				self._checkNumberOperands(expr.operator, left, right)
				return left * right
			case TokenType.SLASH:
				self._checkNumberOperands(expr.operator, left, right)
				return left / right
			case TokenType.GREATER:
				self._checkNumberOperands(expr.operator, left, right)
				return left > right
			case TokenType.GREATER_EQUAL:
				self._checkNumberOperands(expr.operator, left, right)
				return left >= right
			case TokenType.LESS:
				self._checkNumberOperands(expr.operator, left, right)
				return left < right
			case TokenType.LESS_EQUAL:
				self._checkNumberOperands(expr.operator, left, right)
				return left <= right
			case TokenType.BANG_EQUAL:
				return left != right
			case TokenType.EQUAL_EQUAL:
				return left == right
			case _:
				return None
			
	def visit_assign(self, expr: Assign) -> Any:
		value = self.evaluate(expr.value)
		self._environment.assign(expr.name, value)
		return value


# ----------- Funtions and other *callables* ---------------

class LoxCallable(ABC):
	@abstractmethod
	def call(self, interpreter: Interpreter, arguments: list) -> Any: ...
	
	@abstractmethod
	def arity(self) -> int: ...

	# optional method
	def __str__(self) -> str:
		return ""
	
class LoxFunction(LoxCallable):
	declaration: Function

	def __init__(self, declaration: Function):
		self.declaration = declaration

	def call(self, interpreter: Interpreter, arguments: list) -> None:
		environment = Environment(interpreter._globals)

		for i in range(len(self.declaration.params)):
			param = self.declaration.params[i]
			environment.define(param.lexeme, arguments[i])

		interpreter.execute_block(self.declaration.body, environment)

		return None

	def arity(self) -> int:
		return len(self.declaration.params)

	def __str__(self) -> str:
		return f"<fn {self.declaration.name.lexeme} >"

# ------------ Native functions and methods ---------------

class ClockCallable(LoxCallable):
	@staticmethod
	def arity() -> int:
		return 0
	
	@staticmethod
	def call(interpreter: Interpreter, arguments: list) -> int:
		return int(time.time())
	
	@staticmethod
	def __str__() -> str:
		return "<native fn>"