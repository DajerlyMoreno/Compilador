from automata.fa.nfa import NFA
import re
import sys
import os

# Importar los componentes de Octave
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
from core.octave_lexer import lexer
from core.octave_parser import parser, limpiar_mensajes as limpiar_parser, obtener_mensajes as obtener_parser
from core.analisis_semantico import analisis_semantico, limpiar as limpiar_semantico, obtener as obtener_semantico

class MealyTokenizer:
    def __init__(self):
        # Estados de la máquina de Mealy
        self.states = {
            'INICIAL',
            'EN_IDENTIFICADOR', 
            'EN_NUMERO',
            'EN_STRING_DOBLE',
            'EN_STRING_SIMPLE',
            'EN_OPERADOR',
            'EN_COMENTARIO'
        }
        
        # Definir transiciones y salidas
        self.transitions = {
            'INICIAL': {
                'letra': ('EN_IDENTIFICADOR', 'ACUMULAR'),
                'digito': ('EN_NUMERO', 'ACUMULAR'),
                '"': ('EN_STRING_DOBLE', 'ACUMULAR'),
                "'": ('EN_STRING_SIMPLE', 'ACUMULAR'),
                '=': ('EN_OPERADOR', 'ACUMULAR'),
                '!': ('EN_OPERADOR', 'ACUMULAR'),
                '<': ('EN_OPERADOR', 'ACUMULAR'),
                '>': ('EN_OPERADOR', 'ACUMULAR'),
                '&': ('EN_OPERADOR', 'ACUMULAR'),
                '|': ('EN_OPERADOR', 'ACUMULAR'),
                '+': ('INICIAL', 'EMITIR_SIMPLE'),
                '-': ('INICIAL', 'EMITIR_SIMPLE'),
                '*': ('INICIAL', 'EMITIR_SIMPLE'),
                '/': ('INICIAL', 'EMITIR_SIMPLE'),
                '(': ('INICIAL', 'EMITIR_SIMPLE'),
                ')': ('INICIAL', 'EMITIR_SIMPLE'),
                ';': ('INICIAL', 'EMITIR_SIMPLE'),
                'espacio': ('INICIAL', 'IGNORAR'),
                'newline': ('INICIAL', 'IGNORAR'),
                'tab': ('INICIAL', 'IGNORAR')
            },
            'EN_IDENTIFICADOR': {
                'letra': ('EN_IDENTIFICADOR', 'ACUMULAR'),
                'digito': ('EN_IDENTIFICADOR', 'ACUMULAR'),
                '_': ('EN_IDENTIFICADOR', 'ACUMULAR'),
                'otro': ('INICIAL', 'EMITIR_ID_Y_PROCESAR')
            },
            'EN_NUMERO': {
                'digito': ('EN_NUMERO', 'ACUMULAR'),
                'otro': ('INICIAL', 'EMITIR_NUM_Y_PROCESAR')
            },
            'EN_STRING_DOBLE': {
                '"': ('INICIAL', 'EMITIR_STRING'),
                'otro': ('EN_STRING_DOBLE', 'ACUMULAR')
            },
            'EN_STRING_SIMPLE': {
                "'": ('INICIAL', 'EMITIR_STRING'),
                'otro': ('EN_STRING_SIMPLE', 'ACUMULAR')
            },
            'EN_OPERADOR': {
                '=': ('INICIAL', 'EMITIR_OP_DOBLE'),
                '&': ('INICIAL', 'EMITIR_OP_DOBLE'),
                '|': ('INICIAL', 'EMITIR_OP_DOBLE'),
                'otro': ('INICIAL', 'EMITIR_OP_Y_PROCESAR')
            }
        }
        
        # Palabras clave
        self.keywords = {'if', 'else', 'end', 'elseif', 'for', 'while', 'disp'}
        
    def clasificar_caracter(self, char):
        """Clasifica un carácter en su categoría correspondiente"""
        if char.isalpha():
            return 'letra'
        elif char.isdigit():
            return 'digito'
        elif char in ' \t':
            return 'espacio'
        elif char == '\n':
            return 'newline'
        elif char == '_':
            return '_'
        elif char == '"':
            return '"'
        elif char == "'":
            return "'"
        elif char in '=!<>&|':
            return char
        elif char in '+-*/();':
            return char
        else:
            return 'otro'
    
    def tokenizar(self, codigo):
        """Tokeniza el código usando la máquina de Mealy"""
        tokens = []
        estado_actual = 'INICIAL'
        buffer = ''
        i = 0
        
        while i < len(codigo):
            char = codigo[i]
            tipo_char = self.clasificar_caracter(char)
            
            # Buscar transición
            transiciones_estado = self.transitions.get(estado_actual, {})
            
            # Buscar transición específica o genérica
            if tipo_char in transiciones_estado:
                nuevo_estado, accion = transiciones_estado[tipo_char]
            elif 'otro' in transiciones_estado:
                nuevo_estado, accion = transiciones_estado['otro']
            else:
                # Transición no válida, saltar carácter
                i += 1
                continue
            
            # Ejecutar acción
            token_emitido = self.ejecutar_accion(accion, char, buffer, tokens)
            
            # Actualizar buffer y estado
            if accion == 'ACUMULAR':
                buffer += char
                i += 1
            elif accion in ['EMITIR_ID_Y_PROCESAR', 'EMITIR_NUM_Y_PROCESAR', 'EMITIR_OP_Y_PROCESAR']:
                buffer = ''
                # No incrementar i, reprocesar el carácter actual
            elif accion in ['EMITIR_SIMPLE', 'EMITIR_STRING', 'EMITIR_OP_DOBLE']:
                buffer = ''
                i += 1
            elif accion == 'IGNORAR':
                i += 1
            else:
                i += 1
                
            estado_actual = nuevo_estado
        
        # Procesar buffer restante
        if buffer:
            if estado_actual == 'EN_IDENTIFICADOR':
                self.emitir_identificador(buffer, tokens)
            elif estado_actual == 'EN_NUMERO':
                tokens.append('num')
            elif estado_actual in ['EN_STRING_DOBLE', 'EN_STRING_SIMPLE']:
                tokens.append('string')
            elif estado_actual == 'EN_OPERADOR':
                tokens.append(buffer)
        
        return tokens
    
    def ejecutar_accion(self, accion, char, buffer, tokens):
        """Ejecuta la acción correspondiente de la máquina de Mealy"""
        if accion == 'ACUMULAR':
            return None
            
        elif accion == 'EMITIR_SIMPLE':
            tokens.append(char)
            return char
            
        elif accion == 'EMITIR_ID_Y_PROCESAR':
            self.emitir_identificador(buffer, tokens)
            return buffer
            
        elif accion == 'EMITIR_NUM_Y_PROCESAR':
            tokens.append('num')
            return 'num'
            
        elif accion == 'EMITIR_STRING':
            tokens.append('string')
            return 'string'
            
        elif accion == 'EMITIR_OP_Y_PROCESAR':
            tokens.append(buffer)
            return buffer
            
        elif accion == 'EMITIR_OP_DOBLE':
            token_doble = buffer + char
            tokens.append(token_doble)
            return token_doble
            
        elif accion == 'IGNORAR':
            return None
            
        return None
    
    def emitir_identificador(self, buffer, tokens):
        """Emite un identificador, verificando si es palabra clave"""
        if buffer in self.keywords:
            tokens.append(buffer)
        else:
            tokens.append('id')

