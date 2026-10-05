class Validador:
    """
    Se encarga de validar la definición formal
    de un autómata finito.
    """

    def __init__(self, automata):
        self.automata = automata
        self.errores = []

    def validar_estados(self):
        """Comprueba que exista al menos un estado."""

        if not self.automata.estados:
            self.errores.append(
                "El conjunto de estados Q no puede estar vacío."
            )

    def validar_estado_inicial(self):
        """Comprueba que q0 pertenezca a Q."""

        if self.automata.estado_inicial not in self.automata.estados:
            self.errores.append(
                f"El estado inicial "
                f"'{self.automata.estado_inicial}' "
                f"no pertenece al conjunto Q."
            )

    def validar_estados_finales(self):
        """Comprueba que F sea subconjunto de Q."""

        for estado in self.automata.estados_finales:

            if estado not in self.automata.estados:
                self.errores.append(
                    f"El estado final '{estado}' "
                    f"no pertenece al conjunto Q."
                )

    def validar_transiciones(self):
        """
        Comprueba que los estados y símbolos utilizados
        en las transiciones sean válidos.
        """

        for estado_origen, transiciones in self.automata.transiciones.items():

            # Comprobar estado de origen
            if estado_origen not in self.automata.estados:
                self.errores.append(
                    f"El estado origen '{estado_origen}' "
                    f"no pertenece a Q."
                )

            for simbolo, destinos in transiciones.items():

                # Comprobar símbolo
                if simbolo not in self.automata.alfabeto:
                    self.errores.append(
                        f"El símbolo '{simbolo}' "
                        f"no pertenece al alfabeto Σ."
                    )

                # Convertir destino en una lista
                # para poder manejar AFD y AFND
                if isinstance(destinos, list):
                    destinos_lista = destinos
                else:
                    destinos_lista = [destinos]

                # Comprobar estados destino
                for destino in destinos_lista:

                    if destino not in self.automata.estados:
                        self.errores.append(
                            f"El estado destino '{destino}' "
                            f"no pertenece a Q."
                        )

    def validar(self):
        """
        Ejecuta todas las validaciones.

        Devuelve True si el autómata es válido.
        """

        self.errores = []

        self.validar_estados()
        self.validar_estado_inicial()
        self.validar_estados_finales()
        self.validar_transiciones()

        return len(self.errores) == 0

    def mostrar_resultado(self):

        if self.validar():

            print("\n✓ AUTÓMATA VÁLIDO")
            print("No se encontraron errores.")

        else:

            print("\n✗ AUTÓMATA INVÁLIDO")

            print("\nErrores encontrados:")

            for error in self.errores:
                print(f"  - {error}")