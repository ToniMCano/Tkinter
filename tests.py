import tkinter as tk
from tkcalendar import Calendar

def seleccionar_elemento(event):
    elemento_seleccionado = event.widget.cget("text") # recibir el texto, con .bind
    etiqueta.config(text=f"Elemento seleccionado: {elemento_seleccionado}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("300x200")

# Crear un Frame
frame = tk.Frame(ventana, bd=1, relief=tk.SOLID)
frame.grid(row=0, column=0, sticky='nsew')

# Agregar elementos al Frame
elementos = [["Elemento 1", "Elemento 2", "Elemento 3", "Elemento 4"] ,
             ["Elemento A1", "Elemento A2", "Elemento A3", "Elemento A4"],
             ["Elemento B1", "Elemento B2", "Elemento B3", "Elemento B4"]
            ]      
     
for i, elemento in enumerate(elementos):
    for e, otro in enumerate(elemento):
        etiqueta = tk.Label(frame, text=otro, bd=1, relief=tk.SOLID)
        etiqueta.grid(row=i, column=e, sticky='nsew')
        etiqueta.bind("<Button-1>", seleccionar_elemento) # con bind, se comporta como un botón

# Crear una etiqueta para mostrar el elemento seleccionado
etiqueta = tk.Label(ventana, text="")
etiqueta.grid(row=1, column=0, sticky='nsew')

def funciona():
    print("Funciona")

def actualizar_texto(opcion):
    menubutton.config(text=opcion)

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


import tkinter as tk
from tkinter import ttk

def toggle_frame_visibility():
    if frame.winfo_ismapped():
        frame.grid_forget()
    else:
        frame.grid(row=1, column=0, sticky="ew")
        frame.lift()  # Elevar el Frame al frente
        
        

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("300x200")

frameboton = ttk.Frame(ventana)
frameboton.grid(row = 0 , column = 0)

# Crear un botón para mostrar/ocultar el Frame
boton = ttk.Button(frameboton, text="Mostrar/Ocultar", command=toggle_frame_visibility)
boton.grid(row=0, column=0, sticky="ew", pady=10)

# Crear un Frame que se mostrará/ocultará
frame = tk.Frame(ventana, bg = "green")

# Agregar contenido al Frame
frame_calendar = tk.Frame(frame)
frame_calendar.grid(row = 0, column = 3)

calendar = Calendar(frame_calendar , selectedmode = "day" , date_pattern = "dd-mm-yyyy")
calendar.grid(row = 0 , column = 0)

# Configurar el tamaño y la posición del Frame
ventana.rowconfigure(1, weight=1)
ventana.columnconfigure(0, weight=1)


test = tk.Label(ventana , text = "Se mueve?" , bg = "red")
test.grid(row=1 , column = 0)

# Ejecutar la ventana
ventana.mainloop()


# Ejecutar la ventana
ventana.mainloop()