# Instancia global del tokenizador
mealy_tokenizer = MealyTokenizer()

def tokenizar_simple(codigo):
    """Función de interfaz que usa la máquina de Mealy (para compatibilidad)"""
    return mealy_tokenizer.tokenizar(codigo)

# AFN para estructura IF básica
afn_if = NFA(
    states={
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6',
        'q7', 'q8', 'q9', 'q10'
    },
    input_symbols={
        'if', 'elseif', 'else', 'end', '(', ')', ';',
        '==', '!=', '<', '>', '<=', '>=',
        '&&', '||',
        'id', 'num', 'BLOQUE_VALIDO'
    },
    transitions={
        'q0': {'if': {'q1'}},
        'q1': {'(': {'q2'}},
        'q2': {
            'id': {'q3'}, 
            'num': {'q3'}},
        'q3': {
            '==': {'q4'}, 
            '!=': {'q4'}, 
            '<': {'q4'}, 
            '>': {'q4'},
            '<=': {'q4'}, 
            '>=': {'q4'}
        },
        'q4': {
            'id': {'q5'}, 
            'num': {'q5'}
        },
        'q5': {
            '&&': {'q2'}, 
            '||': {'q2'}, 
            ')': {'q6'}
        },
        'q6': {'BLOQUE_VALIDO': {'q7'}},
        'q7': {
            'elseif': {'q1'},
            'else': {'q8'}, 
            'end': {'q10'}
        },
        'q8': {'BLOQUE_VALIDO': {'q9'}},
        'q9': {'end': {'q10'}}
    },
    initial_state='q0',
    final_states={'q10'}
)

