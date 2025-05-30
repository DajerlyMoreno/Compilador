from automata.fa.nfa import NFA
import re
from afn_Asignacion import validar_asignacion

def tokenizar(codigo):
    patron = r'''
        (==|!=|<=|>=|&&|\|\|)        | # operadores dobles
        ([<>!=+\-*/])               | # operadores simples (agregado +, -, *, /)
        (\bif\b|\belse\b|\bend\b|\belseif\b)   | # palabras clave
        ([a-zA-Z_]\w*)              | # identificadores (id)
        (\d+)                       | # números (num)
        (".*?"|'.*?')               | # cadenas de texto (agregado)
        ([();=])                    # paréntesis, punto y coma, igual (agregado =)
    '''
    tokens = re.findall(patron, codigo, re.VERBOSE)
    
    tokens = [token for group in tokens for token in group if token]

    # Convertir identificadores y números a tokens genéricos
    tokens_genericos = []
    for tok in tokens:
        if re.fullmatch(r'[a-zA-Z_]\w*', tok) and tok not in {'if', 'else', 'end', 'elseif'}:
            tokens_genericos.append('id')
        elif re.fullmatch(r'\d+', tok):
            tokens_genericos.append('num')
        elif re.fullmatch(r'".*?"|\'.*?\'', tok):  # cadenas de texto
            tokens_genericos.append('string')
        else:
            tokens_genericos.append(tok)
    
    return tokens_genericos


afn_if = NFA(
    states={
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6',
        'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13',
        'q14', 'q15', 'q16', 'q17', 'q18'
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
            'end': {'q18'}
        },
        'q8': {';': {'q9'}},
        'q9': {'end': {'q18'}}
    },
    initial_state='q0',
    final_states={'q18'}
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
    print(f"=== VALIDANDO CÓDIGO ===")
    print(f"Código:\n{codigo}")
    
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
    
    print(f"Tokens de estructura: {estructura_tokens}")
    
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

# Ejemplo
codigo = '''
if (x == 3 && y != 2)
    a = 5;
    b = 3 + 4;
elseif (z > 1)
    c = "hola";
else
    d = 'a';
end
'''

print("=== DEBUGGING ===")
print("¿Código válido?:", validar_if_con_bloque(codigo))
