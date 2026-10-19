
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from automata import Automata
from validador import Validador
from generador_diagrama import GeneradorDiagrama


class InterfazAutomata:
    """Interfaz gráfica del Generador de Diagramas de Autómatas Finitos."""

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador de Diagramas de Autómatas Finitos")
        self.ventana.geometry("900x760")
        self.ventana.minsize(720, 650)

        self.archivo_generado = None

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        estilo = ttk.Style()
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 17, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10))
        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"),
                         padding=8)

    def crear_interfaz(self):
        principal = ttk.Frame(self.ventana, padding=18)
        principal.pack(fill="both", expand=True)

        # Encabezado
        ttk.Label(
            principal,
            text="Generador de Autómatas Finitos",
            style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            principal,
            text="Define los cinco elementos formales y genera su diagrama.",
            style="Subtitulo.TLabel"
        ).pack(anchor="w", pady=(4, 15))

        # Datos formales
        datos = ttk.LabelFrame(
            principal,
            text="1. Definición del autómata",
            padding=12
        )
        datos.pack(fill="x", pady=(0, 12))
        datos.columnconfigure(1, weight=1)

        self.entrada_estados = self.agregar_campo(
            datos, 0, "Estados Q:", "q0, q1, q2"
        )
        self.entrada_alfabeto = self.agregar_campo(
            datos, 1, "Alfabeto Σ:", "0, 1"
        )
        self.entrada_inicial = self.agregar_campo(
            datos, 2, "Estado inicial q0:", "q0"
        )
        self.entrada_finales = self.agregar_campo(
            datos, 3, "Estados finales F:", "q2"
        )

        # Transiciones
        transiciones = ttk.LabelFrame(
            principal,
            text="2. Función de transición δ",
            padding=12
        )
        transiciones.pack(fill="both", expand=True, pady=(0, 12))

        ttk.Label(
            transiciones,
            text="Una transición por línea. Usa el formato: origen, símbolo -> destino(s)"
        ).pack(anchor="w")

        ttk.Label(
            transiciones,
            text="Ejemplo AFD: q0, 0 -> q0     |     Ejemplo AFND: q0, 0 -> q0, q1"
        ).pack(anchor="w", pady=(2, 8))

        self.caja_transiciones = scrolledtext.ScrolledText(
            transiciones,
            height=10,
            font=("Consolas", 11),
            wrap="none"
        )
        self.caja_transiciones.pack(fill="both", expand=True)

        self.caja_transiciones.insert(
            "1.0",
            "q0, 0 -> q0\n"
            "q0, 1 -> q1\n"
            "q1, 0 -> q2\n"
            "q1, 1 -> q0\n"
            "q2, 0 -> q2\n"
            "q2, 1 -> q1"
        )

        # Botones
        botones = ttk.Frame(principal)
        botones.pack(fill="x", pady=(0, 10))

        ttk.Button(
            botones,
            text="Validar autómata",
            command=self.validar_autómata,
            style="Accion.TButton"
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Generar diagrama",
            command=self.generar_diagrama,
            style="Accion.TButton"
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Abrir diagrama",
            command=self.abrir_diagrama
        ).pack(side="left", padx=(0, 8))

        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar
        ).pack(side="right")

        # Área de resultados
        resultados = ttk.LabelFrame(
            principal,
            text="3. Resultado",
            padding=10
        )
        resultados.pack(fill="x")

        self.resultado = tk.Text(
            resultados,
            height=5,
            font=("Consolas", 10),
            wrap="word",
            state="disabled"
        )
        self.resultado.pack(fill="x")

        self.mostrar_resultado(
            "Listo. Introduce los datos y pulsa «Validar autómata»."
        )

    def agregar_campo(self, contenedor, fila, texto, ejemplo):
        ttk.Label(
            contenedor,
            text=texto
        ).grid(row=fila, column=0, sticky="w", padx=(0, 12), pady=5)

        entrada = ttk.Entry(contenedor)
        entrada.grid(row=fila, column=1, sticky="ew", pady=5)
        entrada.insert(0, ejemplo)

        return entrada

    @staticmethod
    def separar_lista(texto):
        return [elemento.strip() for elemento in texto.split(",")
                if elemento.strip()]

    def construir_automata(self):
        estados = self.separar_lista(self.entrada_estados.get())
        alfabeto = self.separar_lista(self.entrada_alfabeto.get())
        estado_inicial = self.entrada_inicial.get().strip()
        estados_finales = self.separar_lista(self.entrada_finales.get())

        if not estados:
            raise ValueError("Debes ingresar al menos un estado en Q.")

        if not alfabeto:
            raise ValueError("Debes ingresar al menos un símbolo en Σ.")

        if not estado_inicial:
            raise ValueError("Debes ingresar el estado inicial.")

        # Leer las transiciones
        transiciones = {}
        lineas = self.caja_transiciones.get("1.0", "end").splitlines()

        for numero, linea in enumerate(lineas, start=1):
            linea = linea.strip()

            if not linea:
                continue

            if "->" not in linea:
                raise ValueError(
                    f"Línea {numero}: falta la flecha ->. "
                    "Ejemplo: q0, 0 -> q1"
                )

            partes = linea.split("->")

            if len(partes) != 2:
                raise ValueError(
                    f"Línea {numero}: la transición debe tener una sola flecha."
                )

            origen_simbolo = partes[0].split(",")
            destinos = self.separar_lista(partes[1])

            if len(origen_simbolo) != 2:
                raise ValueError(
                    f"Línea {numero}: escribe origen y símbolo separados "
                    "por coma. Ejemplo: q0, 0 -> q1"
                )

            origen = origen_simbolo[0].strip()
            simbolo = origen_simbolo[1].strip()

            if not origen or not simbolo or not destinos:
                raise ValueError(
                    f"Línea {numero}: faltan datos en la transición."
                )

            if origen not in transiciones:
                transiciones[origen] = {}

            if simbolo in transiciones[origen]:
                raise ValueError(
                    f"Línea {numero}: ya existe una transición para "
                    f"({origen}, {simbolo}). Combina sus destinos en una "
                    "sola línea si se trata de un AFND."
                )

            # Un destino se guarda como texto; varios, como lista.
            if len(destinos) == 1:
                transiciones[origen][simbolo] = destinos[0]
            else:
                transiciones[origen][simbolo] = destinos

        return Automata(
            estados,
            alfabeto,
            transiciones,
            estado_inicial,
            estados_finales
        )

    def validar_autómata(self):
        try:
            automata = self.construir_automata()
            validador = Validador(automata)

            if validador.validar():
                tipo = automata.detectar_tipo()

                self.mostrar_resultado(
                    "AUTÓMATA VÁLIDO\n"
                    f"Tipo detectado: {tipo}\n"
                    f"Cantidad de estados: {len(automata.estados)}\n"
                    f"Cantidad de símbolos: {len(automata.alfabeto)}\n"
                    f"Estado inicial: {automata.estado_inicial}\n"
                    f"Estados finales: {', '.join(sorted(automata.estados_finales))}"
                )
                return True

            errores = "\n".join(
                f"• {error}" for error in validador.errores
            )
            self.mostrar_resultado("AUTÓMATA INVÁLIDO\n" + errores)
            return False

        except ValueError as error:
            self.mostrar_resultado(f"ERROR EN LOS DATOS\n{error}")
            return False

        except Exception as error:
            self.mostrar_resultado(f"ERROR INESPERADO\n{error}")
            return False

    def generar_diagrama(self):
        try:
            automata = self.construir_automata()
            validador = Validador(automata)

            if not validador.validar():
                errores = "\n".join(validador.errores)
                self.mostrar_resultado(
                    "No se puede generar el diagrama:\n" + errores
                )
                return

            tipo = automata.detectar_tipo()
            generador = GeneradorDiagrama(automata)

            self.archivo_generado = generador.generar(
                nombre_archivo="automata_generado",
                formato="png"
            )

            self.mostrar_resultado(
                "DIAGRAMA GENERADO CORRECTAMENTE\n"
                f"Tipo de autómata: {tipo}\n"
                f"Archivo: {self.archivo_generado}"
            )

            messagebox.showinfo(
                "Éxito",
                "El diagrama se generó correctamente.\n\n"
                f"Ubicación: {self.archivo_generado}"
            )

        except Exception as error:
            self.mostrar_resultado(
                f"NO SE PUDO GENERAR EL DIAGRAMA\n{error}"
            )
            messagebox.showerror("Error", str(error))

    def abrir_diagrama(self):
        if not self.archivo_generado:
            messagebox.showwarning(
                "Aviso",
                "Primero genera un diagrama."
            )
            return

        if not os.path.exists(self.archivo_generado):
            messagebox.showerror(
                "Error",
                "No se encontró el archivo del diagrama."
            )
            return

        try:
            os.startfile(os.path.abspath(self.archivo_generado))
        except OSError as error:
            messagebox.showerror(
                "Error",
                f"No se pudo abrir el diagrama:\n{error}"
            )

    def limpiar(self):
        self.entrada_estados.delete(0, "end")
        self.entrada_alfabeto.delete(0, "end")
        self.entrada_inicial.delete(0, "end")
        self.entrada_finales.delete(0, "end")
        self.caja_transiciones.delete("1.0", "end")
        self.archivo_generado = None

        self.mostrar_resultado(
            "Formulario limpiado. Ingresa un nuevo autómata."
        )

    def mostrar_resultado(self, mensaje):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", mensaje)
        self.resultado.configure(state="disabled")


if __name__ == "__main__":
    ventana = tk.Tk()
    aplicacion = InterfazAutomata(ventana)
    ventana.mainloop()
