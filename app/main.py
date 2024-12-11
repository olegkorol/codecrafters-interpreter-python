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
        for char in file_contents:
            success = scanner(char)
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
        case _:
            print(f"[line 1] Error: Unexpected character: {char}", file=sys.stderr)
            return False

    return True


if __name__ == "__main__":
    main()
