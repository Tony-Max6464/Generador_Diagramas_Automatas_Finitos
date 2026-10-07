from graphviz import Digraph
import os


class GeneradorDiagrama:
    """
    Genera el diagrama visual de un autómata finito
    utilizando Graphviz.
    """

    def __init__(self, automata):
        self.automata = automata

    def generar(self, nombre_archivo="diagrama_automata", formato="png"):
        """
        Genera el diagrama del autómata.

        Parámetros:
            nombre_archivo: nombre del archivo de salida.
            formato: formato de imagen (png, svg, pdf, etc.).
        """

        # Crear objeto Graphviz
        diagrama = Digraph(
            name="AutomataFinito",
            format=formato
        )

        # Configuración visual
        diagrama.attr(
            rankdir="LR",
            bgcolor="white"
        )

        # Configuración de los estados
        diagrama.attr(
            "node",
            shape="circle",
            style="filled",
            fillcolor="white"
        )

        # ==========================================
        # ESTADO INICIAL
        # ==========================================

        # Nodo invisible que apunta al estado inicial
        diagrama.node(
            "inicio",
            shape="point",
            width="0.15"
        )

        diagrama.edge(
            "inicio",
            self.automata.estado_inicial
        )

        # ==========================================
        # ESTADOS
        # ==========================================

        for estado in self.automata.estados:

            # Los estados finales tienen doble círculo
            if estado in self.automata.estados_finales:

                diagrama.node(
                    estado,
                    shape="doublecircle",
                    label=estado,
                    style="filled",
                    fillcolor="white"
                )

            else:

                diagrama.node(
                    estado,
                    shape="circle",
                    label=estado,
                    style="filled",
                    fillcolor="white"
                )

        # ==========================================
        # TRANSICIONES
        # ==========================================

        for estado_origen, transiciones in self.automata.transiciones.items():

            for simbolo, destinos in transiciones.items():

                # AFD: un solo destino
                if not isinstance(destinos, list):
                    destinos = [destinos]

                # AFND: varios destinos
                for destino in destinos:

                    diagrama.edge(
                        estado_origen,
                        destino,
                        label=str(simbolo)
                    )

        # ==========================================
        # CREAR CARPETA DE SALIDA
        # ==========================================

        carpeta_salida = "diagramas"

        os.makedirs(
            carpeta_salida,
            exist_ok=True
        )

        # Ruta del archivo
        ruta = os.path.join(
            carpeta_salida,
            nombre_archivo
        )

        # Generar archivo
        archivo_generado = diagrama.render(
            filename=ruta,
            cleanup=True
        )

        print("\n===== DIAGRAMA GENERADO =====")
        print(f"Archivo: {archivo_generado}")

        return archivo_generado