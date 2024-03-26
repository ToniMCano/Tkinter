
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import sqlite3  
from tkcalendar import Calendar




                

class Main:
    def __init__(self, root):
        self.ventana_principal = root
        self.ventana_principal.title("MyCRM")
        self.ventana_principal.resizable(1,1)
        
        # INFO LISTA
        
        self.frame_tree = ttk.Frame(self.ventana_principal)
        self.frame_tree.grid(row = 1 , column = 0 , sticky = "nswe" ,  rowspan=4)
        self.frame_tree.grid_columnconfigure(0, weight=1)
        
        self.info = ttk.Treeview(self.frame_tree,height = 15)
        self.info.grid(row = 0 , column = 0 , sticky = 'nsew')     
        
        self.info["columns"] = ("ultimo_contacto" , "Días_C" , "ultima_venta", "Días:V", "Cantidad" , "Porcentaje")
        self.info.heading("#0" , text = "Cliente")
        self.info.heading("#1" , text  ="Último Contacto")
        self.info.heading("#2" , text = "Días_C")
        self.info.heading("#3" , text = "Ultima Venta")
        self.info.heading("#4" , text = "Días_V")
        self.info.heading("#5" , text = "Cantidad")
        self.info.heading("#6" , text = "Porcentaje")
        
        self.info.column("#0" , width = 150)
        self.info.column("#1" , width = 150)
        self.info.column("#2" , width = 35)
        self.info.column("#3" , width = 150)
        self.info.column("#4" , width = 35)
        self.info.column("#5" , width = 150)
        self.info.column("#6" , width = 150)
        
        self.info.heading("#0", command = self.on_heading_click)
        
        
        style = ttk.Style()
        style.configure("mystyle.Treeview" , highlightthickness = 2 , bd = 0, font = ("Calibri" , 9)) # Modificar la fuente de la tabla
        style.configure("mystyle.Treeview.Heading" , font = ("Calibri" , 9 , 'bold'))   # Modificar la fuente de las cabeceras
        style.layout("mystyle.Treeview" , [("mystyle.Treeview.treearea", {'sticky' : 'nswe'})]) # Eliminar los bordes??
        
        self.ventana_principal.grid_columnconfigure(0, weight=1) # Configuramos el redimensionamiento del frame principal
        self.ventana_principal.grid_columnconfigure(6, weight=1)
        
        # HEADER
        
        self.header = ttk.Frame(self.ventana_principal)
        self.header.grid(row = 0 , column = 0 , columnspan = 8 , pady = 5 , padx = 5 , sticky = 'nsew')
        #self.header.columnconfigure(0, weight = 1)
        
        # AÑADIR CONTACTOS
        
        self.pool = tk.Button(self.header, text = "Pool")
        self.pool.config(height=2 ,width=3)
        self.pool.pack(side="left")
        
        self.pop_up = tk.Button(self.header, text = "PopUp")
        self.pop_up.config(height = 2, width = 3)
        self.pop_up.pack(side="right")
       
        
        # LEAD, CANDIDATE , CONTACT
        
        self.selected_option = StringVar()
        self.selected_option.set("Contact")
        
        self.triangle_icon = Image.open("recursos/triangulo.png")
        self.triangle_icon = self.triangle_icon.resize((10,10))
        self.triangle_icon = ImageTk.PhotoImage(self.triangle_icon)
        
        self.frame_menu_button = Frame(self.header , bg = 'grey' , bd = 1, relief = "sunken")
        self.frame_menu_button.pack(side="left", padx=5)
        
        self._label_icon = tk.Label(self.frame_menu_button , textvariable=self.selected_option , bg = 'white' )
        self._label_icon.config( width = 10, height = 1)
        self._label_icon.grid(row=0,column=0 ) 
        
        self.menu_button = tk.Menubutton(self.frame_menu_button , text = "", image = self.triangle_icon , compound="right",  bg = 'lightgrey' , bd = 1 , relief = "groove")
        #self.menu_button.config(width=10 , height = 1)
        self.menu_button.grid(row = 0 , column = 1 , sticky = "nswe", padx=1) 

        # Crear un Menú y asociarlo al Menubutton
        self.menu = tk.Menu(self.menu_button, tearoff=False)
        self.menu_button.configure(menu=self.menu)

        # Agregar opciones al Menú
        self.menu.add_command(label="Lead", command= lambda: self.update_selected("Lead"))
        self.menu.add_command(label="Candidate", command= lambda: self.update_selected("Candidate"))
        self.menu.add_command(label="Contact", command= lambda: self.update_selected("Contact"))


        # CALENDARIO
        
        self.icon_calendar= Image.open("recursos/calendar.png")
        self.calendar_icon = self.icon_calendar.resize((16,16))
        self.icon_calendar = ImageTk.PhotoImage(self.calendar_icon)

        def toggle_frame_visibility():
            self.frame_container_calendar.config(bg='')
            if self.frame_container_calendar.winfo_ismapped():
                self.frame_container_calendar.grid_forget()
            else:
                self.frame_container_calendar.grid(row=1, column=0, sticky="nswe") # Si lo pongo en 0 desplaza el contenido que en el mismo nivel
                self.frame_container_calendar.lift()  # Elevar el Frame al frente
        

        self.frame_boton = tk.Frame(self.header, bg = 'white' , bd = 1, relief = "sunken")
        self.frame_boton.config(height=1)
        self.frame_boton.pack(side="left" , padx=5)

        self.fecha = StringVar()
        self.fecha.set("25 Abril")
        
        self.label_calendar_button = tk.Label(self.frame_boton , textvariable = self.fecha, bg = 'white')
        self.label_calendar_button.config(width = 15 , height = 1)
        self.label_calendar_button.grid(row = 0, column = 0)
        
        self.boton_fecha = tk.Button(self.frame_boton, image = self.icon_calendar, command=toggle_frame_visibility)
        self.boton_fecha.grid(row=0, column=1, sticky="ew")

        # Crear un Frame que se mostrará/ocultarself.á
        self.frame_container_calendar = tk.Frame(self.ventana_principal)
        self.frame_container_calendar.config(bg='')

        # Agregar contenido al Frame
        self.frame_calendar = tk.Frame(self.frame_container_calendar)
        self.frame_calendar.pack()

        calendar = Calendar(self.frame_calendar , selectedmode = "day" , date_pattern = "dd-mm-yyyy")
        calendar.grid(row = 0 , column = 0)
        
        

        
        # LOG

        self.frame_log = Frame(self.frame_tree , borderwidth = 1 , relief = 'solid')
        self.frame_log.grid(row = 2, column = 0 , sticky = W+E)
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
        
        
        # NÚMERO DE CONTACTOS/ESTADO
        
        self.contacts = StringVar()
        test = [1,2,1,1,1]
        self.contacts.set(f"Contactos: {len(test)}")
        
        self.contacts_number = tk.Frame(self.frame_tree , bg = "lightgrey")
        self.contacts_number.grid(row = 1 , column = 0 , sticky = "nswe")
        
        self.contacts_var = tk.Label(self.contacts_number , textvariable = self.contacts , font = ("" , 10 , 'bold'))
        self.contacts_var.pack(fill = "both" , expand = True, side = "top")
        
        
       
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
        
        self.entry_mobile = ttk.Entry(self.frame_contacto)
        self.entry_mobile.insert(0 , "686289365")
        self.entry_mobile.grid(row = 6 , column = 1 , pady = 2 , padx = 2 , sticky = W+E)
        
        self.mobile_image= Image.open("recursos/mobile.png")
        self.mobile_resize = self.mobile_image.resize((10,16))
        self.mobile_icon = ImageTk.PhotoImage(self.mobile_resize)
        
        self.mobile_button = ttk.Button(self.entry_mobile , image = self.mobile_icon , width = 2 , command = self.capturar )
        self.mobile_button.pack(side = "right")
        
        self.notas = Text(self.frame_contacto)
        self.notas.config(padx = 2 , pady = 2 ,width = 30 , height = 3)
        self.notas.grid(row = 9 , column = 0, columnspan = 2 , sticky = W+E ,ipady = 10, ipadx=15)
        
        self.margin_bottom_contacto = Label(self.frame_contacto , text = "id: 45612" , bg = 'black' , fg = 'white')
        #self.margin_bottom_contacto.config(height= 0)
        self.margin_bottom_contacto.grid(row = 10 , column = 0 , columnspan = 2 , sticky = W+E)
        
        
    def on_heading_click(self):
        print("funciona")
        
    def update_selected(self,option):
        self.selected_option.set(option)
        print("ha entrado")
        
    def capturar(self):
        print(self.entry_mobile.get())


if __name__ == "__main__":
    
    root = Tk()
    app = Main(root)
    root.mainloop()
    
