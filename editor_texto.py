import tkinter as tk
from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter import colorchooser as ColorChooser
from tkinter import filedialog as FileDialog
import os

root = tk.Tk()
root.title("Editor de Texto")
#root.config(bd = 15)

ruta = ""

text = Text(root)
text.config(padx=5, pady=5, font=("Consolas", 15))
text.pack()

def nuevo():
    global ruta
    ruta = ""
    #escrito = text.get(1.0,END)  # Obtener el contenido de Text - text.focus_set() captura el texto seleccionado.
    text.delete(1.0, END) # Borra el contenido del Text

    root.title("Nuevo Archivo")  # Cambiamos el texto de la ventana principal.

        
def guardar():
    global ruta
    
    mensaje.set("Guardar Archivo")
    
    if ruta != "":
        contenido = text.get(1.0 , "end")   # Obtenemos el texto. Con "end-1c" ("text.get(1.0 , "end-1c")") lo que hacemos es que al guardar no almacene un salto de línea que hace por defecto.
        fichero = open(ruta,"w+")           # Abrimos el archivo en modo escritura para reescribirlo con el nuevo contenido.
        fichero.write(contenido)            # Lo ecribimos
        fichero.close()                     # Lo cerramos para que no se pierdan los cambios.
        root.title(ruta)

    else:
        guardar_como()
        
    mensaje.set("Archvivo Guardado con Éxito.")

    
def guardar_como():
    global ruta
    fichero = FileDialog.asksaveasfile(title = "Guardar Como" , mode = "w" , defaultextension = ".txt",   initialdir = ".")
    if fichero is not None:
        contenido =  text.get(1.0 , "end")
        fichero.write(contenido) # fichero.name, te da la ruta del fichero.
        fichero.close()
    else:
        ruta = ""
        print("no se guarda nada.")
        
    mensaje.set(f"Archivo guardado correctamente")

def abrir():
    global ruta
    text.delete(1.0 , END) # Borramos si hay algo escrito, de lo contrario con el metódo que vamos a usar, añadiría el contenido del archivo a lo que ya hay escrito.
    ruta = FileDialog.askopenfilename(title = "Abrir fichero de texto" , initialdir = "." , filetype = (("Ficheros de Texto" , "*.txt"),)) # initialdir = "." Indica que abra el directorio actual
    if ruta != "":
        file = open(ruta , 'r') # Lo abrimos en modo lectura para no chafarlo.
        contenido = file.read() # capturamos el contenido.
        text.insert("insert" , contenido) # es el método para insertar texto en un Text (lo inserta al final)
        file.close()
        nombre = os.path.basename(ruta) # Obtener el nombre del archivo.
    root.title(ruta + " - Mi Editor") # Se mostrará la ruta del archivo en la ventana principal.
    
    mensaje.set(f"Abriendo {nombre}")
    
    
menubar = Menu(root)
root.config(menu = menubar)

archivo = Menu(menubar , tearoff = 0)

archivo.add_cascade(label = "Nuevo" , command = nuevo)
archivo.add_cascade(label = "Abrir" , command = abrir)
archivo.add_cascade(label = "Guardar" , command = guardar)
archivo.add_cascade(label = "Guardar Como" , command = guardar_como)
archivo.add_separator()
archivo.add_cascade(label = "Salir" , command = root.quit)
    
menubar.add_cascade(label = "Archivo" , menu = archivo )

mensaje = StringVar()

mensaje.set("Aquí irá el mensaje")

label_mensaje = Label(root, textvariable = mensaje)
label_mensaje.pack(side="left")


root.mainloop()




