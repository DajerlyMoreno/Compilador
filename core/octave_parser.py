import ply.yacc as yacc
from .octave_lexer import tokens

start = 'program'

# Lista global para capturar mensajes
mensajes_sintaxis = []

def limpiar_mensajes():
    """Función para limpiar los mensajes antes de cada análisis"""
    global mensajes_sintaxis
    mensajes_sintaxis = []

def agregar_mensaje(mensaje):
    """Función para agregar un mensaje a la lista"""
    global mensajes_sintaxis
    mensajes_sintaxis.append(mensaje)
    return mensaje

def obtener_mensajes():
    """Función para obtener todos los mensajes acumulados"""
    global mensajes_sintaxis
    return '\n'.join(mensajes_sintaxis)

def p_program(p):
    'program : statement_list'
    if len(p) == 2:
        p[0] = p[1]
        agregar_mensaje("[SINTAXIS] Programa analizado correctamente")
    else:
        p[0] = []
        agregar_mensaje("[SINTAXIS] Programa vacío o incompleto")

def p_statement_list_multiple(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]

def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = [p[1]]

def p_statement_if(p):
    'statement : IF expression statement END'
    p[0] = ('if', p[2], p[3])
    agregar_mensaje(f"[SINTAXIS] Sentencia if válida con condición: {p[2]}")

def p_statement_for(p):
    'statement : FOR ID EQUALS expression DOSPUNTOS expression statement_list END'
    if len(p) == 8:
        p[0] = ('for', p[2], p[4], p[6], p[7])
        agregar_mensaje(f"[SINTAXIS] Sentencia for válida: {p[2]} desde {p[4]} hasta {p[6]}") 
    else:
        agregar_mensaje(f"[SINTAXIS] Sentencia for incompleta")

def p_statement_while(p):
    'statement : WHILE expression statement_list END'
    p[0] = ('while', p[2], p[3])
    agregar_mensaje(f"[SINTAXIS] Sentencia while válida con condición: {p[2]}")

def p_statement_disp(p):
    '''statement : DISP LPAREN expression RPAREN SEMICOLON
                 | DISP LPAREN expression RPAREN'''
    p[0] = ('disp', p[3])
    return agregar_mensaje(f"[SINTAXIS] Llamada a disp válida con: {p[3]}")

# Sentencias
def p_statement_assign(p):
    '''statement : ID EQUALS expression SEMICOLON
                 | ID EQUALS expression'''
    p[0] = ('assign', p[1], p[3])
    return agregar_mensaje(f"[SINTAXIS] Asignación válida: {p[1]} = {p[3]}")

def p_statement_expr(p):
    '''statement : expression SEMICOLON 
                 | expression'''
    p[0] = ('statement', p[1])
    return agregar_mensaje(f"[SINTAXIS] Sentencia válida: {p[1]}")

# Expresiones
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression DOUBLE_EQUALS expression
                  | expression GREATER_EQUALS expression
                  | expression LESS_EQUALS expression
                  | expression AND expression
                  | expression OR expression
                  | expression DOSPUNTOS expression'''
    p[0] = ('binop', p[2], p[1], p[3])
    return agregar_mensaje(f"[SINTAXIS] Operación binaria válida: {p[1]} {p[2]} {p[3]}")

def p_expression_cadena(p):
    '''expression : CADENA'''
    p[0] = ('string', p[1])
    return agregar_mensaje(f"[SINTAXIS] Cadena válida: {p[1]}")

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('not', p[2])
    return agregar_mensaje(f"[SINTAXIS] Operación NOT válida: !{p[2]}")

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]
    return agregar_mensaje(f"[SINTAXIS] Expresión agrupada válida: ({p[2]})")

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])
    return agregar_mensaje(f"[SINTAXIS] Número válido: {p[1]}")

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])
    return agregar_mensaje(f"[SINTAXIS] Identificador válido: {p[1]}")

# Manejo de errores sintácticos
def p_error(p):
    if p:
        error_msg = f"[SINTAXIS] Error de sintaxis cerca de: '{p.value}'"
        agregar_mensaje(error_msg)
        return error_msg
    else:
        error_msg = "[SINTAXIS] Error de sintaxis inesperado al final del archivo"
        agregar_mensaje(error_msg)
        return error_msg

# Construcción del parser
parser = yacc.yacc()

