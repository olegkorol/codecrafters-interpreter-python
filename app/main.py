import sys
from app.tokenizer import Tokenizer
from app.parser import AstPrinter, Parser, ParseError
from app.interpreter import Interpreter, pretty_print, LoxRuntimeError





def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <tokenize | parse> <filename>", file=sys.stderr)
        exit(64)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse", "evaluate", "interpret"]:
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
                # print(f"-> SCANNED TOKENS:\n\n{tokens}\n")
                ast = Parser(tokens).parse()
                # print(f"-> PARSED AST:\n\n{ast}\n")
                if ast is not None:
                    ast_print = AstPrinter().print(ast)
                    # print(f"-> PRETTY-PRINTED AST:\n\n{ast_print}\n")
                    print(ast_print)
            except (ParseError, Exception):
                exit(65)
        case "evaluate":
            try:
                tokens = Tokenizer(file_contents, print_to_stdout=False).tokenize()
                ast = Parser(tokens).parse()
                Interpreter().interpret(ast)
            except LoxRuntimeError as error:
                print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
                exit(70)

    exit()

if __name__ == "__main__":
    main()
