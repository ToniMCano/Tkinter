
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3

def funciona():
    print("Funciona")

class Main:
    def __init__(self, root):
        self.ventana_principal = root
        self.ventana_principal.title("MyCRM")
        self.ventana_principal.resizable(1,1)
        
        self.ventana_principal.config(bg ='grey')
        
        self.frame_tree = ttk.Frame(self.ventana_principal)
        self.frame_tree.grid(row = 1 , column = 0 , sticky = "nswe" ,  rowspan=4)
        self.frame_tree.grid_columnconfigure(0, weight=1)
        
        self.info = ttk.Treeview(self.frame_tree,height = 15)
        self.info.grid(row = 0 , column = 0 , sticky = 'nsew')     
        
        self.info["columns"] = ("ultimo_contacto" , "ultima_venta", "Cantidad" , "Porcentaje")
        self.info.heading("#0" , text = "Cliente")
        self.info.heading("#1" , text  ="Último Contacto")
        self.info.heading("#2" , text = "Ultima Venta")
        self.info.heading("#3" , text = "Cantidad")
        self.info.heading("#4" , text = "Porcentaje")
        
        self.info.column("#0" , width = 150)
        self.info.column("#1" , width = 150)
        self.info.column("#2" , width = 150)
        self.info.column("#3" , width = 150)
        self.info.column("#4" , width = 150)
        
        self.info.heading("#0", command = self.on_heading_click)
        
        
        style = ttk.Style()
        style.configure("mystyle.Treeview" , highlightthickness = 2 , bd = 0, font = ("Calibri" , 9)) # Modificar la fuente de la tabla
        style.configure("mystyle.Treeview.Heading" , font = ("Calibri" , 9 , 'bold'))   # Modificar la fuente de las cabeceras
        style.layout("mystyle.Treeview" , [("mystyle.Treeview.treearea", {'sticky' : 'nswe'})]) # Eliminar los bordes
        
        # Configuramos el redimensionamiento del frame principal
        
        self.ventana_principal.grid_columnconfigure(0, weight=1)
        #self.ventana_principal.grid_rowconfigure(0, weight=1)
        self.ventana_principal.grid_columnconfigure(6, weight=1)
        #self.ventana_principal.grid_rowconfigure(1, weight=2)
        
        self.header = Frame(self.ventana_principal , bg = 'red')
        self.header.grid(row = 0 , column = 0 , columnspan = 8 , sticky = 'nsew')
        self.header.columnconfigure(0, weight = 1)
        
        
        menubutton = tk.Menubutton(self.header, text="Seleccionar")
        menubutton.grid(row = 0 , column = 0 , sticky= W)

        # Crear un Menú y asociarlo al Menubutton
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)

        # Agregar opciones al Menú
        menu.add_command(label="Opción 1", command= funciona)
        menu.add_command(label="Opción 2", command= funciona)
        menu.add_command(label="Opción 3", command= funciona)


        self.frame_log = Frame(self.frame_tree , borderwidth = 1 , relief = 'solid')
        self.frame_log.grid(row = 1, column = 0 , sticky = W+E)
        self.frame_log.grid_columnconfigure(1, weight=1)
        
        self.texto_log =Text(self.frame_log)
        self.texto_log.config(height = 3 , width = 80)
        self.texto_log.grid(row = 1 , column = 1, rowspan = 2 , sticky = W+E, padx = 5    , pady = 5)
        
        self.next_contact = ttk.Button(self.frame_log , text = "Next Contact")
        self.next_contact.grid(row = 1, column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_pop_up = ttk.Button(self.frame_log , text = "Pop Up")
        self.boton_pop_up.grid(row = 2 , column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_log = ttk.Button(self.frame_log , text = "Log")
        self.boton_log.grid(row = 1 , column = 7, padx = 2 , pady= 2 , sticky = "nswe" , rowspan = 2)
       
        # FRAME EMPRESA
        
        self.frame_empresa =Frame(self.ventana_principal  , borderwidth=1, relief="solid") 
        self.frame_empresa.grid(row = 1 , column = 5 , pady = 0 , sticky = "nswe" , columnspan = 5 , rowspan = 2) # sticky="nswe" Se expande en todas las driecciones.
        
        self.frame_empresa.grid_columnconfigure(1, weight=1)
        self.frame_empresa.grid_columnconfigure(0, weight=1)
        
        self.encabezado_empresa = tk.Label(self.frame_empresa, text="Empresa", bg='black', fg='white')
        self.encabezado_empresa.grid(row = 0 , column = 0 , columnspan = 2  , sticky=W+E)
        
        self.label_nombre_empreasa = ttk.Label(self.frame_empresa, text = "Empresa" , font = ("Calibri" , 9 , 'bold'))
        self.label_nombre_empreasa.grid(row = 1 , column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_nombre_empresa = ttk.Entry(self.frame_empresa)
        self.entry_nombre_empresa.insert(0 , "Gusanitos,S.A") # Es lo mismo que placeholder
        self.entry_nombre_empresa.grid(row = 2, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        
        
        self.label_empleados_empresa = ttk.Label(self.frame_empresa , text = "Número de Empleados", font = ("Calibri" , 9 , 'bold'))
        self.label_empleados_empresa.grid(row = 1 , column = 1 , sticky = W+E , padx = 2  , pady = 2)
        
        self.entry_empleados_empresa = ttk.Entry(self.frame_empresa)
        self.entry_empleados_empresa.insert(0,"50-50")
        self.entry_empleados_empresa.grid(row = 2 , column = 1 , padx = 2  , pady = 2 , sticky = W+E)
                
        self.label_actividad_empresa = ttk.Label(self.frame_empresa , text = "Actividad", font = ("Calibri" , 9 , 'bold'))
        self.label_actividad_empresa.grid(row = 3 , column = 0, sticky=W+E , padx = 2 , pady = 2)
        
        self.entry_actividad_empresa = ttk.Entry(self.frame_empresa)
        self.entry_actividad_empresa.insert(0, "Arquitectura e Ingeniería")
        self.entry_actividad_empresa.grid(row = 4 , column = 0, columnspan= 2 , sticky = W+E , padx = 2  , pady = 2) 
        
        self.label_web_empresa = ttk.Label(self.frame_empresa , text = "Web", font = ("Calibri" , 9 , 'bold'))
        self.label_web_empresa.grid(row = 5, column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_web_empresa = ttk.Entry(self.frame_empresa)
        self.entry_web_empresa.insert(0,"www.google.com")
        self.entry_web_empresa.grid(row = 6, column= 0 , padx = 2  , pady = 2 , sticky = W+E)
        
        self.label_mail_empresa = ttk.Label(self.frame_empresa , text = "Mail", font = ("Calibri" , 9 , 'bold'))
        self.label_mail_empresa.grid(row = 5, column = 1, sticky = W+E , padx = 2 , pady = 2)
        
        self.entry_mail_empresa = ttk.Entry(self.frame_empresa)
        self.entry_mail_empresa.insert(0,"provwork2015@gmail.com")
        self.entry_mail_empresa.grid(row = 6 , column = 1,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_telefono_empresa = ttk.Label(self.frame_empresa , text = "Teléfono", font = ("Calibri" , 9 , 'bold'))
        self.label_telefono_empresa.grid(row = 7, column = 0 , sticky = W+E , padx = 2 ,  pady = 2)
        
        self.entry_telefono_empresa = ttk.Entry(self.frame_empresa)
        self.entry_telefono_empresa.insert(0,"965125477")
        self.entry_telefono_empresa.grid(row = 8, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.label_telefono_dos = ttk.Label(self.frame_empresa , text = "Otro Teléfono", font = ("Calibri" , 9 , 'bold'))
        self.label_telefono_dos.grid(row = 7, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.entry_telefono_dos = ttk.Entry(self.frame_empresa)
        self.entry_telefono_dos.insert(0,"684458253")
        self.entry_telefono_dos.grid(row = 8, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.margin_bottom = ttk.Label(self.frame_empresa)
        self.margin_bottom.grid(row = 9 ,column= 0 , columnspan=2, sticky = W+E , pady =1)
        
        
        #FRAME CONTACTO
        
        self.frame_contacto = ttk.Frame(self.ventana_principal , borderwidth = 1, relief = 'solid')
        self.frame_contacto.grid(row = 3 , column = 5  , columnspan=2 , rowspan = 2 , sticky='nsew')
        
        self.frame_contacto.grid_columnconfigure(1, weight=1)
        self.frame_contacto.grid_columnconfigure(0, weight=1)
        
        
        self.encabezado_contacto = Label(self.frame_contacto , text = "Contacto" ,bg = "black" , fg = 'white')
        self.encabezado_contacto.grid(row = 0 , column = 0 , columnspan = 2  ,sticky=W+E)
        
        self.label_nombre_contacto = ttk.Label(self.frame_contacto , text = "Nombre  ")
        self.label_nombre_contacto.grid(row = 1 , column = 0 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_nombre_contacto = ttk.Entry(self.frame_contacto)
        self.entry_nombre_contacto.insert(0 , "Pepitos")
        self.entry_nombre_contacto.grid(row = 2 , column = 0 ,  padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_apellido_contacto = ttk.Label(self.frame_contacto , text = "Apellido")
        self.label_apellido_contacto.grid(row = 1 , column = 1 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_apellido_contacto = ttk.Entry(self.frame_contacto)
        self.entry_apellido_contacto.insert(0, "Palotes")
        self.entry_apellido_contacto.grid(row = 2 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_cargo = ttk.Label(self.frame_contacto, text = "Cargo")
        self.label_cargo.grid(row = 3 , column = 0, padx = 2 , pady = 2 , sticky = W+E)
        self.entry_cargo = ttk.Entry(self.frame_contacto)
        self.entry_cargo.insert(0, "Director General")
        self.entry_cargo.grid(row = 4 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        
        self.label_mail_contacto = ttk.Label(self.frame_contacto , text = "Mail")
        self.label_mail_contacto.grid(row = 3 , column = 1 , padx = 2 , pady = 2  , sticky = W+E)
        
        self.entry_mail_contacto = ttk.Entry(self.frame_contacto)
        self.entry_mail_contacto.insert(0,"pepito.palotes@gusanitosa.com")
        self.entry_mail_contacto.grid(row = 4, column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_telefono_contacto = ttk.Label(self.frame_contacto , text = "Teléfono")
        self.label_telefono_contacto.grid(row = 5 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        
        self.entry_telefono_contacto = ttk.Entry(self.frame_contacto)
        self.entry_telefono_contacto.insert(0, "963278165")
        self.entry_telefono_contacto.grid(row = 6 , column = 0 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_movil = ttk.Label(self.frame_contacto , text = "Móvil")
        self.label_movil.grid(row = 5 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_movil = ttk.Entry(self.frame_contacto)
        self.entry_movil.insert(0 , "686289365")
        self.entry_movil.grid(row = 6 , column = 1 , pady = 2 , padx = 2 , sticky = W+E)
        
        self.boton = ttk.Button(self.entry_movil , text = 8 , width = 2)
        self.boton.pack(side = "right")
        
        self.notas = Text(self.frame_contacto)
        self.notas.config(padx = 2 , pady = 2 ,width = 30 , height = 3)
        self.notas.grid(row = 9 , column = 0, columnspan = 2 , sticky = W+E ,ipady = 5)
        
        self.margin_bottom_contacto = Label(self.frame_contacto , text = "id: 45612" , bg = 'black' , fg = 'white')
        #self.margin_bottom_contacto.config(height= 0)
        self.margin_bottom_contacto.grid(row = 10 , column = 0 , columnspan = 2 , sticky = W+E)
        
        
    def on_heading_click(self):
        print("funciona")


if __name__ == "__main__":
    
    root = Tk()
    app = Main(root)
    root.mainloop()
    
