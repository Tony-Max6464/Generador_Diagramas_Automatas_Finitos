class Automata:
    """
    Representa un autómata finito mediante sus 5 elementos formales:

    Q      -> conjunto de estados
    Sigma  -> alfabeto
    delta  -> función de transición
    q0     -> estado inicial
    F      -> estados finales
    """

    def __init__(self, estados, alfabeto, transiciones, estado_inicial, estados_finales):

        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)

    def mostrar(self):
        """Muestra la definición formal del autómata."""

        print("\n===== AUTÓMATA FINITO =====")

        print("Q =", self.estados)
        print("Σ =", self.alfabeto)
        print("q0 =", self.estado_inicial)
        print("F =", self.estados_finales)

        print("\nδ (transiciones):")

        for estado, transiciones_estado in self.transiciones.items():

            for simbolo, destino in transiciones_estado.items():

                print(
                    f"δ({estado}, {simbolo}) = {destino}"
                )