def usar_octave_parser(codigo_bloque):
    """
    Usa el parser de Octave para validar un bloque de código
    """
    try:
        # Limpiar mensajes anteriores
        limpiar_parser()
        limpiar_semantico()
        
        # Tokenizar con lexer de Octave
        lexer.input(codigo_bloque)
        
        # Parsear con parser de Octave
        ast = parser.parse(codigo_bloque, lexer=lexer)
        
        # Análisis semántico
        if ast:
            analisis_semantico(ast)
            
        # Verificar si hay errores
        mensajes_parser = obtener_parser()
        mensajes_semantico = obtener_semantico()
        
        errores_parser = [m for m in mensajes_parser if "Error" in m]
        errores_semantico = [m for m in mensajes_semantico if "Error" in m]
        
        if errores_parser or errores_semantico:
            print(f"❌ Errores en el bloque:")
            for error in errores_parser + errores_semantico:
                print(f"  {error}")
            return False
        else:
            print(f"✅ Bloque válido:")
            for mensaje in mensajes_parser + mensajes_semantico:
                print(f"  {mensaje}")
            return True
            
    except Exception as e:
        print(f"❌ Error al procesar bloque: {e}")
        return False

def extraer_bloques_codigo_mejorado(codigo):
    """
    Extrae los bloques de código de una estructura if-elseif-else considerando anidamiento
    VERSIÓN CORREGIDA que maneja correctamente las estructuras anidadas
    """
    bloques = []
    lineas = codigo.split('\n')
    
    # Encontrar todas las posiciones de palabras clave del IF principal
    palabras_clave_principales = []
    nivel_anidamiento = 0
    
    for i, linea in enumerate(lineas):
        linea_limpia = linea.strip()
        
        # Contar niveles de anidamiento
        if re.match(r'\b(if|for|while)\b', linea_limpia):
            if nivel_anidamiento == 0 and linea_limpia.startswith('if('):
                # Es el IF principal
                palabras_clave_principales.append((i, 'if'))
            nivel_anidamiento += 1
        elif linea_limpia.startswith('elseif(') and nivel_anidamiento == 1:
            # Es un ELSEIF del IF principal
            palabras_clave_principales.append((i, 'elseif'))
        elif linea_limpia == 'else' and nivel_anidamiento == 1:
            # Es un ELSE del IF principal
            palabras_clave_principales.append((i, 'else'))
        elif linea_limpia == 'end':
            nivel_anidamiento -= 1
            if nivel_anidamiento == 0:
                # Es el END del IF principal
                palabras_clave_principales.append((i, 'end'))
    
    # Extraer bloques entre palabras clave principales
    for i in range(len(palabras_clave_principales) - 1):
        linea_actual, tipo_actual = palabras_clave_principales[i]
        linea_siguiente, tipo_siguiente = palabras_clave_principales[i + 1]
        
        # Solo procesar if, elseif y else (no end)
        if tipo_actual in ['if', 'elseif', 'else']:
            # Extraer líneas entre la palabra clave actual y la siguiente
            bloque_lineas = []
            for j in range(linea_actual + 1, linea_siguiente):
                if j < len(lineas):
                    linea = lineas[j]
                    if linea.strip():  # Solo agregar líneas no vacías
                        bloque_lineas.append(linea)
            
            if bloque_lineas:
                bloque_codigo = '\n'.join(bloque_lineas)
                bloques.append((tipo_actual, bloque_codigo))
    
    return bloques

