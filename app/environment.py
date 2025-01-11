from typing import Any
from app.types import Token
from app.parser import Expr
from app.interpreter import LoxRuntimeError

class Environment:
	values: dict[str, Any]

	def __init__(self, values: dict[str, Any] = {}):
		self.values = values if values is not None else {}

	def define(self, name: str, value: Any) -> Any:
		self.values[name] = value

	def assign(self, name: Token, value: Any) -> Any:
		if name.lexeme in self.values:
			self.values[name.lexeme] = value
			return
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

	def get(self, name: Token):
		if name.lexeme in self.values:
			return self.values[name.lexeme]
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
