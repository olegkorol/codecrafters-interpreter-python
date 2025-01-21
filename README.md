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

## Usage

Write your code in e.g. `test.lox` and run it with:

```sh
./lox.sh run test.lox
```
