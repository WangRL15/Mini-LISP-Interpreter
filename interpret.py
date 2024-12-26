import sys
import ply.lex as lex
import ply.yacc as yacc

# ---- LEXICAL ANALYZER ----
# Reserved words
reserved = {
    'mod': 'MOD',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'define': 'DEFINE',
    'fun': 'FUN',
    'if': 'IF',
    'print-num': 'PRINTNUM',
    'print-bool': 'PRINTBOOL'
}

# Update tokens
tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'GREATER', 'LESS', 'EQUAL',
    'LPAREN', 'RPAREN',
    'NUMBER', 'BOOLEAN', 'ID'
] + list(reserved.values())

# Define literals
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_GREATER   = r'>'
t_LESS      = r'<'
t_EQUAL     = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

class SyntaxError(Exception):
    pass

# Regular expressions for tokens
def t_NUMBER(t):
    r'-?(0|[1-9][0-9]*)'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'\#t|\#f'
    t.value = True if t.value == '#t' else False
    return t

def t_ID(t):
    r'[a-z][a-z0-9-]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}'")

lexer = lex.lex()

# ---- PARSER ----
def p_program(p):
    '''program : statement
               | statement program'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_statement(p):
    '''statement : expression
                 | define_statement
                 | print_statement'''
    p[0] = p[1]

def p_expression(p):
    '''expression : NUMBER
                  | BOOLEAN
                  | ID
                  | numerical_op
                  | logical_op
                  | comparison_op
                  | function_exp
                  | function_call
                  | if_expression'''
    p[0] = p[1]

def p_define_statement(p):
    '''define_statement : LPAREN DEFINE ID expression RPAREN'''
    p[0] = ('define', p[3], p[4])

# --Print Implement--
def p_print_statement(p):
    '''print_statement : LPAREN PRINTNUM expression RPAREN
                       | LPAREN PRINTBOOL expression RPAREN'''
    p[0] = ('print', p[2], p[3])

# --Validation--
# check count of parameter
# raise error if it parameters do not match
def validate_args_count(args, min_args, max_args=None, op_name=""):
    if max_args is None:
        max_args = min_args
    count = len(args) if args else 0
    if count < min_args:
        raise SyntaxError(f"Need {min_args} arguments, but got {count}.")
    if max_args != -1 and count > max_args:  # -1 表示無上限
        raise SyntaxError(f"Expected {max_args} arguments, but got {count}.")

# --Numerical Operations--
def p_numerical_op(p):
    '''numerical_op : LPAREN PLUS expression_list RPAREN
                    | LPAREN MINUS expression expression RPAREN
                    | LPAREN TIMES expression_list RPAREN
                    | LPAREN DIVIDE expression expression RPAREN
                    | LPAREN MOD expression expression RPAREN'''
    # setting AST
    if p[2] == '+':
        validate_args_count(p[3], 2, -1, "+")  # -1 表示無上限
        p[0] = ('+', p[3])
    elif p[2] == '-':
        validate_args_count([p[3], p[4]], 2, 2, "-")
        p[0] = ('-', p[3], p[4])
    elif p[2] == '*':
        validate_args_count(p[3], 2, -1, "*")
        p[0] = ('*', p[3])
    elif p[2] == '/':
        validate_args_count([p[3], p[4]], 2, 2, "/")
        p[0] = ('/', p[3], p[4])
    elif p[2] == 'mod':
        validate_args_count([p[3], p[4]], 2, 2, "mod")
        p[0] = ('mod', p[3], p[4])

# --Logical Operations--
def p_logical_op(p):
    '''logical_op : LPAREN AND expression_list RPAREN
                  | LPAREN OR expression_list RPAREN
                  | LPAREN NOT expression RPAREN'''
    if p[2] in ['and', 'or']:
        validate_args_count(p[3], 2, -1, p[2])
        p[0] = (p[2], p[3])
    elif p[2] == 'not':
        validate_args_count([p[3]], 1, 1, "not")
        p[0] = ('not', p[3])

# --Comparison Operations--
def p_comparison_op(p):
    '''comparison_op : LPAREN GREATER expression expression RPAREN
                     | LPAREN LESS expression expression RPAREN
                     | LPAREN EQUAL expression_list RPAREN'''
    if p[2] == '=':
        validate_args_count(p[3], 2, -1, "=")
        p[0] = ('=', p[3])
    else:
        validate_args_count([p[3], p[4]], 2, 2, p[2])
        p[0] = (p[2], p[3], p[4])

def p_expression_list(p):
    '''expression_list : 
                       | expression
                       | expression expression_list'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

