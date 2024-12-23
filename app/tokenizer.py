import sys
from enum import Enum

TokenType = Enum("TokenType", [
    "NUMBER", "STRING", "IDENTIFIER", "LEFT_PAREN", "RIGHT_PAREN", "LEFT_BRACE", "RIGHT_BRACE",
    "STAR", "DOT", "COMMA", "PLUS", "MINUS", "SEMICOLON", "EQUAL", "EQUAL_EQUAL", "BANG",
    "BANG_EQUAL", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL", "SLASH", "EOF",
    # Reserved words
    "AND", "CLASS", "ELSE", "FALSE", "FOR", "FUN", "IF", "NIL", "OR", "PRINT", "RETURN", "SUPER",
    "THIS", "TRUE", "VAR", "WHILE"
])

class Tokenizer:
    scan_errors = False
    is_identifier_open = False
    identifier = ""
    result_tokens = []

    def __init__(self, file_contents: str, print_to_stdout: bool = False):
        self.file_contents: str = file_contents
        self.file_contents_length: int = len(file_contents)
        self.print_to_stdout = print_to_stdout

    def tokenize(self):
        index_to_ignore = None # Used to store indexes that are part of multiple-character lexemes
        current_line = 1
        ignore_rest_of_line = None
        is_string_literal_open = False
        string_literal = ""
        number_literal = "" # Stored as string
        
        if not len(self.file_contents):
            print("EOF  null") if self.print_to_stdout else None
            self.result_tokens.append({"type": TokenType.EOF, "lexeme": "null", "literal": None})
            return self.result_tokens

        for i in range(self.file_contents_length):
            if i == index_to_ignore:
                continue

            char = self.file_contents[i]
            next_char = self.file_contents[i + 1] if i < self.file_contents_length - 1 else None

            if char == "\n":
                current_line += 1
                continue

            # This is set in action when we find a comment. The rest of the line is ignored
            if current_line == ignore_rest_of_line:
                continue

            # Handles string literals
            if char == '"': # String literals
                is_string_literal_open = not is_string_literal_open
                if not is_string_literal_open:
                    print(f'STRING "{string_literal}" {string_literal}') if self.print_to_stdout else None
                    self.result_tokens.append({"type": TokenType.STRING, "lexeme": string_literal, "literal": string_literal})
                    string_literal = ""
                continue

            if is_string_literal_open:
                # Adds content to string literal until it is closed
                string_literal += char
                continue

            # Handles number literals
            if (char.isdigit() or (char == '.' and next_char and next_char.isdigit())) and not self.is_identifier_open:
                number_literal += char
                if not next_char or not (next_char.isdigit() or next_char == '.'):
                    print(f"NUMBER {number_literal} {float(number_literal)}") if self.print_to_stdout else None
                    self.result_tokens.append({"type": TokenType.NUMBER, "lexeme": number_literal, "literal": float(number_literal)})
                    number_literal = ""
                continue

            # Handles other multiple-character lexemes
            if char == "=" and next_char == "=":
                self._scan("==", current_line)
                index_to_ignore = i + 1
            elif char == "!" and next_char == "=":
                self._scan("!=", current_line)
                index_to_ignore = i + 1
            elif char in ["<", ">"] and next_char == "=":
                self._scan(char + "=", current_line)
                index_to_ignore = i + 1
            elif char == "/" and next_char == "/": # Comments `//` - Stop here
                ignore_rest_of_line = current_line
                continue
            elif char in ["\t", " "]: # Ignore these
                self._resolve_identifier(self.identifier)
                continue
            elif (char.isalpha() or char == "_") or (self.is_identifier_open and char.isdigit()):
                self.is_identifier_open = True
                self.identifier += char
            # Handles single-character lexemes
            else:
                self._scan(char, current_line)

        # If we get here, but a string literal is still open, throw an error and exit early
        if is_string_literal_open:
            print(f"[line {current_line}] Error: Unterminated string.", file=sys.stderr)
            print("EOF  null") if self.print_to_stdout else None
            self.result_tokens.append({"type": TokenType.EOF, "lexeme": "null", "literal": None})
            exit(65)

        if self.is_identifier_open:
            self._resolve_identifier(self.identifier)
        
        print("EOF  null") if self.print_to_stdout else None
        self.result_tokens.append({"type": TokenType.EOF, "lexeme": "null", "literal": None})

        if self.scan_errors:
            exit(65)
        else:
            return self.result_tokens

    def _scan(self, char, current_line):
        # If it gets to this function and we still have an identifier open, we need to close it
        if self.is_identifier_open:
            self._resolve_identifier(self.identifier)

        match char:
            case "(":
                print("LEFT_PAREN ( null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.LEFT_PAREN, "lexeme": "(", "literal": None})
            case ")":
                print("RIGHT_PAREN ) null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.RIGHT_PAREN, "lexeme": ")", "literal": None})
            case "{":
                print("LEFT_BRACE { null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.LEFT_BRACE, "lexeme": "{", "literal": None})
            case "}":
                print("RIGHT_BRACE } null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.RIGHT_BRACE, "lexeme": "}", "literal": None})
            case "*":
                print("STAR * null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.STAR, "lexeme": "*", "literal": None})
            case ".":
                print("DOT . null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.DOT, "lexeme": ".", "literal": None})
            case ",":
                print("COMMA , null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.COMMA, "lexeme": ",", "literal": None})
            case "+":
                print("PLUS + null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.PLUS, "lexeme": "+", "literal": None})
            case "-":
                print("MINUS - null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.MINUS, "lexeme": "-", "literal": None})
            case ";":
                print("SEMICOLON ; null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.SEMICOLON, "lexeme": ";", "literal": None})
            case "=":
                print("EQUAL = null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.EQUAL, "lexeme": "=", "literal": None})
            case "==":
                print("EQUAL_EQUAL == null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.EQUAL_EQUAL, "lexeme": "==", "literal": None})
            case "!":
                print("BANG ! null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.BANG, "lexeme": "!", "literal": None})
            case "!=":
                print("BANG_EQUAL != null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.BANG_EQUAL, "lexeme": "!=", "literal": None})
            case "<":
                print("LESS < null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.LESS, "lexeme": "<", "literal": None})
            case "<=":
                print("LESS_EQUAL <= null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.LESS_EQUAL, "lexeme": "<=", "literal": None})
            case ">":
                print("GREATER > null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.GREATER, "lexeme": ">", "literal": None})
            case ">=":
                print("GREATER_EQUAL >= null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.GREATER_EQUAL, "lexeme": ">=", "literal": None})
            case "/":
                print("SLASH / null") if self.print_to_stdout else None
                self.result_tokens.append({"type": TokenType.SLASH, "lexeme": "/", "literal": None})
            case _:
                print(f"[line {current_line}] Error: Unexpected character: {char}", file=sys.stderr)
                self.scan_errors = True
                return False
        return True

    def _resolve_identifier(self, identifier: str):
        reserved_words = ["and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"]

        self.is_identifier_open = False

        if not identifier:
            self.identifier = ""
            return

        if identifier in reserved_words:
            print(f"{identifier.upper()} {identifier} null") if self.print_to_stdout else None
            self.result_tokens.append({"type": getattr(TokenType, identifier.upper()), "lexeme": identifier, "literal": None})
        else:
            print(f"IDENTIFIER {identifier} null") if self.print_to_stdout else None
            self.result_tokens.append({"type": TokenType.IDENTIFIER, "lexeme": identifier, "literal": None})

        self.identifier = ""