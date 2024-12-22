import sys
from app.tokenizer import Tokenizer
from app.parser import parser

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <tokenize | parse> <filename>", file=sys.stderr)
        exit(64)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(64)

    with open(filename) as file:
        file_contents = file.read()

    match command:
        case "tokenize":
            Tokenizer(file_contents, print_to_stdout=True).tokenize()
        case "parse":
            tokens = Tokenizer(file_contents, print_to_stdout=False).tokenize()
            parser(tokens)

    exit()

if __name__ == "__main__":
    main()
