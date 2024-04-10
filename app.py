
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
import webbrowser
from models import Employee , Client , Contact , ContactPerson
import db
import openpyxl
from sqlalchemy import and_ , or_  
from actions import Actions as act
from datetime import datetime
import locale
from tkinter import messagebox as mb
locale.setlocale(locale.LC_ALL, '')


 

 
def nace_list():
    excel = openpyxl.load_workbook("recursos\\NACE.xlsx")

    nace = excel['Hoja 1']['A']

    lista_nace = []

    for x in nace:
        valor = x.value.split(" - ")
        
        if len(valor[0]) > 1:
            lista_nace.append( valor[0] + " " + valor[1])
        
    return lista_nace
    

class Main:
    def __init__(self, root):
        self.ventana_principal = root
        self.ventana_principal.title("MyCRM")
        self.ventana_principal.resizable(1,1)
        self.ventana_principal.geometry('1200x800')
        self.center_window(self.ventana_principal)
        
        # INFO LISTA
        
        style = ttk.Style()
        style.configure("mystyle.Treeview" , highlightthickness = 2 , bd = 0, font = ("Calibri" , 9), bg = "lightgrey" ) # Modificar la fuente de la tabla
        style.configure("mystyle.Treeview.Heading" , font = ("Calibri" , 9 , 'bold'))   # Modificar la fuente de las cabeceras
        style.layout("mystyle.Treeview" , [("mystyle.Treeview.treearea", {'sticky' : 'nswe'})]) # Eliminar los bordes??
        self.frame_tree = ttk.Frame(self.ventana_principal)
        self.frame_tree.grid(row = 1 , column = 0 , sticky = "nswe" ,  rowspan=3)
        self.frame_tree.grid_columnconfigure(0, weight=1)
        
        self.info = ttk.Treeview(self.frame_tree,height = 20 , style="mystyle.Treeview")
        self.info.grid(row = 0 , column = 0 , sticky = 'nsew')     
        
        self.info["columns"] = ("Estado" , "ultimo_contacto" , "Días_C" , "ultima_venta", "Días_V", "Cantidad" , "Porcentaje")
        self.info.heading("#0" , text = "Estado" , command = lambda: self.on_heading_click("state"))
        self.info.heading("#1" , text = "Cliente" , command = lambda: self.on_heading_click("client"))
        self.info.heading("#2" , text  ="Último Contacto" , command = lambda: self.on_heading_click("last_contact"))
        self.info.heading("#3" , text = "Días_C" , command = lambda: self.on_heading_click("days_contact"))
        self.info.heading("#4" , text = "Ultima Venta" , command = lambda: self.on_heading_click("last_sale"))
        self.info.heading("#5" , text = "Días_V" , command = lambda: self.on_heading_click("days_sale"))
        self.info.heading("#6" , text = "Cantidad" , command = lambda: self.on_heading_click("amount"))
        self.info.heading("#7" , text = "Porcentaje" , command = lambda: self.on_heading_click("percentage"))
        
        self.info.column("#0" , width = 35)
        self.info.column("#1" , width = 150)
        self.info.column("#2" , width = 50)
        self.info.column("#3" , width = 10)
        self.info.column("#4" , width = 50)
        self.info.column("#5" , width = 10)
        self.info.column("#6" , width = 20)
        self.info.column("#7" , width = 20)
        
        
        self.ventana_principal.grid_columnconfigure(0, weight=1) # Configuramos el redimensionamiento del frame principal
        self.ventana_principal.grid_columnconfigure(5, weight=1)
        self.ventana_principal.grid_rowconfigure(3, weight=1)
        
        #IMAGENES 
        
        self.mobile_image= Image.open("recursos/mobile.png")
        self.mobile_resize = self.mobile_image.resize((10,16))
        self.mobile_icon = ImageTk.PhotoImage(self.mobile_resize)
                
        self.triangle_icon = Image.open("recursos/triangulo.png")
        self.triangle_icon = self.triangle_icon.resize((10,10))
        self.triangle_icon = ImageTk.PhotoImage(self.triangle_icon)
        
        self.icon_calendar= Image.open("recursos/calendar.png")
        self.calendar_icon = self.icon_calendar.resize((16,16))
        self.icon_calendar = ImageTk.PhotoImage(self.calendar_icon)
        
        self.web_icon = Image.open("recursos/web2.png")
        self.web_icon = self.web_icon.resize((13,13))
        self.web_icon = ImageTk.PhotoImage(self.web_icon)
        
        self.mail_image = Image.open("recursos/mail.png")
        self.mail_icon = self.mail_image.resize((16,12))
        self.mail_icon = ImageTk.PhotoImage(self.mail_icon)
        
        self.phone_image = Image.open("recursos/phone.png")
        self.phone_icon = self.phone_image.resize((12,12))
        self.phone_icon = ImageTk.PhotoImage(self.phone_icon)
        
        self.cross_image = Image.open("recursos/cross.png")
        self.cross_image.resize((12,12))
        self.cross_icon = ImageTk.PhotoImage(self.cross_image)
        
        # HEADER
        
        self.header = ttk.Frame(self.ventana_principal)
        self.header.grid(row = 0 , column = 0 , columnspan = 6, pady = 5 , padx = 5 , sticky = W+E)
        self.header.columnconfigure(10, weight = 1)
     
        # LEAD, CANDIDATE , CONTACT
        
        self.selected_option = StringVar()
        self.selected_option.set("Contact")
        
        self.employee = ttk.Combobox(self.header ,state = "readonly",values=["AMC", "MMG", "ITL"] , width= 10)
        self.employee.configure(background='lightblue')
        self.employee.current(newindex=0)
               
        self.employee.grid(row = 0 , column = 3 , padx = 5)
        self.employee.bind("<<ComboboxSelected>>" , self.test)

        self.combo_state = ttk.Combobox(self.header ,state = "readonly",values=["Lead", "Candidate", "Contact"] , width= 10)
        self.combo_state.configure(background='lightblue')
        self.combo_state.current(newindex=0)
        #self.combo_state.config(background = 'white')
        self.combo_state.grid(row = 0 , column = 4 , padx = 5)
        self.combo_state.bind("<<ComboboxSelected>>" , self.state)

        # CALENDAR
        
        # Crear un Frame que se mostrará/ocultará self.frame_button
        self.frame_container_calendar = tk.Frame(self.ventana_principal)

        # Agregar contenido al Frame

        self.calendar = Calendar(self.frame_container_calendar , selectedmode = "day" , date_pattern = "dd-mm-yyyy")
        self.calendar.grid(row = 0 , column = 0)
        self.calendar_date = self.calendar.bind("<<CalendarSelected>>", lambda e: self.calendar_selected_date(e))
        
        self.frame_calendar_button = tk.Frame(self.header, bg = 'white' , bd = 1, relief = "sunken")
        self.frame_calendar_button.config(height=1)
        self.frame_calendar_button.grid(row = 0 , column = 5 , padx = 5)

        self.fecha = StringVar()
        self.fecha.set(datetime.now().strftime("%d %B").title())
        
        
        self.label_calendar_button = tk.Label(self.frame_calendar_button , textvariable = self.fecha, bg = 'white')
        self.label_calendar_button.config(width = 15 , height = 1)
        self.label_calendar_button.grid(row = 0, column = 6)
        
        self.boton_fecha = tk.Button(self.frame_calendar_button, image = self.icon_calendar, command = self.toggle_frame_visibility)
        self.boton_fecha.config(cursor = 'arrow')
        self.boton_fecha.grid(row=0, column=1, sticky="ew")

        # AÑADIR CONTACTOS DESDE POOL
        
        self.add_company = tk.Button(self.header , text = 'Add\nCompany' , font = ("Calibri" , 9 ,'bold') , command = self.add_company) 
        #self.add_company.config(height = 47, width = 47)
        self.add_company.grid(row = 0 , column = 0 , padx = 5) 
        
        self.pool = tk.Button(self.header, text = "Pool")
        self.pool.config(cursor = 'arrow')
        self.pool.config(height=2 ,width=5)
        self.pool.grid(row = 0 , column = 1 , padx = 5)
        
        self.pop_up = tk.Button(self.header, text = "PopUp")
        self.pop_up.config(cursor = 'arrow')
        self.pop_up.config(height = 2, width = 5)
        self.pop_up.grid(row = 0 , column = 10 , padx = 5 , sticky = E)
        

        
        # LOG

        self.frame_log = Frame(self.frame_tree , borderwidth = 1 , relief = 'solid')
        self.frame_log.grid(row = 2, column = 0 , sticky = W+E)
        self.frame_log.grid_columnconfigure(1, weight=1)
        
        self.texto_log =Text(self.frame_log)
        self.texto_log.config(height = 3 , width = 80)
        self.texto_log.grid(row = 1 , column = 1, rowspan = 2 , sticky = W+E, padx = 5    , pady = 5)
        
        self.next_contact = ttk.Button(self.frame_log , text = "Next Contact")
        self.next_contact.config(cursor = 'arrow')
        self.next_contact.grid(row = 1, column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_pop_up = ttk.Button(self.frame_log , text = "Pop Up")
        self.boton_pop_up.config(cursor = 'arrow')
        self.boton_pop_up.grid(row = 2 , column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_log = ttk.Button(self.frame_log , text = "Log")
        self.boton_log.config(cursor = 'arrow')
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
        
        self.frame_empresa = tk.Frame(self.ventana_principal  , borderwidth=1, relief="solid") 
        self.frame_empresa.grid(row = 1 , column = 5 , pady = 0 , sticky = "nswe" , columnspan = 4, rowspan = 2) # sticky="nswe" Se expande en todas las driecciones.
        
        self.frame_empresa.grid_columnconfigure(1, weight=1)
        self.frame_empresa.grid_columnconfigure(0, weight=1)
        
        self.encabezado_empresa = tk.Label(self.frame_empresa, text="Empresa", bg='black', fg='white')
        self.encabezado_empresa.grid(row = 0 , column = 0 , columnspan = 3  , sticky=W+E)
        
        self.label_nombre_empreasa = ttk.Label(self.frame_empresa, text = "Empresa" , font = ("Calibri" , 9 , 'bold'))
        self.label_nombre_empreasa.grid(row = 1 , column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_nombre_empresa = ttk.Entry(self.frame_empresa)
        self.entry_nombre_empresa.insert(0 , "Gusanitos,S.A") # Es lo mismo que placeholder
        self.entry_nombre_empresa.grid(row = 2, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        
        
        self.label_empleados_empresa = ttk.Label(self.frame_empresa , text = "Número de Empleados", font = ("Calibri" , 9 , 'bold'))
        self.label_empleados_empresa.grid(row = 1 , column = 1 , sticky = W+E , padx = 2  , pady = 2)
        
        self.entry_empleados_empresa = ttk.Entry(self.frame_empresa)
        self.entry_empleados_empresa.insert(0,"50-100")
        self.entry_empleados_empresa.grid(row = 2 , column = 1 , padx = 2  , pady = 2 , sticky = W+E)
                
        self.label_actividad_empresa = ttk.Label(self.frame_empresa , text = "Actividad", font = ("Calibri" , 9 , 'bold'))
        self.label_actividad_empresa.grid(row = 3 , column = 0, sticky=W+E , padx = 2 , pady = 2)
        
        self.entry_actividad_empresa = ttk.Entry(self.frame_empresa)
        self.entry_actividad_empresa.insert(0, "Arquitectura e Ingeniería")
        self.entry_actividad_empresa.grid(row = 4 , column = 0, columnspan= 2 , sticky = W+E , padx = 2  , pady = 2) 
        
        self.label_web = ttk.Label(self.frame_empresa , text = "Web", font = ("Calibri" , 9 , 'bold'))
        self.label_web.grid(row = 5, column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_web = ttk.Entry(self.frame_empresa)
        self.entry_web.insert(0,"www.google.com")
        self.entry_web.grid(row = 6, column= 0 , padx = 2  , pady = 2 , sticky = W+E)
        
        self.web_button = ttk.Button(self.entry_web ,  image = self.web_icon , command = self.abrir_enlace)
        self.web_button.config(cursor = 'arrow')
        self.web_button.pack(side = "right")
        
        self.label_mail = ttk.Label(self.frame_empresa , text = "Mail", font = ("Calibri" , 9 , 'bold'))
        self.label_mail.grid(row = 5, column = 1, sticky = W+E , padx = 2 , pady = 2)
        
        self.entry_mail_empresa = ttk.Entry(self.frame_empresa)
        self.entry_mail_empresa.insert(0,"provwork2015@gmail.com")
        self.entry_mail_empresa.grid(row = 6 , column = 1,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        
        
        self.mail_button = ttk.Button(self.entry_mail_empresa, image = self.mail_icon)
        self.mail_button.config(cursor = 'arrow')
        self.mail_button.pack(side = "right")
        
        self.label_phone = ttk.Label(self.frame_empresa , text = "Teléfono", font = ("Calibri" , 9 , 'bold'))
        self.label_phone.grid(row = 7, column = 0 , sticky = W+E , padx = 2 ,  pady = 2)
        
        self.entry_telefono_empresa = ttk.Entry(self.frame_empresa)
        self.entry_telefono_empresa.insert(0,"965125477")
        self.entry_telefono_empresa.grid(row = 8, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.phone_button = ttk.Button(self.entry_telefono_empresa , image = self.phone_icon)
        self.phone_button.config(cursor = 'arrow')
        self.phone_button.pack(side = "right")
        
        self.label_phone2 = ttk.Label(self.frame_empresa , text = "Otro Teléfono", font = ("Calibri" , 9 , 'bold'))
        self.label_phone2.grid(row = 7, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.entry_phone2 = ttk.Entry(self.frame_empresa)
        self.entry_phone2.insert(0,"684458253")
        self.entry_phone2.grid(row = 8, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.phone2_button = ttk.Button(self.entry_phone2 , image = self.mobile_icon)
        self.phone2_button.config(cursor = 'arrow')
        self.phone2_button.pack(side = "right")
        
        self.margin_bottom = ttk.Label(self.frame_empresa)
        self.margin_bottom.grid(row = 9 ,column= 0 , columnspan=2, sticky = W+E , pady =1)
        
        
        #FRAME CONTACTO
        
        self.contact_frame = ttk.Frame(self.ventana_principal , borderwidth = 1, relief = 'solid')
        self.contact_frame.grid(row = 3 , column = 5  , columnspan=2 , rowspan = 2 , sticky='nsew')
        
        self.contact_frame.grid_columnconfigure(1, weight=1)
        self.contact_frame.grid_columnconfigure(0, weight=1)
        self.contact_frame.grid_columnconfigure(0, weight=1)      
        
        self.contact_header = Label(self.contact_frame , text = "Contacto" ,bg = "black" , fg = 'white')
        self.contact_header.grid(row = 0 , column = 0 , columnspan = 2  ,sticky=W+E)
        
        self.new_contact = tk.Button(self.contact_header , text = "+"  , font = ("", 12 , "bold") , bg = "white" , bd =0 , command = self.create_contact)
        self.new_contact.config(cursor = 'arrow')
        self.new_contact.config(height=1 , padx=1 , pady = 1)
        self.new_contact.pack(side = "right")
        
        self.other_contact = tk.Button(self.contact_header , image = self.triangle_icon , fg = "white" , font = ("", 12 , "bold") , bg = "white" , bd =0)
        self.other_contact.config(cursor = 'arrow')
        self.other_contact.config(height=10 , padx=5)
        self.other_contact.pack(side = "left" , fill = "y")
        
        self.label_nombre_contacto = ttk.Label(self.contact_frame , text = "Nombre  ")
        self.label_nombre_contacto.grid(row = 1 , column = 0 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_nombre_contacto = ttk.Entry(self.contact_frame)
        self.entry_nombre_contacto.insert(0 , "Pepitos")
        self.entry_nombre_contacto.grid(row = 2 , column = 0 ,  padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_apellido_contacto = ttk.Label(self.contact_frame , text = "Apellidos")
        self.label_apellido_contacto.grid(row = 1 , column = 1 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_apellido_contacto = ttk.Entry(self.contact_frame)
        self.entry_apellido_contacto.insert(0, "Palotes")
        self.entry_apellido_contacto.grid(row = 2 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.label_cargo = ttk.Label(self.contact_frame, text = "Cargo")
        self.label_cargo.grid(row = 3 , column = 0, padx = 2 , pady = 2 , sticky = W+E)
        self.entry_cargo = ttk.Entry(self.contact_frame)
        self.entry_cargo.insert(0, "Director General")
        self.entry_cargo.grid(row = 4 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        
        self.label_mail_contacto = ttk.Label(self.contact_frame , text = "Mail")
        self.label_mail_contacto.grid(row = 3 , column = 1 , padx = 2 , pady = 2  , sticky = W+E)
        
        self.entry_contact_mail = ttk.Entry(self.contact_frame)
        self.entry_contact_mail.insert(0,"pepito.palotes@gusanitosa.com")
        self.entry_contact_mail.grid(row = 4, column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.contact_mail_button = ttk.Button(self.entry_contact_mail , image = self.mail_icon) 
        self.mail_button.config(cursor = 'arrow')
        self.contact_mail_button.pack(side = "right")
        
        self.label_contact_phone = ttk.Label(self.contact_frame , text = "Teléfono")
        self.label_contact_phone.grid(row = 5 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        
        self.entry_contact_phone = ttk.Entry(self.contact_frame)
        self.entry_contact_phone.insert(0, "963278165")
        self.entry_contact_phone.grid(row = 6 , column = 0 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.contact_phone_button = ttk.Button(self.entry_contact_phone , image = self.phone_icon)
        self.contact_phone_button.config(cursor = 'arrow')
        self.contact_phone_button.pack(side = "right")
        
        self.label_mobile = ttk.Label(self.contact_frame , text = "Móvil")
        self.label_mobile.grid(row = 5 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_mobile = ttk.Entry(self.contact_frame)
        self.entry_mobile.insert(0 , "686289365")
        self.entry_mobile.grid(row = 6 , column = 1 , pady = 2 , padx = 2 , sticky = W+E)
        
        self.mobile_button = ttk.Button(self.entry_mobile , image = self.mobile_icon , width = 2 , command = self.capturar )
        self.mobile_button.config(cursor = 'arrow')
        self.mobile_button.pack(side = "right")
                                                                       # Centrar texto------------------------
        self.free_space = ttk.Label(self.contact_frame , text="algo" , anchor = 'center' , justify =  'center')
        self.free_space.grid(row = 7 , column = 0 , columnspan = 2 ,sticky = 'nswe')
        self.contact_frame.grid_rowconfigure(7,weight=1)
        
        self.notas = Text(self.contact_frame)
        self.notas.config(padx = 2 , pady = 2 ,width = 30 , height = 3)
        self.notas.grid(row = 8, column = 0, columnspan = 2 , sticky = W+E ,ipady = 10, ipadx=15)
        
        self.margin_bottom_contacto = Label(self.contact_frame , text = "id: 45612" , bg = 'black' , fg = 'white')
        #self.margin_bottom_contacto.config(height= 0)
        self.margin_bottom_contacto.grid(row = 9 , column = 0 , columnspan = 2 , sticky = W+E)
        
        self.load_contacts(employee)    
    
    def center_window(self, window):
        
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        
    def on_heading_click(self , e):
        
        print(f"funciona {e}")
        
        
    def update_selected(self,option):
        
        self.selected_option.set(option)
        print("ha entrado")
        
        
    def capturar(self):
        
        print(self.entry_mobile.get())
        
        
    def create_contact(self):
        
        frame = tk.Toplevel()
        frame.title("Nuevo Contacto")
        frame.geometry("400x200")
        #frame.minsize(400, 400)    # Establecer un tamaño mínimo de 300x200
        frame.grid_columnconfigure(0 , weight = 1)
        self.center_window(frame)
        
        
        frame_info = ttk.Frame(frame)
        frame_info.grid(row = 0 , column = 0, padx = 5 , pady = 10 , sticky = W+E)
        frame_info.grid_columnconfigure(0 , weight = 1)
        frame_info.grid_columnconfigure(1 , weight = 1)
        
        label_name = ttk.Label(frame_info, text = "Nombre:")
        label_name.grid(row = 0 , column = 0 , padx = 5 , sticky = W+E)
        
        entry_name = ttk.Entry(frame_info)
        entry_name.grid(row = 1 , column = 0 , padx = 5 , sticky = W+E)
        
        label_surname = ttk.Label(frame_info , text = "Apellidos")
        label_surname.grid(row = 0 , column = 1 , padx = 5 , sticky = W+E)
        
        entry_surname = ttk.Entry(frame_info)
        entry_surname.grid(row = 1 , column = 1 , padx = 5 , sticky = W+E)
        
        label_job_title = ttk.Label(frame_info , text = "Cargo")
        label_job_title.grid(row = 2 , column = 0 , sticky = W+E , padx = 5)
        
        entry_job_title = ttk.Entry(frame_info)
        entry_job_title.grid(row = 3 , column = 0, sticky = W+E , padx = 5)
        
        label_mail = ttk.Label(frame_info , text = "Mail")
        label_mail.grid(row = 2 , column = 1 , sticky = W+E , padx = 5)
        
        entry_mail = ttk.Entry(frame_info)
        entry_mail.grid(row = 3 , column = 1, sticky = W+E , padx = 5)
        
        label_phone = ttk.Label(frame_info , text = "Teléfono")
        label_phone.grid(row = 4 , column = 0 , sticky = W+E , padx = 5)
        
        entry_phone = ttk.Entry(frame_info)
        entry_phone.grid(row = 5 , column = 0, sticky = W+E , padx = 5)
        
        label_mobile = ttk.Label(frame_info , text = "Móvil")
        label_mobile.grid(row = 4 , column = 1 , sticky = W+E , padx = 5)
        
        entry_mobile = ttk.Entry(frame_info)
        entry_mobile.grid(row = 5 , column = 1, sticky = W+E , padx = 5)
        
        save_button = ttk.Button(frame_info, text = "Guardar")
        save_button.grid(row = 6 , column = 0 , columnspan = 2 , padx = 20 , pady = 20 , sticky = W+E)
    
    
    def calendar_selected_date(self , event):
        
        try:
            fecha_seleccionada = self.calendar.get_date() # 10-04-2024
            month = int(fecha_seleccionada[3:5])
            year = int(fecha_seleccionada[6:])
            
            if int(fecha_seleccionada[0]) == 0:
                day = int(fecha_seleccionada[1])
            
            else:
                day = int(fecha_seleccionada[0:2])
                
            self.fecha.set(datetime(year,month,day).strftime("%d %B")) 
            self.toggle_frame_visibility()
            
        except Exception as e:
            mb.showwarning("Error" , "Ha habido un problema con las fechas")
               
    
        
    def test(self, event):
        
        item = self.combo_state.get()
        print(item)
        
        
    def abrir_enlace(self):
        
         webbrowser.open_new('https://chat.openai.com/c/2220aa72-de48-497a-b191-203933de98d3')
         
         
    def add_company(self):
        
            add_company_frame = Toplevel()
            add_company_frame.title("Add Company")
            add_company_frame.geometry("600x300")
            
            add_company_frame.grid_columnconfigure(0 , weight = 1)
            
            company_frame = ttk.Labelframe(add_company_frame , text = 'Empresa')
            company_frame.grid(row = 0 , column = 0 , columnspan = 4 , padx = 10 , pady = 10 , sticky = W+E)
            
            company_frame.grid_columnconfigure(0 , weight = 1)   
            company_frame.grid_columnconfigure(1 , weight = 1)
            
            company_name = ttk.Label(company_frame , text ="Nombre: ")
            company_name.grid(row =0 , column = 0 , padx = 5 , pady = 5 )
            
            entry_comapany_name = ttk.Entry(company_frame)
            entry_comapany_name.grid(row =0 , column = 1 , columnspan = 5 , padx = 5 , pady = 5 , sticky = W+E)
            
            company_nif= ttk.Label(company_frame , text ="N.I.F: ")
            company_nif.grid(row =0 , column = 6 , padx = 5 , pady = 5)
            
            entry_comapany_nif = ttk.Entry(company_frame)
            entry_comapany_nif.grid(row =0 , column = 7 , padx = 5 , pady = 5)
            
            company_activity = ttk.Label(company_frame , text ="Actividad: ")
            company_activity.grid(row =4 , column = 0 , padx = 5 , pady = 5)
            
            self.nace_list_menu = ttk.Combobox(company_frame, state = 'readonly' , values = nace_list())
            self.nace_list_menu.grid(row =4 , column = 1 ,  columnspan= 7 , padx = 5 , pady = 5 , sticky = W+E)
            self.nace_list_menu.current(newindex = 0)
            self.nace_list_menu.bind("<<ComboboxSelected>>" , self.mas_tests) # Cambiar la función ######################################
            
            
            company_adress = ttk.Labelframe(add_company_frame , text ="Dirección: ")
            company_adress.grid(row =1 , column = 0 , columnspan = 4 , padx = 10 , pady = 10 , sticky = W+E)
            
            company_street_label = ttk.Label(company_adress, text="Calle: ")
            company_street_label.grid(row=0, column=0, padx=5, pady=5, columnspan=3, sticky="we")

            company_street = ttk.Entry(company_adress)
            company_street.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="we")

            company_street_label_number = ttk.Label(company_adress, text="Núm: ")
            company_street_label_number.grid(row=0, column=4, pady=5, sticky="we")

            company_street_number = ttk.Entry(company_adress , width = 6)
            company_street_number.grid(row=1, column=4,  pady=5)
            
            company_street_label_floor = ttk.Label(company_adress, text="Piso: ")
            company_street_label_floor.grid(row=0, column=5, padx=5, pady=5, sticky="we")
            
            company_street_floor = ttk.Entry(company_adress , width = 6)
            company_street_floor.grid(row=1, column=5, padx=5, pady=5)
            
            company_adress.grid_columnconfigure(0 , weight = 1)
            company_adress.grid_columnconfigure(1 , weight = 1)
            
            company_contact = ttk.Labelframe(add_company_frame , text = "Contacto")   
            company_contact.grid(row = 2 , column = 0 , columnspan = 4 , padx = 10 , pady = 10 , sticky = W+E)
            company_contact.grid_columnconfigure(0 , weight = 1)   
            company_contact.grid_columnconfigure(1 , weight = 1)       
            
            company_web = ttk.Label(company_contact , text ="Web: ")
            company_web.grid(row =2 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            entry_comapany_web = ttk.Entry(company_contact)
            entry_comapany_web.grid(row = 2 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
            
            company_mail = ttk.Label(company_contact , text ="Mail: ")
            company_mail.grid(row =2 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
            
            entry_comapany_mail = ttk.Entry(company_contact)
            entry_comapany_mail.grid(row =2 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
            
            company_phone = ttk.Label(company_contact , text ="Teléfono: ")
            company_phone.grid(row =3 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            entry_comapany_phone = ttk.Entry(company_contact)
            entry_comapany_phone.grid(row =3 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
            
            company_phone2 = ttk.Label(company_contact , text ="Teléfono2: ")
            company_phone2.grid(row =3 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
            
            entry_comapany_phone2 = ttk.Entry(company_contact)
            entry_comapany_phone2.grid(row =3 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
            
            company_activity = ttk.Label(company_frame , text ="Actividad: ")
            company_activity.grid(row =4 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)

            self.center_window(add_company_frame)
            
            
    def state(self, event):  # Recibir valor del Combobox
        
            item = self.combo_state.get()
            print(item)

        # CALENDARIO

    def toggle_frame_visibility(self):
        
        self.frame_container_calendar.config(bg='')
        
        if self.frame_container_calendar.winfo_ismapped(): # Comprueba si self.frame_container_calendar es visible, si es visible lo oculta con self.frame_container_calendar.grid_forget()
            self.frame_container_calendar.grid_forget()
            
        else:
            self.frame_container_calendar.grid(row=1, column=0) # Si lo pongo en 0 desplaza el contenido que hay en el mismo nivel
            self.frame_container_calendar.lift()  # Elevar el Frame al frente
    
    
    def sql3(self):
        pass
    

    def mas_tests(self , event):
        
        test = Date()
        print(test.test(10))
        
        
    def load_contacts(self , employee):
        #self.info.insert("" , 0 , text = 'client[0]' , values =['client[1]' , 'client[2]' , 'client[3]' , 'client[4]' , 'client[5]' , "Cantidad" , "Porcentaje"])
        contacts = db.session.query(Client).filter(and_(Client.state == "Lead" , Client.employee_id == employee )).all()
        
        for client in contacts:
            self.info.insert(text = client[0] , values =[client[1] , client[2] , client[3] , client[4] , client[5] , "Cantidad" , "Porcentaje"])
            

  
employee = "AMC"


        
lista_datos = [
    ["Empresa 1", "01-01-2023", 50, "15-03-2024", 300, 10],
    ["Empresa 2", "20-07-2023", 75, "05-05-2024", 500, 25],
    ["Empresa 3", "10-02-2023", 20, "30-04-2024", 200, 5],
    ["Empresa 4", "12-09-2023", 90, "10-06-2024", 400, 15],
    ["Empresa 5", "05-05-2023", 40, "20-02-2024", 100, 30],
    ["Empresa 6", "15-11-2023", 60, "25-08-2024", 600, 20],
    ["Empresa 7", "25-03-2023", 10, "12-12-2023", 50, 35],
    ["Empresa 8", "08-06-2023", 85, "02-07-2024", 450, 40],
    ["Empresa 9", "30-04-2023", 30, "01-01-2024", 150, 45],
    ["Empresa 10", "18-12-2023", 70, "08-09-2024", 700, 50],
    ["Empresa 11", "21-08-2023", 55, "14-11-2024", 550, 12],
    ["Empresa 12", "02-03-2023", 25, "19-12-2023", 250, 27],
    ["Empresa 13", "29-10-2023", 80, "07-10-2024", 800, 8],
    ["Empresa 14", "17-06-2023", 45, "23-03-2024", 450, 33],
    ["Empresa 15", "07-01-2023", 15, "28-05-2024", 150, 18],
    ["Empresa 16", "13-05-2023", 65, "09-01-2024", 650, 22],
    ["Empresa 17", "26-09-2023", 95, "03-08-2024", 950, 38],
    ["Empresa 18", "11-04-2023", 35, "16-06-2024", 350, 42],
    ["Empresa 19", "24-12-2023", 75, "20-09-2024", 750, 47],
    ["Empresa 20", "19-07-2023", 50, "31-07-2024", 500, 9],
    ["Empresa 21", "03-02-2023", 10, "26-11-2023", 100, 15],
    ["Empresa 22", "08-11-2023", 60, "04-04-2024", 600, 31],
    ["Empresa 23", "14-05-2023", 40, "29-12-2024", 400, 17],
    ["Empresa 24", "23-10-2023", 85, "06-03-2024", 850, 23],
    ["Empresa 25", "06-06-2023", 30, "22-10-2024", 300, 28],
    ["Empresa 26", "16-01-2023", 20, "18-09-2024", 200, 36],
    ["Empresa 27", "22-08-2023", 70, "13-02-2024", 700, 41],
    ["Empresa 28", "04-03-2023", 45, "11-07-2024", 450, 46],
    ["Empresa 29", "01-11-2023", 55, "05-05-2024", 550, 48],
    ["Empresa 30", "18-06-2023", 65, "27-01-2024", 650, 3],
    ["Empresa 31", "20-01-2023", 5, "21-08-2024", 50, 11],
    ["Empresa 32", "13-07-2023", 80, "03-06-2024", 800, 19],
    ["Empresa 33", "11-02-2023", 15, "09-04-2024", 150, 26],
    ["Empresa 34", "05-09-2023", 35, "28-12-2023", 350, 34],
    ["Empresa 35", "24-04-2023", 90, "26-10-2024", 900, 39],
    ["Empresa 36", "30-11-2023", 25, "17-09-2024", 250, 44],
    ["Empresa 37", "22-06-2023", 75, "01-03-2024", 750, 49],
    ["Empresa 38", "02-01-2023", 50, "04-11-2024", 500, 7],
    ["Empresa 39", "09-08-2023", 60, "23-02-2024", 600, 14],
    ["Empresa 40", "28-03-2023", 45, "30-08-2024", 450, 21],
    ["Empresa 41", "15-10-2023", 30, "10-10-2024", 300, 29],
    ["Empresa 42", "27-05-2023", 70, "15-01-2024", 700, 37],
    ["Empresa 43", "12-12-2023", 20, "06-07-2024", 200, 43],
    ["Empresa 44", "10-07-2023", 40, "24-05-2024", 400, 1],
    ["Empresa 45", "06-02-2023", 85, "12-09-2024", 850, 13],
    ["Empresa 46", "23-09-2023", 10, "11-11-2023", 100, 16],
    ["Empresa 47", "14-04-2023", 55, "07-01-2024", 550, 24],
    ["Empresa 48", "18-11-2023", 65, "20-06-2024", 650, 32]]
 
     

if __name__ == "__main__":
    
    
    db.Base.metadata.create_all(db.engine)
    #€usuario = Contact(name_contact = "campo uno" , last =  "campo dos")
    #db.session.add(usuario)
    #db.session.commit()
    #db.session.close()
    root = Tk()
    app = Main(root)
    act.login(app)
    root.mainloop()
    
