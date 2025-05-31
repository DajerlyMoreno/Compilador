import ply.lex as lex

tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN', 'SEMICOLON', 'DOSPUNTOS',
    'IF', 'WHILE', 'FOR', 'GREATER', 'LESS',
    'SQUOTE', 'CADENA', 'DQUOTE',
    'AND', 'OR', 'NOT', 'LESS_EQUALS', 'GREATER_EQUALS',
    'DOUBLE_EQUALS',     
    'END',          
    'DISP',             
    'COMMA', 'TRUE', 'FALSE', 'NULL'         
]

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_DOUBLE_EQUALS = r'=='
t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOLON = r';'
t_GREATER = r'>'
t_LESS    = r'<'
t_SQUOTE  = r'\''
t_DQUOTE  = r'"'
t_END    = r'end'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_NOT     = r'!'
t_COMMA   = r','
t_DOSPUNTOS = r':' 

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() == 'if':
        t.type = 'IF'
    elif t.value.lower() == 'while':
        t.type = 'WHILE'
    elif t.value.lower() == 'end':
        t.type = 'END'
    elif t.value.lower() == 'disp':
        t.type = 'DISP'
    elif t.value.lower() == 'for':
        t.type = 'FOR'
    elif t.value.lower() == 'true':
        t.type = 'TRUE'
    elif t.value.lower() == 'false':
        t.type = 'FALSE'
    elif t.value.lower() == 'null':
        t.type = 'NULL'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_CADENA(t):
    r'"[^"]*"'
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"[LÉXICO] Token no válido: {t.value[0]}")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()
