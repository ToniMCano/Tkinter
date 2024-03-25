import tkinter as tk

def seleccionar_elemento(event):
    elemento_seleccionado = event.widget.cget("text")
    etiqueta.config(text=f"Elemento seleccionado: {elemento_seleccionado}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("300x200")

# Crear un Frame
frame = tk.Frame(ventana, bd=1, relief=tk.SOLID)
frame.grid(row=0, column=0, sticky='nsew')

# Agregar elementos al Frame
elementos = ["Elemento 1", "Elemento 2", "Elemento 3", "Elemento 4"]
for elemento in elementos:
    etiqueta = tk.Label(frame, text=elemento, bd=1, relief=tk.SOLID)
    etiqueta.grid(row=0, column=0, sticky='nsew')
    etiqueta.bind("<Button-1>", seleccionar_elemento)

# Crear una etiqueta para mostrar el elemento seleccionado
etiqueta = tk.Label(ventana, text="")
etiqueta.grid(row=1, column=0, sticky='nsew')

def funciona():
    print("Funciona")

def actualizar_texto(opcion):
    menubutton.config(text=opcion)

ventana_principal = tk.Tk()

header = tk.Frame(ventana, bg='red')
header.grid(row=3, column=0, columnspan=8, sticky='nsew')
header.columnconfigure(0, weight=1)

opcion_seleccionada = tk.StringVar()  # Variable para almacenar la última opción seleccionada
opcion_seleccionada.set("Seleccionar")  # Establecer el valor inicial

menubutton = tk.Menubutton(header, textvariable=opcion_seleccionada)
menubutton.grid(row=4, column=0, sticky='w')  # Alineación a la izquierda

# Crear un Menú y asociarlo al Menubutton
menu = tk.Menu(menubutton, tearoff=False)
menubutton.configure(menu=menu)

# Agregar opciones al Menú
menu.add_command(label="Opción 1", command=lambda: [funciona(), actualizar_texto("Opción 1")])
menu.add_command(label="Opción 2", command=lambda: [funciona(), actualizar_texto("Opción 2")])
menu.add_command(label="Opción 3", command=lambda: [funciona(), actualizar_texto("Opción 3")])


# Ejecutar la ventana
ventana.mainloop()
