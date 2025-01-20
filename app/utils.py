from typing import Any
from app.types import Token

def pretty_print(value: Any):
	"""
	Pretty-printer to satisfy:
	> For the number literals, the tester will check that the program prints the number
	  with the minimum number of decimal places without losing precision.
	  (For example, 10.40 should be printed as 10.4).
	"""
	match value:
		case None:
			return "nil"
		case bool():
			return str(value).lower()
		case int():
			# Use repr to get full precision
			return repr(value)
		case float():
			# Remove .0 for whole numbers, preserve precision for others
			float_str = repr(value)
			return float_str.rstrip('0').rstrip('.') if float_str.endswith('.0') else float_str
		case _:
			return value
		
class LoxRuntimeError(RuntimeError):
	message: str
	token: Token

	def __init__(self, token: Token, message: str):
		super().__init__(message)
		self.message = message
		self.token = token