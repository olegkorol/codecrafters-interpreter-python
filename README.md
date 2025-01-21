# PyLox

![image](https://craftinginterpreters.com/image/a-map-of-the-territory/mountain.png)
<sup>*Image from [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom*</sup>

This is a language implementation of the [Lox programming language](https://craftinginterpreters.com/the-lox-language.html), written in Python.
It includes:

- A **lexer** (aka. scanner)
- An AST (Abstract Syntax Tree) **parser**
- A tree-walk **interpreter**

The implementation is based on the book [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom and
was crafted with the help of the unit tests from the ["Build your own Interpreter"](https://app.codecrafters.io/courses/interpreter/overview) challenge by CodeCrafters.

## Grammar

### Program Structure

```text
program        → declaration* EOF ;
```

### Declarations and Statements

```text
declaration    → funDecl
               | varDecl
               | statement ;

funDecl        → "fun" function ;
function       → IDENTIFIER "(" parameters? ")" block ;
parameters     → IDENTIFIER ( "," IDENTIFIER )* ;

varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

statement      → exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block ;

block          → "{" declaration* "}" ;
exprStmt       → expression ";" ;
forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                 expression? ";"
                 expression? ")" statement ;
ifStmt         → "if" "(" expression ")" statement
                 ( "else" statement )? ;
printStmt      → "print" expression ";" ;
returnStmt     → "return" expression? ";" ;
whileStmt      → "while" "(" expression ")" statement ;
```

### Expressions

```text
expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | logic_or ;
logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → equality ( "and" equality )* ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary | call ;
call           → primary ( "(" arguments? ")" )* ;
primary        → NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" | IDENTIFIER ;

arguments      → expression ( "," expression )* ;
```

## Usage

Write your code in e.g. `test.lox` and run it with:

```sh
./lox.sh run test.lox
```
