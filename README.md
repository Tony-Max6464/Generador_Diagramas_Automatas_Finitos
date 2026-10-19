Generador de Diagramas de Autómatas Finitos
Aplicación desarrollada en Python que permite definir un autómata finito desde una interfaz gráfica, validar su definición, identificar su estructura y generar su diagrama de estados mediante Graphviz.
Características actuales
- Introducir los estados Q, el alfabeto Σ, el estado inicial q0 y los estados finales F.
- Agregar y eliminar transiciones desde la interfaz gráfica.
- Seleccionar varios estados de destino para representar transiciones no deterministas.
- Validar la consistencia de la definición formal.
- Identificar estructuras AFD, AFND y AFD incompletos.
- Generar el diagrama del autómata en formato PNG.
- Abrir el diagrama generado desde la aplicación.
- Consultar el resultado de la validación en un panel con desplazamiento.
Alcance actual: la interfaz representa transiciones mediante símbolos del alfabeto. No se incluye una opción específica para transiciones epsilon (ε). La clasificación estructural se basa en si una transición tiene varios destinos; si no hay destinos múltiples pero faltan transiciones, se informa como AFD incompleto.

Requisitos
- Python 3 instalado.
- Visual Studio Code (recomendado, aunque puede usarse otro editor).
- Extensión de Python para Visual Studio Code (recomendada).
- Graphviz instalado en el sistema operativo.
- Paquete de Python graphviz.
Instalar las dependencias
1. Instala Python desde python.org si todavía no está instalado.
2. Instala Graphviz desde graphviz.org.
3. En Windows, si el programa no encuentra el ejecutable dot, agrega la carpeta bin de Graphviz a la variable de entorno PATH. Después, cierra y vuelve a abrir Visual Studio Code.
4. Instala el paquete de Python graphviz usando la terminal integrada de VS Code:
   python -m pip install -r requirements.txt
   Si el archivo requirements.txt no contiene la dependencia, instala el paquete con:
   python -m pip install graphviz
Graphviz del sistema y el paquete de Python son componentes diferentes; se necesitan ambos para generar diagramas.
Estructura del proyecto
La estructura puede verse así:
Generador_Diagramas_Automatas_Finitos/
├── main.py
├── interfaz.py
├── automata.py
├── validador.py
├── generador_diagrama.py
├── requirements.txt
├── README.md
├── ejemplos/
└── diagramas/
- main.py: inicia la aplicación gráfica.
- interfaz.py: contiene los campos, botones, tabla de transiciones y resultados.
- automata.py: representa el autómata, detecta su estructura y comprueba si faltan transiciones.
- validador.py: revisa la consistencia de los elementos del autómata.
- generador_diagrama.py: genera el diagrama con Graphviz.
- requirements.txt: lista las dependencias de Python.
- ejemplos/: carpeta destinada a ejemplos de autómatas.
- diagramas/: carpeta donde se guardan los diagramas generados, según la configuración del generador.
La presencia de las carpetas ejemplos/ y diagramas/ puede depender de los archivos incluidos en la copia del repositorio.
Cómo ejecutar el programa
Desde Visual Studio Code
1. Abre en VS Code la carpeta del proyecto completo.
2. Abre el archivo main.py.
3. Selecciona el intérprete de Python instalado en tu equipo, si VS Code lo solicita.
4. Ejecuta main.py con el botón Run Python File (Ejecutar archivo Python).
5. Se abrirá la ventana Generador de Autómatas Finitos.
También puede ejecutarse desde la terminal integrada, ubicada en la carpeta del proyecto:
python main.py
Cómo utilizar la interfaz
1. Definir los elementos formales
En Elementos formales, completa los campos separados por comas:
- Estados Q: lista de estados, por ejemplo q0, q1, q2.
- Alfabeto Σ: lista de símbolos, por ejemplo 0, 1.
- Estado inicial: un estado que pertenezca a Q, por ejemplo q0.
- Estados finales F: uno o más estados de Q, separados por comas, por ejemplo q2.
Los nombres de estados y símbolos deben escribirse de forma consistente. No repitas estados ni símbolos.

Pulsa Actualizar listas después de editar Q o el alfabeto. Importante: esta acción actualiza las opciones de selección y borra las transiciones que ya se habían agregado. Por eso, úsala antes de empezar a registrar las transiciones o después de estar seguro de que deseas reiniciarlas.
2. Agregar las transiciones
En Agregar una transición:
1. Selecciona el estado de origen.
2. Selecciona el símbolo del alfabeto.
3. Selecciona uno o varios estados de destino.
4. Pulsa Agregar transición.
Para elegir varios destinos, mantén presionada la tecla Ctrl mientras haces clic en cada estado de destino. Esto permite representar una transición no determinista.

