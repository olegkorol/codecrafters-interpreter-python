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

    # Uncomment this block to pass the first stage
    if file_contents:
        for char in file_contents:
            if char in ["(", ")"]:
                scan_paranthesis(char)
        sys.stdout.write("EOF  null\n")
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

def scan_paranthesis(char):
    match char:
        case "(":
            sys.stdout.write("LEFT_PAREN ( null\n")
        case ")":
            sys.stdout.write("RIGHT_PAREN ) null\n")


if __name__ == "__main__":
    main()
