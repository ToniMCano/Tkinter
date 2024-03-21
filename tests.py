import tkinter as tk
from tkinter import ttk

class Main:
    def __init__(self, master):
        self.ventana_principal = master
        self.ventana_principal.title("Ejemplo de Treeview con heading clickeable")

        # Creamos un Frame para contener el Treeview y el botón
        self.frame = ttk.Frame(self.ventana_principal)
        self.frame.pack(fill='both', expand=True)

        # Creamos un Treeview
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(fill='both', expand=True)

        # Configuramos los headings
        self.tree["columns"] = ("name", "age")
        self.tree.heading("#0", text="Cliente")

        # Agregamos algunos datos de ejemplo
        self.tree.insert("", "end", text="Cliente 1", values=("John", 30))
        self.tree.insert("", "end", text="Cliente 2", values=("Alice", 25))
        self.tree.insert("", "end", text="Cliente 3", values=("Bob", 40))

        # Creamos un botón encima del encabezado
        self.heading_button = tk.Button(self.frame, text="Cliente", command=self.on_heading_click)
        self.heading_button.pack(side="top", fill="x")

    def on_heading_click(self):
        print("Heading clickeado")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
