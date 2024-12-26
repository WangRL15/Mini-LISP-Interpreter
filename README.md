I'll help you convert that content into Markdown format. Here's the README.md version:

# Mini-LISP Interpreter

Final project for the Compilers course at National Central University, Fall 2023.

## Documents

- [Compiler Final Project Requirements](./docs/Compiler%20Final%20Project.pdf)
- [Mini-LISP Language Specification](./docs/MiniLisp.pdf)

## Development

- **Operating System**: Mac OS M2
- **Language**: Python

## Features

### Basic Features

**Important**: Features 1-4 must be finished before other features.

| Feature | Description | Points | Public | Hidden
|---------|-------------|---------|---------|---------|
| Syntax Validation | Print "syntax error" when parsing invalid syntax | 10 | ✅ | ✅ | 
| Print | Implement print-num statement | 10 | ✅ | ✅ | 
| Numerical Operations | Implement all numerical operations | 25 | ✅ | ✅ |
| Logical Operations | Implement all logical operations | 25 | ✅ | ✅ | 
| if Expression | Implement if expression | 8 | ✅ | ✅ |
| Variable Definition | Able to define a variable | 8 | ✅ | ✅ |
| Function | Able to declare and call an anonymous function | 8 | ✅ | ✅ |
| Named Function | Able to declare and call a named function | 6 | ✅ | ✅ | 


## Usage


### Run Test

Script Features:

- Compile, execute tests, and clear output files
- Count the number of test cases passed and failed
- Display expected and actual outputs for failed test cases

Execution Method:

```bash
./run_test.sh
```

If encountering issues like permission error, try modifying script permissions:

```bash
chmod +x run_tests.sh
```