def contar_palabras_clave(codigo):
    """
    Cuenta las palabras clave de control de flujo para determinar si hay estructuras anidadas
    """
    palabras = ['for', 'while', 'if', 'end']
    contadores = {}
    
    for palabra in palabras:
        contadores[palabra] = len(re.findall(r'\b' + palabra + r'\b', codigo, re.IGNORECASE))
    
    return contadores

def validar_estructura_balanceada(codigo):
    """
    Valida que las estructuras de control estén balanceadas
    """
    # Contar estructuras de apertura y cierre
    abiertas = 0
    cerradas = 0
    
    lineas = codigo.split('\n')
    for linea in lineas:
        linea_limpia = linea.strip()
        
        # Contar estructuras que abren
        if re.match(r'\b(if|for|while)\b', linea_limpia):
            abiertas += 1
        
        # Contar estructuras que cierran
        if linea_limpia == 'end':
            cerradas += 1
    
    return abiertas == cerradas

def validar_if_con_bloques_anidados(codigo):
    """
    Valida la estructura IF completa con capacidad de reconocer estructuras anidadas
    VERSIÓN CORREGIDA
    """
    print("=== VALIDACIÓN IF CON ESTRUCTURAS ANIDADAS ===")
    
    # 1. Extraer la estructura de control
    estructura_tokens = []
    
    # Buscar if con su condición
    if_match = re.search(r'if\s*\((.*?)\)', codigo, re.DOTALL)
    if if_match:
        condicion = if_match.group(1).strip()
        estructura_tokens.extend(['if', '('])
        # Tokenizar la condición
        cond_tokens = tokenizar_simple(f"dummy ({condicion})")
        estructura_tokens.extend(cond_tokens[2:-1])  # Excluir 'dummy', '(' y último ')'
        estructura_tokens.extend([')', 'BLOQUE_VALIDO'])
    
    # Buscar elseif
    elseif_matches = re.findall(r'elseif\s*\((.*?)\)', codigo, re.DOTALL)
    for condicion in elseif_matches:
        condicion = condicion.strip()
        estructura_tokens.extend(['elseif', '('])
        cond_tokens = tokenizar_simple(f"dummy ({condicion})")
        estructura_tokens.extend(cond_tokens[2:-1])
        estructura_tokens.extend([')', 'BLOQUE_VALIDO'])
    
    # Buscar else
    if re.search(r'\belse\b', codigo):
        estructura_tokens.extend(['else', 'BLOQUE_VALIDO'])
    
    # Buscar end
    if re.search(r'\bend\b', codigo):
        estructura_tokens.append('end')
    
    print(f"Tokens de estructura: {estructura_tokens}")
    
    # 2. Validar estructura con AFN
    try:
        estructura_valida = afn_if.accepts_input(estructura_tokens)
        print(f"¿Estructura de control válida? {estructura_valida}")
        if not estructura_valida:
            return False
    except Exception as e:
        print(f"Error validando estructura: {e}")
        return False
    
    # 3. Extraer y validar bloques de código usando el método corregido
    bloques = extraer_bloques_codigo_mejorado(codigo)
    print(f"Bloques encontrados: {len(bloques)}")
    
    for i, (tipo_bloque, codigo_bloque) in enumerate(bloques):
        print(f"\n--- Validando bloque {i+1} ({tipo_bloque}) ---")
        print(f"Código del bloque:")
        print(codigo_bloque)
        print("---")
        
        # Verificar si el bloque tiene estructuras anidadas
        contadores = contar_palabras_clave(codigo_bloque)
        tiene_estructuras_anidadas = any(count > 0 for palabra, count in contadores.items())
        
        if tiene_estructuras_anidadas:
            print(f"🔍 Bloque contiene estructuras anidadas: {contadores}")
            
            # Validar que las estructuras estén balanceadas
            if validar_estructura_balanceada(codigo_bloque):
                print("✅ Estructuras balanceadas correctamente")
                resultado_bloque = True
            else:
                print("❌ Estructuras desbalanceadas")  
                resultado_bloque = False
        else:
            # Para bloques simples, usar el parser de Octave
            resultado_bloque = usar_octave_parser(codigo_bloque)
        
        if not resultado_bloque:
            print(f"❌ Bloque {i+1} inválido")
            return False
        else:
            print(f"✅ Bloque {i+1} válido")
    
    print("\n✅ Toda la estructura IF es válida")
    return True

