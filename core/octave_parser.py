import ply.yacc as yacc
from octave_lexer import tokens

start = 'program'

# Programa completo: lista de sentencias
def p_program_multiple(p):
    'program : program statement'
    if isinstance(p[1], list):
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1], p[2]]

def p_program_single(p):
    'program : statement'
    p[0] = [p[1]]

# Sentencias
def p_statement_assign(p):
    'statement : ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[3])
    print(f"[SINTAXIS] Asignación válida: {p[1]} = {p[3]}")

def p_statement_expr(p):
    'statement : expression SEMICOLON'
    p[0] = ('statement', p[1])
    print(f"[SINTAXIS] Sentencia válida: {p[1]}")

# Expresiones
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"[SINTAXIS] Error de sintaxis cerca de: '{p.value}'")
    else:
        print("[SINTAXIS] Error de sintaxis inesperado al final del archivo")

# Construcción del parser
parser = yacc.yacc()
