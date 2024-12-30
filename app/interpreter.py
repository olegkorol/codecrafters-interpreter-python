from app.parser import Binary, ExprVisitor, Expr, Grouping, Literal, Unary
from app.tokenizer import TokenType
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
		case _:
			return value

class Interpreter(ExprVisitor):
	def evaluate(self, expr: Expr) -> Any:
		return expr.accept(self)
	
	def _isTruthy(self, value: Any):
		if value is None:
			return False
		if value == "nil":
			return False
		if isinstance(value, bool):
			return value
		if value == "true":
			return True
		if value == "false":
			return False
		return True

	def visit_literal(self, expr: Literal) -> Any:
		return expr.value

	def visit_grouping(self, expr: Grouping) -> Any:
		return self.evaluate(expr.expression)
	
	def visit_unary(self, expr: Unary) -> Any:
		right = self.evaluate(expr.right)

		match expr.operator.type:
			case TokenType.MINUS:
				if not isinstance(right, str):
					return -(right)
			case TokenType.BANG:
				return str(not self._isTruthy(right)).lower() # we want to output the bool as string
			case _:
				return "nil"
	
	def visit_binary(self, expr: Binary) -> Any:
		left = self.evaluate(expr.left)
		right = self.evaluate(expr.right)

		match expr.operator.type:
			case TokenType.PLUS:
				if type(left) == type(right):
					return left + right
			case TokenType.MINUS:
				return left - right
			case TokenType.STAR:
				return left * right
			case TokenType.SLASH:
				return left / right
			case TokenType.GREATER:
				return left > right
			case TokenType.GREATER_EQUAL:
				return left >= right
			case TokenType.LESS:
				return left < right
			case TokenType.LESS_EQUAL:
				return left <= right
			case TokenType.BANG_EQUAL:
				return left != right
			case TokenType.EQUAL_EQUAL:
				return left == right
			case _:
				return "nil"