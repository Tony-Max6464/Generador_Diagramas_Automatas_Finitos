

import os

import tkinter as tk

from tkinter import ttk, messagebox, scrolledtext



from automata import Automata

from validador import Validador

from generador_diagrama import GeneradorDiagrama





class InterfazAutomata:

    """Interfaz gráfica para crear y dibujar autómatas finitos."""



    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title("Generador de Diagramas de Autómatas Finitos")

        self.ventana.geometry("1000x820")

        self.ventana.minsize(800, 680)



        self.transiciones_ui = []

        self.archivo_generado = None



        self.configurar_estilos()

        self.crear_interfaz()



    def configurar_estilos(self):

        estilo = ttk.Style()

        estilo.configure("Titulo.TLabel", font=("Segoe UI", 17, "bold"))

        estilo.configure("Tipo.TLabel", font=("Segoe UI", 12, "bold"))

        estilo.configure("Accion.TButton", font=("Segoe UI", 10, "bold"),

                         padding=7)

        estilo.configure("Treeview", rowheight=27)



    def crear_interfaz(self):

        principal = ttk.Frame(self.ventana, padding=16)

        principal.pack(fill="both", expand=True)



        ttk.Label(

            principal,

            text="Generador de Autómatas Finitos",

            style="Titulo.TLabel"

        ).pack(anchor="w")



        ttk.Label(

            principal,

            text="Define los elementos formales y construye las transiciones."

        ).pack(anchor="w", pady=(3, 5))



        self.etiqueta_tipo = ttk.Label(

            principal,

            text="Tipo de autómata: pendiente de validar",

            style="Tipo.TLabel",

            foreground="#0078D7"

        )

        self.etiqueta_tipo.pack(anchor="w", pady=(0, 10))



        # 1. Elementos formales

        datos = ttk.LabelFrame(

            principal, text="1. Elementos formales", padding=10

        )

        datos.pack(fill="x", pady=(0, 10))

        datos.columnconfigure(1, weight=1)

        datos.columnconfigure(3, weight=1)



        self.entrada_estados = self.campo(

            datos, 0, 0, "Estados Q:", "q0, q1, q2"

        )

        self.entrada_alfabeto = self.campo(

            datos, 0, 2, "Alfabeto Σ:", "0, 1"

        )

        self.entrada_inicial = self.campo(

            datos, 1, 0, "Estado inicial:", "q0"

        )

        self.entrada_finales = self.campo(

            datos, 1, 2, "Estados finales F:", "q2"

        )



        ttk.Button(

            datos,

            text="Actualizar listas",

            command=self.actualizar_listas

        ).grid(row=2, column=0, columnspan=4, sticky="ew", pady=(8, 0))



        # 2. Agregar transiciones

        panel = ttk.LabelFrame(

            principal, text="2. Agregar una transición", padding=10

        )

        panel.pack(fill="x", pady=(0, 10))

        panel.columnconfigure(1, weight=1)

        panel.columnconfigure(3, weight=1)



        ttk.Label(panel, text="Estado de origen:").grid(

            row=0, column=0, sticky="w", padx=(0, 6), pady=4

        )



        self.combo_origen = ttk.Combobox(panel, state="readonly")

        self.combo_origen.grid(

            row=0, column=1, sticky="ew", padx=(0, 14), pady=4

        )



        ttk.Label(panel, text="Símbolo:").grid(

            row=0, column=2, sticky="w", padx=(0, 6), pady=4

        )



        self.combo_simbolo = ttk.Combobox(panel, state="readonly")

        self.combo_simbolo.grid(

            row=0, column=3, sticky="ew", pady=4

        )



        ttk.Label(

            panel,

            text="Estado(s) de destino: mantén Ctrl para elegir varios."

        ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(8, 4))



        frame_destinos = ttk.Frame(panel)

        frame_destinos.grid(

            row=2, column=0, columnspan=4, sticky="ew"

        )

        frame_destinos.columnconfigure(0, weight=1)



        self.lista_destinos = tk.Listbox(

            frame_destinos,

            selectmode=tk.EXTENDED,

            height=3,

            exportselection=False

        )

        self.lista_destinos.grid(row=0, column=0, sticky="ew")



        scroll_destinos = ttk.Scrollbar(

            frame_destinos,

            orient="vertical",

            command=self.lista_destinos.yview

        )

        scroll_destinos.grid(row=0, column=1, sticky="ns")

        self.lista_destinos.configure(

            yscrollcommand=scroll_destinos.set

        )



        ttk.Button(

            panel,

            text="Agregar transición",

            style="Accion.TButton",

            command=self.agregar_transicion

        ).grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0))



        # 3. Tabla de transiciones

        panel_tabla = ttk.LabelFrame(

            principal, text="3. Transiciones agregadas", padding=10

        )

        panel_tabla.pack(fill="both", expand=False, pady=(0, 10))

        panel_tabla.columnconfigure(0, weight=1)

        panel_tabla.rowconfigure(0, weight=1)



        self.tabla = ttk.Treeview(

            panel_tabla,

            columns=("origen", "simbolo", "destinos"),

            show="headings",

            height=4,

            selectmode="extended"

        )

        self.tabla.heading("origen", text="Origen")

        self.tabla.heading("simbolo", text="Símbolo")

        self.tabla.heading("destinos", text="Destino(s)")

        self.tabla.column("origen", width=110, anchor="center")

        self.tabla.column("simbolo", width=100, anchor="center")

        self.tabla.column("destinos", width=300, anchor="w")

        self.tabla.grid(row=0, column=0, sticky="nsew")



        scroll_tabla = ttk.Scrollbar(

            panel_tabla,

            orient="vertical",

            command=self.tabla.yview

        )

        scroll_tabla.grid(row=0, column=1, sticky="ns")

        self.tabla.configure(yscrollcommand=scroll_tabla.set)



        ttk.Button(

            panel_tabla,

            text="Eliminar transición seleccionada",

            command=self.eliminar_transicion

        ).grid(row=1, column=0, sticky="ew", pady=(8, 0))



        # 4. Acciones

        botones = ttk.Frame(principal)

        botones.pack(fill="x", pady=(0, 10))



        ttk.Button(

            botones,

            text="Validar autómata",

            style="Accion.TButton",

            command=self.validar_automata

        ).pack(side="left", padx=(0, 7))



        ttk.Button(

            botones,

            text="Generar diagrama",

            style="Accion.TButton",

            command=self.generar_diagrama

        ).pack(side="left", padx=(0, 7))



        ttk.Button(

            botones,

            text="Abrir diagrama",

            command=self.abrir_diagrama

        ).pack(side="left", padx=(0, 7))



        ttk.Button(

            botones,

            text="Limpiar todo",

            command=self.limpiar

        ).pack(side="right")



        # 5. Resultados

        panel_resultado = ttk.LabelFrame(

            principal, text="4. Resultado de la validación", padding=8

        )

        panel_resultado.pack(fill="x")



        self.resultado = scrolledtext.ScrolledText(

            panel_resultado,

            height=5,

            wrap="word",

            font=("Consolas", 10),

            state="disabled"

        )

        self.resultado.pack(fill="x")



        self.actualizar_listas()

        self.mostrar_resultado(

            "Listo. Actualiza las listas y agrega las transiciones."

        )



    def campo(self, contenedor, fila, columna, etiqueta, ejemplo):

        ttk.Label(

            contenedor, text=etiqueta

        ).grid(

            row=fila, column=columna,

            sticky="w", padx=(0, 6), pady=5

        )



        entrada = ttk.Entry(contenedor)

        entrada.grid(

            row=fila, column=columna + 1,

            sticky="ew", padx=(0, 12), pady=5

        )

        entrada.insert(0, ejemplo)

        return entrada



    @staticmethod

    def separar_lista(texto):

        return [

            elemento.strip()

            for elemento in texto.split(",")

            if elemento.strip()

        ]



    def actualizar_listas(self):

        estados = self.separar_lista(self.entrada_estados.get())

        alfabeto = self.separar_lista(self.entrada_alfabeto.get())



        if len(estados) != len(set(estados)):

            messagebox.showerror("Error", "No repitas estados en Q.")

            return



        if len(alfabeto) != len(set(alfabeto)):

            messagebox.showerror(

                "Error", "No repitas símbolos en el alfabeto."

            )

            return



        self.combo_origen["values"] = estados

        self.combo_simbolo["values"] = alfabeto



        self.combo_origen.set(estados[0] if estados else "")

        self.combo_simbolo.set(alfabeto[0] if alfabeto else "")



        self.lista_destinos.delete(0, "end")

        for estado in estados:

            self.lista_destinos.insert("end", estado)



        self.transiciones_ui.clear()

        self.actualizar_tabla()

        self.archivo_generado = None

        self.etiqueta_tipo.configure(

            text="Tipo de autómata: pendiente de validar",

            foreground="#0078D7"

        )

        self.mostrar_resultado(

            "Listas actualizadas. Agrega las transiciones."

        )



    def agregar_transicion(self):

        origen = self.combo_origen.get()

        simbolo = self.combo_simbolo.get()



        destinos = [

            self.lista_destinos.get(i)

            for i in self.lista_destinos.curselection()

        ]



        if not origen or not simbolo:

            messagebox.showwarning(

                "Faltan datos", "Selecciona origen y símbolo."

            )

            return



        if not destinos:

            messagebox.showwarning(

                "Falta el destino", "Selecciona al menos un destino."

            )

            return



        if any(

            t[0] == origen and t[1] == simbolo

            for t in self.transiciones_ui

        ):

            messagebox.showwarning(

                "Transición duplicada",

                "Ya existe una transición para ese origen y símbolo.\n"

                "Para un AFND, selecciona todos los destinos juntos."

            )

            return



        self.transiciones_ui.append((origen, simbolo, destinos))

        self.actualizar_tabla()

        self.marcar_pendiente()

        self.mostrar_resultado(

            f"Agregada: {origen}, {simbolo} -> {', '.join(destinos)}"

        )



    def actualizar_tabla(self):

        for elemento in self.tabla.get_children():

            self.tabla.delete(elemento)



        for indice, (origen, simbolo, destinos) in enumerate(

            self.transiciones_ui

        ):

            self.tabla.insert(

                "",

                "end",

                iid=str(indice),

                values=(origen, simbolo, ", ".join(destinos))

            )



    def eliminar_transicion(self):

        seleccion = self.tabla.selection()



        if not seleccion:

            messagebox.showwarning(

                "Selecciona una transición",

                "Selecciona la transición que deseas eliminar."

            )

            return



        for indice in sorted(

            (int(item) for item in seleccion), reverse=True

        ):

            del self.transiciones_ui[indice]



        self.actualizar_tabla()

        self.marcar_pendiente()

        self.mostrar_resultado("Transición(es) eliminada(s).")



    def construir_automata(self):

        estados = self.separar_lista(self.entrada_estados.get())

        alfabeto = self.separar_lista(self.entrada_alfabeto.get())

        inicial = self.entrada_inicial.get().strip()

        finales = self.separar_lista(self.entrada_finales.get())



        if not estados:

            raise ValueError("Ingresa al menos un estado en Q.")

        if len(estados) != len(set(estados)):

            raise ValueError("Hay estados repetidos en Q.")

        if not alfabeto:

            raise ValueError("Ingresa al menos un símbolo en Σ.")

        if len(alfabeto) != len(set(alfabeto)):

            raise ValueError("Hay símbolos repetidos en Σ.")

        if not inicial:

            raise ValueError("Ingresa el estado inicial.")



        transiciones = {}



        for origen, simbolo, destinos in self.transiciones_ui:

            valor = destinos[0] if len(destinos) == 1 else list(destinos)

            transiciones.setdefault(origen, {})[simbolo] = valor



        return Automata(

            estados, alfabeto, transiciones, inicial, finales

        )



    def analizar_automata(self):

        automata = self.construir_automata()

        validador = Validador(automata)



        if not validador.validar():

            errores = "\n".join(

                f"• {error}" for error in validador.errores

            )

            self.etiqueta_tipo.configure(

                text="Definición inválida",

                foreground="#C62828"

            )

            self.mostrar_resultado(

                "AUTÓMATA INVÁLIDO\n" + errores

            )

            return None



        tipo = automata.detectar_tipo()

        faltantes = automata.obtener_transiciones_faltantes()



        if tipo == "AFND":

            etiqueta = "Tipo de autómata: AFND"

            detalle = (

                "La función de transición contiene al menos un par "

                "estado-símbolo con varios destinos."

            )

            color = "#0078D7"

        elif faltantes:

            etiqueta = "Tipo estructural: AFD incompleto"

            pares = ", ".join(

                f"({estado}, {simbolo})"

                for estado, simbolo in faltantes

            )

            detalle = (

                "No se encontraron transiciones con varios destinos, "

                "pero faltan transiciones para completar un AFD.\n"

                f"Pares sin transición: {pares}"

            )

            color = "#B26A00"

        else:

            etiqueta = "Tipo de autómata: AFD completo"

            detalle = (

                "Cada estado tiene exactamente un destino para cada "

                "símbolo del alfabeto."

            )

            color = "#218838"



        self.etiqueta_tipo.configure(

            text=etiqueta,

            foreground=color

        )



        resumen = (

            "DEFINICIÓN FORMAL CONSISTENTE\n"

            f"{etiqueta}\n"

            f"Estados: {len(automata.estados)}\n"

            f"Símbolos: {len(automata.alfabeto)}\n"

            f"Estado inicial: {automata.estado_inicial}\n"

            f"Estados finales: {', '.join(sorted(automata.estados_finales))}\n\n"

            f"{detalle}"

        )



        self.mostrar_resultado(resumen)

        return automata



    def validar_automata(self):

        try:

            self.analizar_automata()

        except Exception as error:

            self.etiqueta_tipo.configure(

                text="No se pudo analizar el autómata",

                foreground="#C62828"

            )

            self.mostrar_resultado(f"Error al validar:\n{error}")



    def generar_diagrama(self):

        try:

            automata = self.analizar_automata()



            if automata is None:

                return



            generador = GeneradorDiagrama(automata)

            self.archivo_generado = generador.generar(

                nombre_archivo="automata_generado",

                formato="png"

            )



            self.mostrar_resultado(

                self.obtener_resumen_actual()

                + f"\n\nDiagrama generado: {self.archivo_generado}"

            )



            messagebox.showinfo(

                "Diagrama generado",

                f"Archivo creado:\n{self.archivo_generado}"

            )



        except Exception as error:

            self.mostrar_resultado(

                f"No se pudo generar el diagrama:\n{error}"

            )

            messagebox.showerror("Error", str(error))



    def obtener_resumen_actual(self):

        return self.resultado.get("1.0", "end").strip()



    def abrir_diagrama(self):

        if not self.archivo_generado:

            messagebox.showwarning(

                "Sin diagrama", "Primero genera un diagrama."

            )

            return



        ruta = os.path.abspath(self.archivo_generado)



        if not os.path.exists(ruta):

            messagebox.showerror(

                "Archivo no encontrado", f"No existe:\n{ruta}"

            )

            return



        try:

            os.startfile(ruta)

        except OSError as error:

            messagebox.showerror("No se pudo abrir", str(error))



    def marcar_pendiente(self):

        self.archivo_generado = None

        self.etiqueta_tipo.configure(

            text="Tipo de autómata: pendiente de validar",

            foreground="#0078D7"

        )



    def limpiar(self):

        for entrada in (

            self.entrada_estados,

            self.entrada_alfabeto,

            self.entrada_inicial,

            self.entrada_finales

        ):

            entrada.delete(0, "end")



        self.transiciones_ui.clear()

        self.actualizar_tabla()

        self.combo_origen.set("")

        self.combo_simbolo.set("")

        self.lista_destinos.delete(0, "end")

        self.marcar_pendiente()

        self.mostrar_resultado(

            "Formulario limpiado. Introduce un nuevo autómata."

        )



    def mostrar_resultado(self, mensaje):

        self.resultado.configure(state="normal")

        self.resultado.delete("1.0", "end")

        self.resultado.insert("1.0", mensaje)

        self.resultado.configure(state="disabled")





if __name__ == "__main__":

    ventana = tk.Tk()

    InterfazAutomata(ventana)

    ventana.mainloop()