# --Declare and Call an Anonymous Function--
# ('fun', param_exprs, body_exprs)
def p_function_exp(p):
    '''function_exp : LPAREN FUN LPAREN expression_list RPAREN expression_list RPAREN'''
    p[0] = ('fun', p[4], p[6])

# --Declare and Call a Nameed Function--
# ('call', fun_exp | ID, exprs)
def p_function_call(p):
    '''function_call : LPAREN function_exp expression_list RPAREN
                     | LPAREN ID expression_list RPAREN'''
    p[0] = ('call', p[2], p[3])

# --If Expression--
# ('if', condiction, if_exprs, else_exprs)
def p_if_expression(p):
    '''if_expression : LPAREN IF expression expression expression RPAREN'''
    p[0] = ('if', p[3], p[4], p[5])

# --Validation--
# raise error when input invalid grammer
def p_error(p):
    if p is None:
        raise SyntaxError("Unexpected end of file")
    raise SyntaxError(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

# ---- INTERPRETER ----
def evaluate(node, local_vars=None):
    """Evaluate an expression."""
    # save defined ID and Function
    global variables
    
    current_scope = variables.copy()
    if local_vars:
        current_scope.update(local_vars)

    # Number or Boolean
    if isinstance(node, int) or isinstance(node, bool):
        return node
    elif isinstance(node, str):
        # check if variable is defined(in the current scope)
        if node not in current_scope:
            raise SyntaxError(f"Variable {node} not defined")
        return current_scope[node]
    elif isinstance(node, tuple):
        if node[0] in ['+', '*']:
            return sum(evaluate(x, local_vars) for x in node[1]) if node[0] == '+' else prod(evaluate(x, local_vars) for x in node[1])
        elif node[0] == '-':
            return evaluate(node[1], local_vars) - evaluate(node[2], local_vars)
        elif node[0] == '/':
            denominator = evaluate(node[2], local_vars)
            if denominator == 0:
                raise SyntaxError("Division by zero")
            return evaluate(node[1], local_vars) // evaluate(node[2], local_vars)
        elif node[0] == 'mod':
            denominator = evaluate(node[2], local_vars)
            if denominator == 0:
                raise SyntaxError("Division by zero in modulo")
            return evaluate(node[1], local_vars) % evaluate(node[2], local_vars)
        elif node[0] == '<':
            return evaluate(node[1], local_vars) < evaluate(node[2], local_vars)
        elif node[0] == '>':
            return evaluate(node[1], local_vars) > evaluate(node[2], local_vars)
        elif node[0] == '=':
            values = [evaluate(x, local_vars) for x in node[1]]
            return all(v == values[0] for v in values)
        elif node[0] == 'and':
            return all(evaluate(x, local_vars) for x in node[1])
        elif node[0] == 'or':
            return any(evaluate(x, local_vars) for x in node[1])
        elif node[0] == 'not':
            return not evaluate(node[1], local_vars)
        elif node[0] == 'if':
            condition = evaluate(node[1], local_vars)
            return evaluate(node[2], local_vars) if condition else evaluate(node[3], local_vars)
        elif node[0] == 'fun':
            return node
        elif node[0] == 'call':
            # get function node
            func = evaluate(node[1], local_vars)
            if func and func[0] == 'fun':
                # function
                params, body = func[1], func[2]
                # raise error when count of function params does not match the params
                if len(params) != len(node[2]):
                    raise SyntaxError(f"Function expects {len(params)} arguments, but got {len(node[2])}")
                # mapping params to real number
                local_scope = {params[i]: evaluate(arg, local_vars) for i, arg in enumerate(node[2])}
                return evaluate(body[0], local_scope)
            else:
                raise SyntaxError(f"Invalid function call: {node}")

def interpret(ast):
    """Interpret the parsed AST."""
    if not ast:
        return
    for stmt in ast:
        execute(stmt)

def execute(node):
    """Execute a single AST node."""
    if isinstance(node, tuple) and node[0] in ['define', 'print']:
        if node[0] == 'define':
            variables[node[1]] = evaluate(node[2])
        elif node[0] == 'print':
            if node[1] == 'print-num':
                print(evaluate(node[2]))
            elif node[1] == 'print-bool':
                print('#t' if evaluate(node[2]) else '#f')
    else:
        return evaluate(node)

def prod(iterable):
    """Helper function to calculate product of an iterable."""
    result = 1
    for x in iterable:
        result *= x
    return result

variables = {}

# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    try:
        data = sys.stdin.read()
        if not data.strip():
            sys.exit(0)
        # print(f"Input:\n{data}")
        try:
            result = parser.parse(data)
            interpret(result)
        # catch all SyntaxError and output syntax error
        except SyntaxError as e:
            print(f"syntax error: {str(e)}")
    except Exception as e:
        print(f"syntax error: {str(e)}")
