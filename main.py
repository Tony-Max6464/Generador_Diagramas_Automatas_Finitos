from automata import Automata
from validador import Validador
from generador_diagrama import GeneradorDiagrama


# ==========================================
# EJEMPLO DE AUTÓMATA FINITO
# ==========================================

# Conjunto de estados Q
estados = ["q0", "q1", "q2"]

# Alfabeto Σ
alfabeto = ["0", "1"]

# Función de transición δ
transiciones = {
    "q0": {
        "0": "q0",
        "1": "q1"
    },

    "q1": {
        "0": "q2",
        "1": "q0"
    },

    "q2": {
        "0": "q2",
        "1": "q1"
    }
}

# Estado inicial q0
estado_inicial = "q0"

# Estados finales F
estados_finales = ["q2"]


# ==========================================
# CREAR EL AUTÓMATA
# ==========================================

automata = Automata(
    estados,
    alfabeto,
    transiciones,
    estado_inicial,
    estados_finales
)


# ==========================================
# MOSTRAR EL AUTÓMATA
# ==========================================

automata.mostrar()


# ==========================================
# VALIDAR EL AUTÓMATA
# ==========================================

validador = Validador(automata)

validador.mostrar_resultado()


# ==========================================
# DETECTAR TIPO
# ==========================================

tipo = automata.detectar_tipo()

print("\nTipo de autómata:", tipo)


# ==========================================
# GENERAR DIAGRAMA
# ==========================================

if validador.validar():

    generador = GeneradorDiagrama(automata)

    generador.generar(
        nombre_archivo="mi_primer_automata",
        formato="png"
    )