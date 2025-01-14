import random
import string
from typing import Any
from app.types import Token
from app.parser import Expr
from app.interpreter import LoxRuntimeError

characters = string.ascii_letters + string.digits

class Environment:
	enclosing: 'Environment | None'
	values: dict[str, Any]
	id: str

	def __init__(self, enclosing: 'Environment | None' = None, values: dict[str, Any] | None = None):
		self.id = self._random_id()
		self.enclosing = enclosing
		# We use .copy() to avoid multiple Environments sharing the same dictionary reference
		self.values = {} if values is None else values.copy()

	@staticmethod
	def _random_id() -> str:
		random_string = ''.join(random.choice(characters) for _ in range(10))
		return random_string

	def define(self, name: str, value: Any) -> Any:
		self.values[name] = value

	def assign(self, name: Token, value: Any) -> Any:
		if name.lexeme in self.values:
			self.values[name.lexeme] = value
			return
		if self.enclosing is not None:
			self.enclosing.assign(name, value)
			return
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

	def get(self, name: Token):
		if name.lexeme in self.values:
			return self.values[name.lexeme]
		if self.enclosing is not None:
			return self.enclosing.get(name)
		raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
