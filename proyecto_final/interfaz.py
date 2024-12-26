import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import compilador  # Importar el módulo completo del compilador

# Función para cargar y redimensionar imágenes
def cargar_icono(ruta, ancho, alto):
    try:
        imagen = Image.open(ruta)
        imagen = imagen.resize((ancho, alto))
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error cargando el icono {ruta}: {e}")
        return None

# Función para analizar el código
def analizar_codigo():
    # Reinicia los errores en el módulo compilador
    compilador.parser_errors = []

    codigo = text_editor.get("1.0", tk.END).strip().replace('\r\n', '\n')
    print("Código a analizar:")
    print(repr(codigo))
    print("Número de líneas:", codigo.count('\n') + 1)

    if not codigo:
        consola.config(state=tk.NORMAL)
        consola.insert(tk.END, "Error: No hay código para analizar.\n")
        consola.config(state=tk.DISABLED)
        return

    # Limpiar la consola
    consola.config(state=tk.NORMAL)
    consola.delete("1.0", tk.END)

    try:
        # Crear una instancia clonada del lexer para generar tokens
        lexer_tokens = compilador.lexer.clone()
        lexer_tokens.input(codigo)

        tokens = []
        while True:
            tok = lexer_tokens.token()
            if not tok:
                break
            tokens.append(f"{tok.type}({tok.value}) en línea {tok.lineno}")
        consola.insert(tk.END, "Tokens generados:\n" + "\n".join(tokens) + "\n\n")

        print("Final lexer_tokens.lineno:", lexer_tokens.lineno)

        # Crear una segunda instancia clonada del lexer para el análisis sintáctico
        lexer_parse = compilador.lexer.clone()
        lexer_parse.input(codigo)

        # Análisis sintáctico pasando la instancia clonada del lexer
        compilador.parser.parse(codigo, lexer=lexer_parse)

        # Mostrar errores sintácticos si los hay
        if compilador.parser_errors:
            consola.insert(tk.END, "Errores de análisis sintáctico:\n" + "\n".join(compilador.parser_errors) + "\n")
        else:
            consola.insert(tk.END, "El análisis sintáctico fue exitoso.\n")
    except SyntaxError as e:
        consola.insert(tk.END, f"Error de análisis sintáctico: {e}\n")
    except Exception as e:
        consola.insert(tk.END, f"Error durante el análisis: {e}\n")

    consola.config(state=tk.DISABLED)

# Función para simular la ejecución del código
def ejecutar_codigo():
    consola.config(state=tk.NORMAL)
    consola.insert(tk.END, "Simulación de ejecución...\n")
    consola.config(state=tk.DISABLED)

# Función para limpiar el editor y la consola
def limpiar():
    text_editor.delete("1.0", tk.END)
    consola.config(state=tk.NORMAL)
    consola.delete("1.0", tk.END)
    consola.config(state=tk.DISABLED)

# Función para abrir un archivo
def abrir_archivo():
    archivo = filedialog.askopenfile(mode='r', filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        contenido = archivo.read()
        text_editor.delete("1.0", tk.END)
        text_editor.insert(tk.END, contenido)

# Función para guardar un archivo
def guardar_archivo():
    archivo = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                       filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        contenido = text_editor.get("1.0", tk.END)
        archivo.write(contenido.strip())
        archivo.close()

# Función para detectar cambios en el editor
def detectar_cambios(event=None):
    boton_ejecutar.config(state=tk.DISABLED)  # Desactiva el botón "Ejecutar" al detectar cambios
    text_editor.edit_modified(False)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Compilador Personalizado")

# Frame para botones
botones_frame = tk.Frame(ventana)
botones_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Cargar imágenes redimensionadas
icono_compilar = cargar_icono("compile.png", 24, 24)
icono_ejecutar = cargar_icono("execute.png", 24, 24)
icono_guardar = cargar_icono("save.png", 24, 24)
icono_limpiar = cargar_icono("clear.png", 24, 24)
icono_abrir = cargar_icono("open.png", 24, 24)

# Botones con íconos
tk.Button(botones_frame, text="Compilar", image=icono_compilar, compound="left", command=analizar_codigo).pack(fill=tk.X, pady=5)
boton_ejecutar = tk.Button(botones_frame, text="Ejecutar", image=icono_ejecutar, compound="left", command=ejecutar_codigo, state=tk.DISABLED)
boton_ejecutar.pack(fill=tk.X, pady=5)
tk.Button(botones_frame, text="Guardar", image=icono_guardar, compound="left", command=guardar_archivo).pack(fill=tk.X, pady=5)
tk.Button(botones_frame, text="Limpiar", image=icono_limpiar, compound="left", command=limpiar).pack(fill=tk.X, pady=5)
tk.Button(botones_frame, text="Abrir archivo", image=icono_abrir, compound="left", command=abrir_archivo).pack(fill=tk.X, pady=5)

# Área de texto para el editor
text_editor = scrolledtext.ScrolledText(ventana, width=80, height=20, undo=True)
text_editor.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
text_editor.bind("<<Modified>>", detectar_cambios)

# Consola de salida
consola = scrolledtext.ScrolledText(ventana, width=80, height=10, state=tk.DISABLED)
consola.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

ventana.mainloop()
