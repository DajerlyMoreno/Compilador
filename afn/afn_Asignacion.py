from automata.fa.nfa import NFA
import string

letras = set(string.ascii_letters)
digitos = set(string.digits) 
operadores = set(['+', '-', '*', '/', '%', '^'])
alfanumericos = letras.union(digitos)

afn_Asignacion = NFA(
    states={'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11'},
    input_symbols=alfanumericos.union({'=', '"', "'",';'}).union(operadores),
    transitions={
        'q0': {letra: {'q1'} for letra in letras},

        'q1': {
            **{valor: {'q1'} for valor in alfanumericos},
            '=': {'q2'}
        },
        'q2': {
            **{letra: {'q4'} for letra in letras},
            **{numero: {'q3'} for numero in digitos},
            "'": {'q9'},
            '"': {'q7'}
        },
        'q3': {
            **{operador: {'q5'} for operador in operadores},
            **{numero: {'q3'} for numero in digitos},
            ";": {'q11'},
        },
        'q4': {
            **{valor: {'q4'} for valor in alfanumericos},
            **{operador: {'q6'} for operador in operadores},
            ";": {'q11'},
        },
        'q5': {
            **{letra: {'q4'} for letra in letras},
            **{numero: {'q3'} for numero in digitos},
            "'": {'q9'},
            '"': {'q7'},
        },
        'q6': {
            **{letra: {'q4'} for letra in letras},
            **{numero: {'q3'} for numero in digitos},
            "'": {'q9'},
            '"': {'q7'}
        },
        'q7': {
            **{valor: {'q8'} for valor in alfanumericos}
        },
        'q8': {
            **{valor: {'q8'} for valor in alfanumericos},
            '"': {'q3'}
        },
        'q9': {
            **{valor: {'q10'} for valor in alfanumericos}
        },
        'q10': {
            **{valor: {'q10'} for valor in alfanumericos},
            "'": {'q3'}
        },
        
    },
    initial_state='q0',
    final_states={'q3', 'q4', 'q11'},
)

def validar_asignacion(cadena):
    """
    Valida si una cadena es una asignación válida.
    """
    cadena = cadena.replace(" ", "")
    try:
        return afn_Asignacion.accepts_input(cadena)
    except Exception:
        return False
    
def simular_automata(cadena):
    afn = afn_Asignacion
    cadena = ''.join(c for c in cadena if not c.isspace())  # eliminar espacios
    salida = ""

    estados_actuales = {afn.initial_state}
    salida += f"Estado inicial: {estados_actuales}\n"

    for i, simbolo in enumerate(cadena):
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