Cada combinación de estado de origen y símbolo se agrega una sola vez. Si necesitas varios destinos para esa combinación, selecciónalos todos antes de pulsar Agregar transición.

Las transiciones añadidas aparecen en la tabla. Para quitar una o varias, selecciónalas en la tabla y pulsa Eliminar transición seleccionada.
3. Validar el autómata
Pulsa Validar autómata. La aplicación revisará la definición y mostrará el resumen en el panel Resultado de la validación.

La etiqueta superior informa del resultado estructural:
- Verde — AFD completo: cada estado tiene una transición definida para cada símbolo del alfabeto, con un único destino.
- Azul — AFND: se detectó al menos una combinación de estado y símbolo con varios destinos.
- Amarillo — AFD incompleto: no se detectaron destinos múltiples, pero faltan transiciones para uno o más pares estado-símbolo.
- Rojo — Definición inválida: se encontraron errores de consistencia, por ejemplo, un estado inicial que no pertenece a Q o un destino que no existe en Q.
El panel inferior muestra más detalles. Si el mensaje es largo, utiliza la barra de desplazamiento.
4. Generar el diagrama
Pulsa Generar diagrama. Si la definición pasa las comprobaciones de consistencia, la aplicación genera una imagen PNG del autómata.

El diagrama distingue el estado inicial y los estados finales, y muestra las transiciones con sus símbolos. El archivo se guarda en la carpeta de salida configurada por generador_diagrama.py (actualmente, diagramas/automata_generado.png).

La comprobación de completitud se informa por separado: un AFD incompleto puede pasar la validación básica de consistencia y aun así tener transiciones faltantes.
5. Abrir el diagrama
Después de generar la imagen, pulsa Abrir diagrama para abrir el archivo PNG con el visor de imágenes predeterminado del sistema.
6. Limpiar el formulario
Pulsa Limpiar todo para vaciar los campos y quitar las transiciones actuales. Después podrás introducir otro autómata.
Ejemplo de prueba: AFD completo
Introduce los siguientes datos:
- Estados Q: q0, q1, q2
- Alfabeto Σ: 0, 1
- Estado inicial: q0
- Estados finales F: q2
Agrega estas seis transiciones:
Estado de origen	Símbolo	Destino
q0	0	q0
q0	1	q1
q1	0	q2
q1	1	q0
q2	0	q2
q2	1	q1


Pulsa Validar autómata. El resultado esperado es AFD completo. Después, pulsa Generar diagrama.
Ejemplos adicionales de comprobación
- AFND: en un par estado-símbolo, selecciona dos destinos al agregar la transición. La etiqueta debe indicar AFND.
- AFD incompleto: deja sin agregar al menos una transición necesaria, sin crear transiciones con varios destinos. La etiqueta debe indicar AFD incompleto.
- Definición inválida: escribe un estado inicial que no aparezca en Q y pulsa Validar autómata. Debe mostrarse un mensaje de definición inválida.
Problemas frecuentes
La aplicación no se abre
- Verifica que seleccionaste el intérprete correcto de Python en VS Code.
- Comprueba que estás ejecutando main.py desde la carpeta del proyecto.
- Revisa el mensaje de error completo en la terminal de VS Code.
Error relacionado con graphviz o dot
- Instala la dependencia de Python con python -m pip install graphviz.
- Instala Graphviz para el sistema operativo.
- En Windows, comprueba que la carpeta bin de Graphviz esté en PATH.
- Reinicia VS Code después de modificar PATH.
No aparece el diagrama
- Valida el autómata y revisa el resultado.
- Comprueba que Graphviz esté instalado y que dot sea accesible.
- Revisa el mensaje de error que muestra la aplicación y la carpeta de salida indicada.
No puedo ver todo el resultado
Usa la barra de desplazamiento del panel Resultado de la validación. El panel está diseñado para mostrar mensajes largos.
Limitaciones actuales
- No se ofrece una entrada específica para transiciones epsilon (ε).
- La detección de AFND se basa en encontrar varios destinos para una misma combinación de estado y símbolo.
- El programa informa de las transiciones faltantes como AFD incompleto; la validación básica de consistencia y la comprobación de completitud son comprobaciones distintas.
- El diagrama se genera como archivo PNG; la interfaz actual no incorpora una vista previa del diagrama dentro de la misma ventana.
Autoría y propósito
Proyecto académico para practicar la representación formal de autómatas finitos, la validación de transiciones y la generación automática de diagramas con Python y Graphviz.