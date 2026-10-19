
class Automata:
    """
    Representa un autómata finito mediante:
    Q, Sigma, delta, q0 y F.
    """

    def __init__(
        self,
        estados,
        alfabeto,
        transiciones,
        estado_inicial,
        estados_finales
    ):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)

    def mostrar(self):
        print("\n===== AUTÓMATA FINITO =====")
        print("Q =", self.estados)
        print("Σ =", self.alfabeto)
        print("q0 =", self.estado_inicial)
        print("F =", self.estados_finales)
        print("\nδ (transiciones):")

        for origen, transiciones_estado in self.transiciones.items():
            for simbolo, destinos in transiciones_estado.items():
                print(f"δ({origen}, {simbolo}) = {destinos}")

    @staticmethod
    def obtener_destinos(destinos):
        """Normaliza los destinos para analizarlos de forma uniforme."""
        if isinstance(destinos, (list, tuple, set, frozenset)):
            return list(destinos)
        return [destinos]

    def detectar_tipo(self):
        """
        Detecta el tipo estructural del autómata.

        Si existe algún par (estado, símbolo) con varios destinos,
        es AFND. En caso contrario, su estructura es determinista.
        La completitud se comprueba por separado.
        """
        for transiciones_estado in self.transiciones.values():
            for destinos in transiciones_estado.values():
                if len(self.obtener_destinos(destinos)) > 1:
                    return "AFND"

        return "AFD"

    def obtener_transiciones_faltantes(self):
        """
        Devuelve los pares (estado, símbolo) sin transición.
        Un AFD completo debe definirlos todos.
        """
        faltantes = []

        for estado in self.estados:
            transiciones_estado = self.transiciones.get(estado, {})

            for simbolo in self.alfabeto:
                if simbolo not in transiciones_estado:
                    faltantes.append((estado, simbolo))
                    continue

                destinos = self.obtener_destinos(
                    transiciones_estado[simbolo]
                )

                if not destinos:
                    faltantes.append((estado, simbolo))

        return sorted(faltantes)

    def es_completo(self):
        """Indica si todos los pares estado-símbolo tienen transición."""
        return len(self.obtener_transiciones_faltantes()) == 0