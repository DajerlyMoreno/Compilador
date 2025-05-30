from automata.fa.nfa import NFA
import re
from afn_Asignacion import validar_asignacion

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
        self.keywords = {'if', 'else', 'end', 'elseif'}
        
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

def tokenizar(codigo):
    """Función de interfaz que usa la máquina de Mealy"""
    return mealy_tokenizer.tokenizar(codigo)

# El resto del código permanece igual
afn_if = NFA(
    states={
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6',
        'q7', 'q8', 'q9', 'q10'
    },
    input_symbols={
        'if', 'elseif', 'else', 'end', '(', ')', ';',
        '==', '!=', '<', '>', '<=', '>=',
        '&&', '||',
        'id', 'num'
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
        'q6': {';': {'q7'}},
        'q7': {
            'elseif': {'q1'},
            'else': {'q8'}, 
            'end': {'q10'}
        },
        'q8': {';': {'q9'}},
        'q9': {'end': {'q10'}}
    },
    initial_state='q0',
    final_states={'q10'}
)

def validar_If(cadena):
    tokens = tokenizar(cadena)
    try:
        return afn_if.accepts_input(tokens)
    except Exception:
        return False

def extraer_asignaciones(codigo):
    """
    Extrae todas las asignaciones del código, excluyendo las palabras clave de control.
    """
    # Remover las palabras clave de control y sus paréntesis
    codigo_sin_control = re.sub(r'\b(if|elseif|else|end)\b.*?\)', '', codigo)
    codigo_sin_control = re.sub(r'\b(else|end)\b', '', codigo_sin_control)
    
    # Dividir por punto y coma y filtrar líneas vacías
    lineas = [linea.strip() for linea in codigo_sin_control.split(';') if linea.strip()]
    
    # Filtrar solo las que parecen asignaciones (contienen =)
    asignaciones = [linea for linea in lineas if '=' in linea and not linea.startswith('if') and not linea.startswith('elseif')]
    
    return asignaciones

def validar_if_con_bloque(codigo):
    
    # 1. Validar la estructura de control
    # Extraer solo la estructura if-elseif-else-end
    estructura_tokens = []
    
    # Buscar if con su condición
    if_match = re.search(r'if\s*\((.*?)\)', codigo, re.DOTALL)
    if if_match:
        condicion = if_match.group(1).strip()
        estructura_tokens.extend(['if', '('])
        # Tokenizar la condición
        cond_tokens = tokenizar(f"dummy ({condicion})")
        estructura_tokens.extend(cond_tokens[2:-1])  # Excluir 'dummy', '(' y último ')'
        estructura_tokens.extend([')', ';'])
    
    # Buscar elseif
    elseif_matches = re.findall(r'elseif\s*\((.*?)\)', codigo, re.DOTALL)
    for condicion in elseif_matches:
        condicion = condicion.strip()
        estructura_tokens.extend(['elseif', '('])
        cond_tokens = tokenizar(f"dummy ({condicion})")
        estructura_tokens.extend(cond_tokens[2:-1])
        estructura_tokens.extend([')', ';'])
    
    # Buscar else
    if re.search(r'\belse\b', codigo):
        estructura_tokens.extend(['else', ';'])
    
    # Buscar end
    if re.search(r'\bend\b', codigo):
        estructura_tokens.append('end')
    
    # Validar con el AFN de IF
    try:
        estructura_valida = afn_if.accepts_input(estructura_tokens)
        print(f"¿Estructura válida? {estructura_valida}")
        if not estructura_valida:
            return False
    except Exception as e:
        print(f"Error validando estructura: {e}")
        return False
    
    # 2. Validar las asignaciones
    asignaciones = extraer_asignaciones(codigo)
    print(f"Asignaciones encontradas: {asignaciones}")
    
    for i, asignacion in enumerate(asignaciones):
        asignacion_completa = asignacion + ";" if not asignacion.endswith(";") else asignacion
        print(f"Validando asignación {i+1}: '{asignacion_completa}'")
        
        if not validar_asignacion(asignacion_completa):
            print(f"❌ Asignación inválida: {asignacion_completa}")
            return False
        else:
            print(f"✅ Asignación válida: {asignacion_completa}")
    
    return True

def simular_automata(cadena):
    afn = afn_if
    tokens = tokenizar(cadena)
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
    tokens = tokenizar(codigo)
    print(f"Tokens generados: {tokens}")
    return tokens

def debug_mealy_paso_a_paso(codigo):
    """Función para ver el funcionamiento paso a paso de la máquina de Mealy"""
    print(f"=== DEBUGGING MÁQUINA DE MEALY ===")
    print(f"Código: {repr(codigo)}")
    print(f"Procesamiento carácter por carácter:")
    
    tokenizer = MealyTokenizer()
    tokens = []
    estado_actual = 'INICIAL'
    buffer = ''
    
    for i, char in enumerate(codigo):
        tipo_char = tokenizer.clasificar_caracter(char)
        print(f"  {i}: '{char}' (tipo: {tipo_char}) - Estado: {estado_actual} - Buffer: '{buffer}'")
        
        # Simular una iteración del tokenizador
        transiciones_estado = tokenizer.transitions.get(estado_actual, {})
        
        if tipo_char in transiciones_estado:
            nuevo_estado, accion = transiciones_estado[tipo_char]
        elif 'otro' in transiciones_estado:
            nuevo_estado, accion = transiciones_estado['otro']
        else:
            continue
            
        print(f"     -> Acción: {accion}, Nuevo estado: {nuevo_estado}")
        
        if accion in ['EMITIR_SIMPLE', 'EMITIR_STRING', 'EMITIR_OP_DOBLE', 'EMITIR_ID_Y_PROCESAR', 'EMITIR_NUM_Y_PROCESAR']:
            print(f"     -> Token emitido!")
            
        estado_actual = nuevo_estado
    
    tokens_finales = tokenizer.tokenizar(codigo)
    print(f"\nTokens finales: {tokens_finales}")
    return tokens_finales

# Ejemplo de uso
if __name__ == "__main__":
    codigo = '''
    if(x == 3 && y != 2)
        a = 5;
    else
        d = 'a';
    end
    '''

    print("=== COMPARACIÓN DE TOKENIZADORES ===")
    print("Tokens con Máquina de Mealy:", tokenizar(codigo))
    print("\n=== DEBUGGING PASO A PASO ===")
    debug_mealy_paso_a_paso("if(x == 3)")
    
    print("\n=== VALIDACIÓN COMPLETA ===")
    print("¿Código válido?:", validar_if_con_bloque(codigo))