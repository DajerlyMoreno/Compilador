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
    
def simular_automata(afn, cadena):
    cadena = ''.join(c for c in cadena if not c.isspace())  # eliminar espacios
    estados_actuales = {afn.initial_state}
    print(f"Estado inicial: {estados_actuales}")

    for i, simbolo in enumerate(cadena):
        nuevos_estados = set()
        print(f"\nSímbolo '{simbolo}' (posición {i}):")

        for estado in estados_actuales:
            transiciones = afn.transitions.get(estado, {})
            if simbolo in transiciones:
                nuevos_estados.update(transiciones[simbolo])
                print(f"  {estado} --{simbolo}--> {transiciones[simbolo]}")
            else:
                print(f"  {estado} --{simbolo}--> ❌ (no hay transición)")

        if not nuevos_estados:
            print("\n❌ No hay transiciones válidas. Cadena rechazada.")
            return False

        estados_actuales = nuevos_estados
        print(f"Estados actuales: {estados_actuales}")

    aceptado = bool(estados_actuales & afn.final_states)
    if aceptado:
        print("\n✅ La cadena fue aceptada.")
    else:
        print("\n❌ La cadena fue rechazada. Estados finales alcanzados:", estados_actuales)
    return aceptado

    
print(validar_asignacion("a = 5"))  # True
print(validar_asignacion("a = b + c"))  # True
print(validar_asignacion("a = 5 + 2;"))  # True

simular_automata(afn_Asignacion, "a = 5 + 2;")