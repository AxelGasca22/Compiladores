import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import ttk
from tkinter import PhotoImage
from compilador import tokenize, analizadorLL1
from PIL import Image, ImageTk

# Función para cargar y redimensionar imágenes
def cargar_icono(ruta, ancho, alto):
    imagen = Image.open(ruta)
    imagen = imagen.resize((ancho, alto))  # Redimensionar (ya no se requiere Image.ANTIALIAS)
    return ImageTk.PhotoImage(imagen)

# Funciones del compilador (placeholders)
def analizar_codigo():
    codigo = text_editor.get("1.0", tk.END).strip()
    if not codigo:
        consola.config(state=tk.NORMAL)
        consola.insert(tk.END, "Error: No hay código para compilar.\n")
        consola.config(state=tk.DISABLED)
        boton_ejecutar.config(state=tk.DISABLED)  # Desactiva el botón "Ejecutar"
        return

    tokens = tokenize(codigo)  # Tokeniza el código ingresado
    consola.config(state=tk.NORMAL)
    consola.delete("1.0", tk.END)  # Limpia la consola
    if analizadorLL1(tokens):  # Valida los tokens con el analizador LL1
        consola.insert(tk.END, "La expresión es válida.\n")
        boton_ejecutar.config(state=tk.NORMAL)  # Activa el botón "Ejecutar"
    else:
        consola.insert(tk.END, "La expresión no es válida.\n")
        boton_ejecutar.config(state=tk.DISABLED)  # Desactiva el botón "Ejecutar"
    consola.config(state=tk.DISABLED)


def ejecutar_codigo():
    consola.config(state=tk.NORMAL)
    consola.insert(tk.END, "Simulación de ejecución...\n")
    consola.config(state=tk.DISABLED)

def limpiar():
    text_editor.delete("1.0", tk.END)
    consola.config(state=tk.NORMAL)
    consola.delete("1.0", tk.END)
    consola.config(state=tk.DISABLED)
    boton_ejecutar.config(state=tk.DISABLED)  # Desactiva el botón "Ejecutar"

def abrir_archivo():
    archivo = filedialog.askopenfile(mode='r', filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        contenido = archivo.read()
        text_editor.delete("1.0", tk.END)
        text_editor.insert(tk.END, contenido)

def guardar_archivo():
    archivo = filedialog.asksaveasfile(mode='w', defaultextension=".txt",
                                       filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        contenido = text_editor.get("1.0", tk.END)
        archivo.write(contenido.strip())
        archivo.close()
        
def detectar_cambios(event=None):
    # Desactiva el botón "Ejecutar" si se modifica el contenido
    boton_ejecutar.config(state=tk.DISABLED)

    # Restablece el flag de "modificado" para futuros eventos
    text_editor.edit_modified(False)

#####################################################################################    
# Funciones de edición
def deshacer():
    text_editor.edit_undo()

def rehacer():
    text_editor.edit_redo()

def cortar():
    text_editor.event_generate("<<Cut>>")

def copiar():
    text_editor.event_generate("<<Copy>>")

def pegar():
    text_editor.event_generate("<<Paste>>")

def seleccionar_todo():
    text_editor.tag_add("sel", "1.0", tk.END)

#####################################################################################
#Funcion de buscar
def buscar():
    palabra = tk.simpledialog.askstring("Buscar", "Introduce la palabra o carácter a buscar:")
    if palabra:
        text_editor.tag_remove("highlight", "1.0", tk.END)  # Limpia resaltados anteriores
        indice_inicio = "1.0"
        while True:
            indice_inicio = text_editor.search(palabra, indice_inicio, stopindex=tk.END)
            if not indice_inicio:  # Si no se encuentra más, rompe el bucle
                break
            indice_fin = f"{indice_inicio}+{len(palabra)}c"
            text_editor.tag_add("highlight", indice_inicio, indice_fin)
            indice_inicio = indice_fin  # Continúa buscando después del último resultado
        text_editor.tag_config("highlight", background="yellow", foreground="black")


#####################################################################################

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Compilador Personalizado")

# Cambiar colores y fuentes para un tema rojo
# ventana.option_add('*Menu.background', '#ff0000')
# ventana.option_add('*Menu.foreground', '#ffffff')
# ventana.option_add('*Menu.font', ('Helvetica', 12))
# ventana.option_add('*Menu.activeBackground', '#ff6666')
# ventana.option_add('*Menu.activeForeground', '#ffffff')

# Frame para botones (lado izquierdo)
botones_frame = tk.Frame(ventana)
botones_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Botones de control dentro del frame
# Cargar imágenes redimensionadas
icono_compilar = cargar_icono("compile.png", 24, 24)
icono_ejecutar = cargar_icono("execute.png", 24, 24)
icono_guardar = cargar_icono("save.png", 24, 24)
icono_limpiar = cargar_icono("clear.png", 24, 24)
icono_abrir = cargar_icono("open.png", 24, 24)

# Botones con íconos redimensionados
tk.Button(botones_frame, text="Compilar", image=icono_compilar, compound="left", command=analizar_codigo).pack(fill=tk.X, pady=5)
boton_ejecutar = tk.Button(botones_frame, text="Ejecutar", image=icono_ejecutar, compound="left", command=ejecutar_codigo, state=tk.DISABLED)
boton_ejecutar.pack(fill=tk.X, pady=5)
boton_guardar = tk.Button(botones_frame, text="Guardar", image=icono_guardar, compound="left", command=guardar_archivo, state=tk.DISABLED)
boton_guardar.pack(fill=tk.X, pady=5)
tk.Button(botones_frame, text="Limpiar", image=icono_limpiar, compound="left", command=limpiar).pack(fill=tk.X, pady=5)
tk.Button(botones_frame, text="Abrir archivo", image=icono_abrir, compound="left", command=abrir_archivo).pack(fill=tk.X, pady=5)




# Área de texto para el editor
text_editor = scrolledtext.ScrolledText(ventana, width=80, height=20, undo=True)
#text_editor = scrolledtext.ScrolledText(ventana, width=80, height=20)
text_editor.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
# Vincular el evento de cambios en el texto
text_editor.bind("<<Modified>>", detectar_cambios)

# Consola de salida
consola = scrolledtext.ScrolledText(ventana, width=80, height=10, state=tk.DISABLED)
consola.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Menú principal
menu_principal = tk.Menu(ventana)
ventana.config(menu=menu_principal)

# Menú de Edición
menu_edicion = tk.Menu(menu_principal, tearoff=0)
menu_edicion.add_command(label="Deshacer", command=deshacer)
menu_edicion.add_command(label="Rehacer", command=rehacer)
menu_edicion.add_separator()  # Línea separadora
menu_edicion.add_command(label="Cortar", command=cortar)
menu_edicion.add_command(label="Copiar", command=copiar)
menu_edicion.add_command(label="Pegar", command=pegar)
menu_edicion.add_separator()  # Línea separadora
menu_edicion.add_command(label="Seleccionar todo", command=seleccionar_todo)

# Agregar el menú de Edición al menú principal
menu_principal.add_cascade(label="Edición", menu=menu_edicion)

# Menú de Buscar
menu_buscar = tk.Menu(menu_principal, tearoff=0)
menu_buscar.add_command(label="Buscar", command=buscar)

# Agregar el menú de Buscar al menú principal
menu_principal.add_cascade(label="Buscar", menu=menu_buscar)




ventana.mainloop()
