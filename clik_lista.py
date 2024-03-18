
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3



def on_treeview_click(event):
    item = tree.focus()  # Obtener el ítem seleccionado
    item_text = tree.item(item, "text")  # Obtener el texto del ítem
    print(f"Se hizo clic en la fila: {item_text}")  # Imprimir el texto del ítem

root = tk.Tk()
root.title("Ejemplo Treeview")

tree = ttk.Treeview(root)
tree["columns"] = ("columna1", "columna2")
tree.heading("#0", text="Nombre")
tree.heading("columna1", text="Columna 1")
tree.heading("columna2", text="Columna 2")

# Insertar datos de ejemplo
for i in range(10):
    tree.insert("", "end", text=f"Ítem {i}", values=(f"Valor 1-{i}", f"Valor 2-{i}"))

tree.pack(fill="both", expand=True)

# Enlazar evento de clic en el Treeview
tree.bind("<Button-1>", on_treeview_click)

root.mainloop()
