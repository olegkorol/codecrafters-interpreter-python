import sys
from app.grammar.expressions import Expr
from app.grammar.statements import Stmt
from app.utils import pretty_print, LoxRuntimeError
from app.scanner import Scanner
from app.parser import Parser, ParseError
from app.ast_printer import AstPrinter
from app.interpreter import Interpreter

def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <tokenize | parse> <filename>", file=sys.stderr)
        exit(64)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in ["tokenize", "parse", "evaluate", "interpret", "run"]:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(64)

    with open(filename) as file:
        file_contents = file.read()

    match command:
        case "tokenize":
            Scanner(file_contents, print_to_stdout=True).tokenize()
        case "parse":
            try:
                tokens = Scanner(file_contents, print_to_stdout=False).tokenize()
                parser = Parser(tokens)
                ast: Expr = parser.parse_expr()
                if ast is not None:
                    print(AstPrinter().print(ast))
            except (ParseError):
                exit(65)
        case "evaluate": # Only for single-line expressions (no statements)
            try:
                tokens = Scanner(file_contents, print_to_stdout=False).tokenize()
                parser = Parser(tokens)
                ast: Expr = parser.parse_expr()
                print(pretty_print(Interpreter().evaluate(ast)))
            except LoxRuntimeError as error:
                print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
                exit(70)
            except ParseError:
                exit(65)
        case "run":
            try:
                tokens = Scanner(file_contents, print_to_stdout=False).tokenize()
                statements: list[Stmt] = Parser(tokens).parse()
                Interpreter().interpret(statements)
            except LoxRuntimeError as error:
                print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
                exit(70)
            except ParseError:
                exit(65)

    exit()

if __name__ == "__main__":
    main()
