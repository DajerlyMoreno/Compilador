from octave_lexer import lexer
from octave_parser import parser

# Función para hacer el análisis semántico
def analisis_semantico(arbol):
    print("\n=== ANÁLISIS SEMÁNTICO ===")

    if not arbol:
        print("[SEMÁNTICA] Error: No se pudo generar el árbol sintáctico.")
        return

    tabla_simbolos = {}

    def recorrer(nodo):
        if nodo is None or not isinstance(nodo, tuple):
            return None

        tipo = nodo[0]

        if tipo == 'assign':
            nombre_var = nodo[1]
            expresion = nodo[2]
            tipo_expr = recorrer(expresion)
            tabla_simbolos[nombre_var] = tipo_expr
            print(f"[SEMÁNTICA] Variable '{nombre_var}' declarada como tipo: {tipo_expr}")
            return tipo_expr

        elif tipo == 'statement':
            return recorrer(nodo[1])

        elif tipo == 'if' or tipo == 'while':
            condicion = nodo[1]
            cuerpo = nodo[2]
            print(f"[DEBUG] Nodo {tipo.upper()}: condición={condicion}, cuerpo={cuerpo}")
        
            tipo_cond = recorrer(condicion)
            
            print(f"[DEBUG] Tipo de condición evaluado: {tipo_cond}")
            
            if tipo_cond != 'boolean':
                print(f"[SEMÁNTICA] Error: Condición en '{tipo}' no es booleana, encontrado: {tipo_cond}")
            
            if isinstance(cuerpo, list):
                print(f"[DEBUG] Procesando cuerpo de {tipo} como lista con {len(cuerpo)} elementos")
                for i, sentencia in enumerate(cuerpo):
                    print(f"[DEBUG] Procesando sentencia {i} en {tipo}: {sentencia}")
                    recorrer(sentencia)
            elif cuerpo is not None:
                print(f"[DEBUG] Procesando cuerpo de {tipo} como nodo único: {cuerpo}")
                recorrer(cuerpo)

        elif tipo == 'for':
            var = nodo[1]
            inicio = nodo[2]
            fin = nodo[3]
            cuerpo = nodo[4] 
            
            tipo_inicio = recorrer(inicio)
            tipo_fin = recorrer(fin)
            tabla_simbolos[var] = 'number'
            print(f"[SEMÁNTICA] Variable de bucle '{var}' declarada como tipo: number")
            
            if isinstance(cuerpo, list):
                for i, sentencia in enumerate(cuerpo):
                    recorrer(sentencia)
            elif isinstance(cuerpo, tuple):
                recorrer(cuerpo)
            elif cuerpo is not None:
                recorrer(cuerpo)
            else:
                print(f"[DEBUG] Cuerpo del for es None")

        elif tipo == 'disp':
            return recorrer(nodo[1])

        elif tipo == 'binop':
            operador = nodo[1]
            izquierda = recorrer(nodo[2])
            derecha = recorrer(nodo[3])

            print(f"[DEBUG] Operación binaria: {operador}, izq: {izquierda}, der: {derecha}")

            if operador in ['+', '-', '*', '/', ':']:
                if izquierda == 'number' and derecha == 'number':
                    return 'number'
                else:
                    print(f"[SEMÁNTICA] Error: Operación '{operador}' requiere números.")
                    return None

            elif operador in ['>', '<', '==', '<=', '>=', '!=']:  # Agregué <= y otros
                if izquierda == 'number' and derecha == 'number':
                    return 'boolean'
                else:
                    print(f"[SEMÁNTICA] Error: Comparación '{operador}' requiere números.")
                    return None

            elif operador == '&&' or operador == '||':
                if izquierda != 'boolean':
                    print(f"[SEMÁNTICA] Error: Operando izquierdo de '{operador}' debe ser booleano, no {izquierda}.")
                    return None
                if derecha != 'boolean':
                    print(f"[SEMÁNTICA] Error: Operando derecho de '{operador}' debe ser booleano, no {derecha}.")
                    return None
                return 'boolean'

        elif tipo == 'not':
            subexpr = recorrer(nodo[1])
            if subexpr != 'boolean':
                print("[SEMÁNTICA] Error: Operador '!' requiere expresión booleana.")
            return 'boolean'

        elif tipo == 'id':
            nombre = nodo[1]
            print(f"[DEBUG] Buscando variable '{nombre}' en tabla: {tabla_simbolos}")
            if nombre not in tabla_simbolos:
                print(f"[SEMÁNTICA] Error: Variable '{nombre}' usada sin declarar.")
                return None
            return tabla_simbolos[nombre]

        elif tipo == 'number':
            return 'number'

        elif tipo == 'string':
            return 'string'

        return None

    # CAMBIO PRINCIPAL: Procesar en el orden correcto
    if isinstance(arbol, list):
        for stmt in arbol:
            print(f"[DEBUG] Procesando statement: {stmt}")
            recorrer(stmt)
    else:
        recorrer(arbol)
    
    print(f"[DEBUG] Tabla de símbolos final: {tabla_simbolos}")


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

codigo = """
i = 1;
for i = 1:10
    disp(i);
end
"""

analizar_codigo(codigo)