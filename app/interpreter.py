from app.parser import Binary, ExprVisitor, Expr, Grouping, Literal, Unary
from app.tokenizer import TokenType, Token
from typing import Any

def pretty_print(value: Any):
	"""
	Pretty-printer to satisfy:
	> For the number literals, the tester will check that the program prints the number
	  with the minimum number of decimal places without losing precision.
	  (For example, 10.40 should be printed as 10.4).
	"""
	match value:
		case float():
			return f"{value:g}"
		case None:
			return "nil"
		case bool():
			return str(value).lower()
		case _:
			return value

class Interpreter(ExprVisitor):
	def interpret(self, expr: Expr) -> None:
		value = self.evaluate(expr)
		print(self._stringify(value))

	def evaluate(self, expr: Expr) -> Any:
		return expr.accept(self)
	
	@staticmethod
	def _stringify(value: Any):
		if value == None:
			return 'nil'
		else:
			return pretty_print(value)
	
	def _isTruthy(self, value: Any):
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
		if isinstance(left, (int, float)) and isinstance(right, (int, float)):
			return
		else:
			raise LoxRuntimeError(operator, "Operands must be numbers.")

	def visit_literal(self, expr: Literal) -> Any:
		return expr.value

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
	
	def visit_binary(self, expr: Binary) -> Any:
		left = self.evaluate(expr.left)
		right = self.evaluate(expr.right)

		match expr.operator.type:
			case TokenType.PLUS:
				if isinstance(left, str) and isinstance(right, str):
					return left + right
				elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
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
			

class LoxRuntimeError(RuntimeError):
	message: str
	token: Token

	def __init__(self, token: Token, message: str):
		super().__init__(message)
		self.message = message
		self.token = token