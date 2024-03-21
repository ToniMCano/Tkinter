import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Creamos un estilo personalizado para el Treeview con líneas de rejilla visibles
style = ttk.Style()
style.configure("Treeview", rowheight=25, font=("Arial", 10), bd=1, relief=tk.SOLID)

# Creamos un estilo personalizado para las líneas de rejilla
style.map("Treeview", foreground=[('!selected', 'gray')], background=[('!selected', 'gray')])

# Creamos un Treeview
tree = ttk.Treeview(root, columns=("columna1", "columna2", "columna3"), selectmode="browse", style="Treeview")

# Añadimos encabezados de columnas
tree.heading("#0", text="Columna 0")
tree.heading("#1", text="Columna 1")
tree.heading("#2", text="Columna 2")
tree.heading("#3", text="Columna 3")

# Añadimos algunos elementos al Treeview
for i in range(10):
    tree.insert("", "end", text=f"Item {i}", values=("Valor 1", "Valor 2", "Valor 3"))

# Mostramos la rejilla
tree.grid(row=0, column=0, sticky="nsew")

# Hacemos que la rejilla se expanda con el tamaño de la ventana
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
