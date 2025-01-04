from typing import Any
from app.types import Token
from app.interpreter import LoxRuntimeError

class Environment:
	values: dict[str, Any]

	def __init__(self, values: dict[str, Any] = {}):
		self.values = values if values is not None else {}

	def define(self, name, value) -> Any:
		self.values[name] = value

	def get(self, name: Token):
		if name.lexeme in self.values:
			return self.values[name.lexeme]
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