def validar_If(cadena):
    """Función original para compatibilidad"""
    tokens = tokenizar_simple(cadena)
    try:
        return afn_if.accepts_input(tokens)
    except Exception:
        return False

def simular_automata(cadena):
    """Simula el autómata paso a paso"""
    afn = afn_if
    tokens = tokenizar_simple(cadena)
    salida = ""

    estados_actuales = {afn.initial_state}
    salida += f"Estado inicial: {estados_actuales}\n"

    for i, simbolo in enumerate(tokens):
        nuevos_estados = set()
        salida += f"\nSímbolo '{simbolo}' (posición {i}):\n"

        for estado in estados_actuales:
            transiciones = afn.transitions.get(estado, {})
            if simbolo in transiciones:
                nuevos_estados.update(transiciones[simbolo])
                salida += f"  {estado} --{simbolo}--> {transiciones[simbolo]}\n"
            else:
                salida += f"  {estado} --{simbolo}--> ❌ (no hay transición)\n"

        if not nuevos_estados:
            salida += "\n❌ No hay transiciones válidas. Cadena rechazada.\n"
            return salida

        estados_actuales = nuevos_estados
        salida += f"Estados actuales: {estados_actuales}\n"

    aceptado = bool(estados_actuales & afn.final_states)
    if aceptado:
        salida += "\n✅ La cadena fue aceptada.\n"
    else:
        salida += f"\n❌ La cadena fue rechazada. Estados finales alcanzados: {estados_actuales}\n"

    return salida

# Función auxiliar para debugging
def debug_tokenizacion(codigo):
    print(f"Código original:\n{repr(codigo)}")
    tokens = tokenizar_simple(codigo)
    print(f"Tokens generados: {tokens}")
    return tokens

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo simple
    codigo_simple = '''
    if(x == 3)
        a = 5;
    else
        d = 10;
    end
    '''
    
    # Ejemplo con estructuras anidadas
    codigo_anidado = '''
    if(x > 5)
        for i = 1:10
            disp(i);
        end
        y = x + 1;
    elseif(x == 3)
        while y < 10
            y = y + 1;
        end
    else
        if z > 0
            disp(z);
        end
    end
    '''
    
    print("=== CÓDIGO SIMPLE ===")
    validar_if_con_bloques_anidados(codigo_simple)
    
    print("\n" + "="*50)
    print("=== CÓDIGO CON ESTRUCTURAS ANIDADAS ===")
    validar_if_con_bloques_anidados(codigo_anidado)