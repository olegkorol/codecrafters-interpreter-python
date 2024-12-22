import sys

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
            self.result_tokens.append("EOF  null")
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
                    self.result_tokens.append(f'STRING "{string_literal}" {string_literal}')
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
                    print(f'NUMBER {number_literal} {float(number_literal)}') if self.print_to_stdout else None
                    self.result_tokens.append(f'NUMBER {number_literal} {float(number_literal)}')
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
            self.result_tokens.append("EOF  null")
            exit(65)

        if self.is_identifier_open:
            self._resolve_identifier(self.identifier)
        
        print("EOF  null") if self.print_to_stdout else None
        self.result_tokens.append("EOF  null")

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
                self.result_tokens.append("LEFT_PAREN ( null")
            case ")":
                print("RIGHT_PAREN ) null") if self.print_to_stdout else None
                self.result_tokens.append("RIGHT_PAREN ) null")
            case "{":
                print("LEFT_BRACE { null") if self.print_to_stdout else None
                self.result_tokens.append("LEFT_BRACE { null")
            case "}":
                print("RIGHT_BRACE } null") if self.print_to_stdout else None
                self.result_tokens.append("RIGHT_BRACE } null")
            case "*":
                print("STAR * null") if self.print_to_stdout else None
                self.result_tokens.append("STAR * null")
            case ".":
                print("DOT . null") if self.print_to_stdout else None
                self.result_tokens.append("DOT . null")
            case ",":
                print("COMMA , null") if self.print_to_stdout else None
                self.result_tokens.append("COMMA , null")
            case "+":
                print("PLUS + null") if self.print_to_stdout else None
                self.result_tokens.append("PLUS + null")
            case "-":
                print("MINUS - null") if self.print_to_stdout else None
                self.result_tokens.append("MINUS - null")
            case ";":
                print("SEMICOLON ; null") if self.print_to_stdout else None
                self.result_tokens.append("SEMICOLON ; null")
            case "=":
                print("EQUAL = null") if self.print_to_stdout else None
                self.result_tokens.append("EQUAL = null")
            case "==":
                print("EQUAL_EQUAL == null") if self.print_to_stdout else None
                self.result_tokens.append("EQUAL_EQUAL == null")
            case "!":
                print("BANG ! null") if self.print_to_stdout else None
                self.result_tokens.append("BANG ! null")
            case "!=":
                print("BANG_EQUAL != null") if self.print_to_stdout else None
                self.result_tokens.append("BANG_EQUAL != null")
            case "<":
                print("LESS < null") if self.print_to_stdout else None
                self.result_tokens.append("LESS < null")
            case "<=":
                print("LESS_EQUAL <= null") if self.print_to_stdout else None
                self.result_tokens.append("LESS_EQUAL <= null")
            case ">":
                print("GREATER > null") if self.print_to_stdout else None
                self.result_tokens.append("GREATER > null")
            case ">=":
                print("GREATER_EQUAL >= null") if self.print_to_stdout else None
                self.result_tokens.append("GREATER_EQUAL >= null")
            case "/":
                print("SLASH / null") if self.print_to_stdout else None
                self.result_tokens.append("SLASH / null")
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
            self.result_tokens.append(f"{identifier.upper()} {identifier} null")
        else:
            print(f"IDENTIFIER {identifier} null") if self.print_to_stdout else None
            self.result_tokens.append(f"IDENTIFIER {identifier} null")

        self.identifier = ""