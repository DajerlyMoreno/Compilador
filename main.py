from octave_lexer import lexer
from octave_parser import parser

# Función para hacer el análisis semántico
def analisis_semantico(arbol):
    print("\n=== ANÁLISIS SEMÁNTICO ===")
    variables_declaradas = set()

    def recorrer(nodo):
        if nodo is None:
            return

        tipo = nodo[0]

        if tipo == 'assign':
            nombre_var = nodo[1]
            expresion = nodo[2]

            # Primero revisamos la expresión
            recorrer(expresion)

            # Luego registramos la variable como declarada
            variables_declaradas.add(nombre_var)

        elif tipo == 'statement':
            recorrer(nodo[1])

        elif tipo == 'binop':
            recorrer(nodo[2])
            recorrer(nodo[3])

        elif tipo == 'id':
            nombre = nodo[1]
            if nombre not in variables_declaradas:
                print(f"[SEMÁNTICA] Error: Variable '{nombre}' usada sin declarar.")

        elif tipo == 'number':
            pass

    # Si es una lista de sentencias, recorrer todas
    if isinstance(arbol, list):
        for stmt in arbol:
            recorrer(stmt)
    else:
        recorrer(arbol)


# Función principal de análisis
def analizar_codigo(codigo):
    print("=== ANÁLISIS LÉXICO ===")
    lexer.input(codigo)
    for tok in lexer:
        print(f"{tok.type}: {tok.value}")

    print("\n=== ANÁLISIS SINTÁCTICO ===")
    resultado = parser.parse(codigo)

    if resultado:
        print("[SINTAXIS] Árbol sintáctico:", resultado)
        analisis_semantico(resultado)
    else:
        print("[SINTAXIS] Error: No se pudo generar el árbol.")

# Código de ejemplo (puedes reemplazarlo por lectura desde archivo si deseas)
codigo = """
a = 5 + 3;
b = a * 2;
"""

analizar_codigo(codigo)
