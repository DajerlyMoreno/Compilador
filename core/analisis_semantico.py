mensajes_semantica = []

def analisis_semantico(arbol):
    if not arbol:
        agregar("[SEMÁNTICA] Error: No se pudo generar el árbol sintáctico.")
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
            agregar(f"[SEMÁNTICA] Variable '{nombre_var}' declarada como tipo: {tipo_expr}")
            return tipo_expr

        elif tipo == 'statement':
            return recorrer(nodo[1])

        elif tipo == 'if' or tipo == 'while':
            condicion = nodo[1]
            cuerpo = nodo[2]
            
            tipo_cond = recorrer(condicion)
            if tipo_cond != 'boolean':
                agregar(f"[SEMÁNTICA] Error: Condición en '{tipo}' no es booleana, encontrado: {tipo_cond}")
            
            if isinstance(cuerpo, list):
                for sentencia in cuerpo:
                    recorrer(sentencia)
            elif cuerpo is not None:
                recorrer(cuerpo)

        elif tipo == 'for':
            var = nodo[1]
            inicio = nodo[2]
            fin = nodo[3]
            cuerpo = nodo[4]
            
            tipo_inicio = recorrer(inicio)
            tipo_fin = recorrer(fin)
            
            if tipo_inicio != 'number' or tipo_fin != 'number':
                agregar("[SEMÁNTICA] Error: El rango del bucle 'for' debe ser numérico.")

            tabla_simbolos[var] = 'number'
            agregar(f"[SEMÁNTICA] Variable de bucle '{var}' declarada implícitamente como tipo: number")
            
            if isinstance(cuerpo, list):
                for sentencia in cuerpo:
                    recorrer(sentencia)
            elif cuerpo is not None:
                recorrer(cuerpo)

        elif tipo == 'disp':
            tipo_expr = recorrer(nodo[1])
            agregar(f"[SEMÁNTICA] Función 'disp' llamada correctamente con parámetro tipo: {tipo_expr}")
            return tipo_expr

        elif tipo == 'binop':
            operador = nodo[1]
            izquierda = recorrer(nodo[2])
            derecha = recorrer(nodo[3])

            if operador in ['+', '-', '*', '/', ':']:
                if izquierda == 'number' and derecha == 'number':
                    return 'number'
                else:
                    agregar(f"[SEMÁNTICA] Error: Operación '{operador}' requiere operandos numéricos.")
                    return None

            elif operador in ['>', '<', '==', '<=', '>=', '!=']:
                if izquierda == 'number' and derecha == 'number':
                    return 'boolean'
                else:
                    agregar(f"[SEMÁNTICA] Error: Comparación '{operador}' requiere operandos numéricos.")
                    return None

            elif operador in ['&&', '||']:
                if izquierda != 'boolean' or derecha != 'boolean':
                    agregar(f"[SEMÁNTICA] Error: Operación lógica '{operador}' requiere operandos booleanos.")
                    return None
                return 'boolean'

        elif tipo == 'not':
            subexpr = recorrer(nodo[1])
            if subexpr != 'boolean':
                agregar("[SEMÁNTICA] Error: Operador '!' requiere expresión booleana.")
            return 'boolean'

        elif tipo == 'id':
            nombre = nodo[1]
            if nombre not in tabla_simbolos:
                agregar(f"[SEMÁNTICA] Error: Variable '{nombre}' usada sin declarar.")
                return None
            return tabla_simbolos[nombre]

        elif tipo == 'number':
            return 'number'

        elif tipo == 'string':
            return 'string'

        return None

    if isinstance(arbol, list):
        for stmt in arbol:
            recorrer(stmt)
    else:
        recorrer(arbol)

    agregar("[SEMÁNTICA] Análisis semántico completado correctamente.")

def limpiar():
    global mensajes_semantica
    mensajes_semantica = []

def agregar(mensaje):
    global mensajes_semantica
    mensajes_semantica.append(mensaje)
    return mensaje

def obtener():
    global mensajes_semantica
    return mensajes_semantica
