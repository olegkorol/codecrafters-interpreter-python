import sys
from app.tokenizer import Tokenizer, TokenType
from app.parser import AstPrinter, Binary, Unary, Token, Literal, Grouping, Parser, ParseError

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
            try:
                tokens = Tokenizer(file_contents, print_to_stdout=False).tokenize()
                # print(f"-> SCANNED TOKENS:\n{tokens}\n")
                ast = Parser(tokens).parse()
                # print(f"-> PARSED AST:\n{ast}\n")
                if ast is not None:
                    ast_print = AstPrinter().print(ast)
                    # print(f"-> PRETTY-PRINTED AST:\n{ast_print}\n")
                    print(ast_print)
            except (ParseError, Exception):
                exit(65)

    exit()

if __name__ == "__main__":
    main()
