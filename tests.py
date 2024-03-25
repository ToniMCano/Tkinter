import tkinter as tk
from tkinter import *
from tkinter import messagebox as MessageBox
from tkinter import colorchooser as ColorChooser
from tkinter import filedialog as FileDialog

root = tk.Tk()
root.title("Editor de Texto")
root.config(bd = 15)

ruta = ""


def nuevo():
    mensaje.set("Nuevo Archivo")
    
def guardar():
    mensaje.set("Archivo Guardado con Éxito")
    
def guardar_como():
    mensaje.set(f"Archivo guardado como...")

def abrir():
    ruta = FileDialog.askopenfilename(title = "Abrir fichero" , initialdir = "C:/")
    
    mensaje.set(f"Abriendo {ruta}")
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

text = Text(root)
text.config(padx=5 , pady=5 , font = ("Consolas" , 15))
text.pack()

mensaje = StringVar()

mensaje.set("Aquí irá el mensaje")

label_mensaje = Label(root, textvariable = mensaje)
label_mensaje.pack(side="left")


root.mainloop()




