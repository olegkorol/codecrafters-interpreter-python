import sys


def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    if file_contents:
        scan_errors = False
        file_contents_length = len(file_contents)
        index_to_ignore = None # Used to store indexes that are part of multiple-character lexemes

        for i in range(file_contents_length):
            if i in index_to_ignore:
                continue

            char = file_contents[i]
            next_char = file_contents[i + 1] if i < file_contents_length - 1 else None

            
            # Handles multiple-character lexemes
            if char == "=" and next_char == "=":
                success = scanner("==")
                index_to_ignore = i + 1
            elif char == "!" and next_char == "=":
                success = scanner("!=")
                index_to_ignore = i + 1
            elif char in ["<", ">"] and next_char == "=":
                success = scanner(char + "=")
                index_to_ignore = i + 1
            elif char == "/" and next_char == "/": # Comments `//` - Stop here
                print("EOF  null")
                return
            elif char == "<" and next_char == "|":
                print("x")
            # Handles single-character lexemes
            else:
                success = scanner(char)
            # Handles errors
            if not success:
                scan_errors = True
        print("EOF  null")

        if scan_errors:
            exit(65)
        else:
            exit(0)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

def scanner(char):
    match char:
        case "(":
            print("LEFT_PAREN ( null")
        case ")":
            print("RIGHT_PAREN ) null")
        case "{":
            print("LEFT_BRACE { null")
        case "}":
            print("RIGHT_BRACE } null")
        case "*":
            print("STAR * null")
        case ".":
            print("DOT . null")
        case ",":
            print("COMMA , null")
        case "+":
            print("PLUS + null")
        case "-":
            print("MINUS - null")
        case ";":
            print("SEMICOLON ; null")
        case "=":
            print("EQUAL = null")
        case "==":
            print("EQUAL_EQUAL == null")
        case "!":
            print("BANG ! null")
        case "!=":
            print("BANG_EQUAL != null")
        case "<":
            print("LESS < null")
        case "<=":
            print("LESS_EQUAL <= null")
        case ">":
            print("GREATER > null")
        case ">=":
            print("GREATER_EQUAL >= null")
        case "/":
            print("SLASH / null")
        case _:
            print(f"[line 1] Error: Unexpected character: {char}", file=sys.stderr)
            return False

    return True


if __name__ == "__main__":
    main()
