import tkinter as tk
from tkinter import *

root = tk.Tk()
root.title("Cafetería")
root.config(bd = 15)


menu_bar = Menu(root)
root.config(menu = menu_bar )


file_menu = Menu(menu_bar , tearoff = 0)
edit_menu = Menu(menu_bar , tearoff = 0)
help_menu = Menu(menu_bar , tearoff = 0)

file_menu.add_cascade(label = "Nuevo")
file_menu.add_cascade(label = "Abrir")
file_menu.add_cascade(label = "Guardar")
file_menu.add_cascade(label = "Cerrar")
file_menu.add_separator()
file_menu.add_command(label = "Salir" , command = root.quit )

edit_menu.add_cascade(label = "Cortar")
edit_menu.add_cascade(label = "Copiar")
edit_menu.add_cascade(label = "Pegar")

menu_bar.add_cascade(label = "Archivo" , menu = file_menu)
menu_bar.add_cascade(label = "Editar" , menu = edit_menu)
menu_bar.add_cascade(label = "Ayuda" , menu = help_menu)

help_menu.add_cascade(label = "Ayuda")
help_menu.add_separator()
help_menu.add_cascade(label = "Acerca de ...")


root.mainloop()




