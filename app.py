
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
from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs , States , ContactActions , Actions , NewCompany
from sales_tab import SalesTab
from sales_actions import OrderFunctions
from statistics_tab import StatisticsTab
from datetime import datetime , timedelta
#import locale
from tkinter import messagebox as mb
from ttkthemes import ThemedTk
import customtkinter as ctk
from customtkinter import * 



#locale.setlocale(locale.LC_ALL, '')  # Si lo implemento cambian las medidas y da error.


class Main:
    
    def __init__(self, root):
        self.main_window = root
        self.main_window.title("MyCRM")
        self.main_window.resizable(1,1)
        self.main_window.geometry('1200x800')
        self.main_window.configure(bg="#f4f4f4") 
        self.main_window.grid_columnconfigure(0 , weight = 1)
        self.main_window.grid_rowconfigure(2 , weight = 1)
        Pops.center_window(self, self.main_window)
        
        self.timer = None

        # INFO LISTA
        
        style = ttk.Style()
        style.configure("Treeview.Heading", background='LightBlue4')  
        style.layout("mystyle.Treeview" , [("mystyle.Treeview.treearea", {'sticky' : 'nswe'})]) # Eliminar los bordes??
        
        self.crm_frame = CTkFrame(self.main_window , fg_color='transparent')
        self.crm_frame.grid(row = 2 , column = 0 , rowspan = 2 , sticky = 'nswe')
        self.crm_frame.grid_columnconfigure(0, weight=3) # Configuramos el redimensionamiento del frame principal
        self.crm_frame.grid_columnconfigure(1, weight=1)
        self.crm_frame.grid_rowconfigure(1, weight=1)

        #self.crm_frame.grid_rowconfigure(1, weight=1)
        
        self.frame_tree = CTkFrame(self.crm_frame, fg_color='transparent')
        self.frame_tree.grid(row = 1 , column = 0 , sticky = "nswe" ,  rowspan = 3)
        self.frame_tree.grid_columnconfigure(0, weight=1)
        self.frame_tree.grid_rowconfigure(3, weight=1)

        self.info = ttk.Treeview(self.frame_tree, height = 20 , style="mystyle.Treeview")
        self.info.grid(row = 0 , column = 0 , sticky = 'nsew')     
        
        self.info["columns"] = ( "#0" , "#1" , "#2" , "#3" ,  "#4")
        self.info.heading("#0" , text = "Estado" , command = lambda: LoadInfo.on_heading_click(self , "state"))
        self.info.heading("#1" , text = "Días" , command = lambda: LoadInfo.on_heading_click(self , "days"))
        self.info.heading("#2" , text  ="Cliente" , command = lambda: LoadInfo.on_heading_click(self , "client"))
        self.info.heading("#3" , text = "Último Contacto" , command = lambda: LoadInfo.on_heading_click(self , "last"))
        self.info.heading("#4" , text = "Próximo Contacto" , command = lambda: LoadInfo.on_heading_click(self , "next"))
        self.info.heading("#5" , text = "C. Postal" , command = lambda: LoadInfo.on_heading_click(self , "postal_code"))
        
        self.info.column("#0" , width = 25 , anchor="center")
        self.info.column("#1" , width = 10 , anchor="center")
        self.info.column("#2" , width = 150)
        self.info.column("#3" , width = 70 , anchor="center")
        self.info.column("#4" , width = 70 , anchor="w")
        self.info.column("#5" , width = 10 , anchor="w")

        self.info.bind("<ButtonRelease-1>" , lambda event: LoadInfo.get_item(self , "crm" , self.info , event))
        
        self.active_employee_id = StringVar()
        
        self.fecha = StringVar()
        
        self.company_id = StringVar()
        
        self.button_a_value = StringVar()
        
        self.button_a_value.set("Terminate")
 
        self.modify_order_id = [False , None]
        
        self.advises = StringVar()
        
        
        Pops.login(self)
        
        
        #IMAGENES 
        
        self.mobile_image= Image.open("recursos/mobile.png")
        self.mobile_resize = self.mobile_image.resize((10,16))
        self.mobile_icon = ImageTk.PhotoImage(self.mobile_resize)
                
        self.triangle_icon = Image.open("recursos/triangulo.png")
        self.triangle_icon = CTkImage(self.triangle_icon , size = (10,10))
                
        self.icon_calendar= Image.open("recursos/calendar.png")
        self.calendar_icon = self.icon_calendar.resize((16,16))
        self.icon_calendar = ImageTk.PhotoImage(self.calendar_icon)
        
        self.web_icon = Image.open("recursos/web2.png")
        self.web_icon = self.web_icon.resize((13,16))
        self.web_icon = ImageTk.PhotoImage(self.web_icon)
        
        self.mail_image = Image.open("recursos/mail.png")
        self.mail_icon = self.mail_image.resize((18,16))
        self.mail_icon = ImageTk.PhotoImage(self.mail_icon)
        
        self.phone_image = Image.open("recursos/phone.png")
        self.phone_icon = self.phone_image.resize((12,16))
        self.phone_icon = ImageTk.PhotoImage(self.phone_icon)

        
        # HEADER
        
        self.header = ttk.Frame(self.main_window)
        self.header.grid(row = 0 , column = 0 , pady = 5 , padx = 5 , sticky = W+E)
        self.header.columnconfigure(10, weight = 1)
        self.header.columnconfigure(6, weight = 1)
        
                # AÑADIR CONTACTOS DESDE POOL
        
        self.new_company = ttk.Button(self.header , text = 'Add Company' , command = lambda: NewCompany.new_company(self)) 
         
     
        # LEAD, CANDIDATE , CONTACT
        
        self.employee = ttk.Combobox(self.header ,state = "readonly", values =  LoadInfo.employees_list() , width= 10)
        self.employee.configure(background='lightblue')
        self.employee.grid(row = 0 , column = 3 , padx = 5)
        self.employee.bind("<<ComboboxSelected>>" , lambda e: Pops.change_employee(self ,  e))

        self.combo_state = ttk.Combobox(self.header ,state = "readonly",values = ["Lead", "Candidate", "Contact" , "Pool" , 'All'], width= 10)
        self.combo_state.configure(background='lightblue')
        self.combo_state.grid(row = 0 , column = 4 , padx = 5)
        self.combo_state.bind("<<ComboboxSelected>>" , lambda e: LoadInfo.companies_state(self , self.active_employee_id.get() , e))

        # CALENDAR
        
        # Crear un Frame que se mostrará/ocultará self.frame_button
        self.frame_calendar = tk.Frame(self.crm_frame , highlightbackground = 'LightBlue4' , highlightthickness = 1)
        MyCalendar.calendar(self , "general")
        self.frame_calendar_next = tk.Frame(self.crm_frame , highlightbackground = 'LightBlue4' , highlightthickness = 1)
        MyCalendar.calendar(self  , "next")
        self.frame_calendar_pop = tk.Frame(self.crm_frame , highlightbackground = 'LightBlue4' , highlightthickness = 1)
        MyCalendar.calendar(self  , "pop")

        # HEADER

        self.frame_calendar_button = CTkFrame(self.header , fg_color = 'white' , border_width = 0)
        #self.frame_calendar_button.config(height=1)
        self.frame_calendar_button.grid(row = 0 , column = 5 , padx = 5)

        self.fecha.set(datetime.now().strftime("%d %B").title())
        
        self.label_calendar_button = CTkLabel(self.frame_calendar_button , textvariable = self.fecha ,fg_color=("white", "white"), text_color = "gray" , bg_color = "White",  width = 100 )
        #self.label_calendar_button.config(width = 15 , height = 1)
        self.label_calendar_button.grid(row = 0, column = 6)
        
        self.boton_fecha = ttk.Button(self.frame_calendar_button, image = self.icon_calendar, command = lambda: MyCalendar.calendar_toggle_frame(self , "general"))
        self.boton_fecha.config(cursor = 'arrow')
        self.boton_fecha.grid(row=0, column=1, sticky="ew")
        
        self.frame_views = ttk.Frame(self.header , height = 30 , width = 300)
        self.frame_views.place(relx=0.4 , y = 2) 
        
        self.crm_view_button = CTkButton(self.frame_views , text = "CRM" , corner_radius = 2 , fg_color = "Lightblue4" , width = 80 , height = 10  , command = lambda: Tabs.select_tab(self , 'crm'))
        self.crm_view_button.place(relx=0.2, rely=0.5  , anchor = 'center')
        
        self.sales_view_button = CTkButton(self.frame_views , text = "Venta" , corner_radius = 2 , fg_color = "Lightblue4" , width = 80 , height = 10 , command = lambda: SalesTab.sales_root(self))
        self.sales_view_button.place(relx=0.5, rely=0.5 , anchor = 'center')
        
        self.statistics_view_button = CTkButton(self.frame_views , text = "Estadísticas" , corner_radius = 2 , fg_color = "Lightblue4" , width = 80 , height = 10 , command = lambda: StatisticsTab.statistics_root(self))
        self.statistics_view_button.place(relx=0.8, rely=0.5 , anchor = 'center')
        
        self.login_button = ttk.Button(self.header , text = "Login" , command = lambda: Pops.login(self))
        self.login_button.grid(row = 0 , column = 10 , sticky = E)
        
        self.pop_up = ttk.Button(self.header, text = "PopUp" , command = lambda: Alerts.pop_up_alert(self, self.active_employee_id.get() , str(datetime.now())))
        self.pop_up.config(cursor = 'arrow')
        self.pop_up.grid(row = 0 , column = 11 , padx = 5 , sticky = E)
        
        self.pop_up_advise  = CTkLabel(self.pop_up , textvariable = self.advises , text_color = 'white' , fg_color = 'red' , corner_radius = 50 , height = 15 , width = 15 , font = ("" , 10 , 'bold'))
        
        
        # LOG

        self.frame_log = ttk.Frame(self.frame_tree )
        self.frame_log.grid(row = 2, column = 0  , columnspan = 2 , sticky = W+E)
        self.frame_log.grid_columnconfigure(1, weight=1)
        
        self.text_log =Text(self.frame_log)
        self.text_log.config(height = 3 , width = 80)
        self.text_log.grid(row = 1 , column = 1, rowspan = 2 , columnspan = 2 , sticky = 'nswe', padx = 5 , pady = 2)
        
        self.next_contact = ttk.Button(self.frame_log , text = "Next Contact" , command = lambda: MyCalendar.calendar_toggle_frame(self , "next"))
        self.next_contact.config(cursor = 'arrow')
        self.next_contact.grid(row = 1, column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_pop_up = ttk.Button(self.frame_log , text = "Pop Up", command = lambda: MyCalendar.calendar_toggle_frame(self , "pop"))
        self.boton_pop_up.config(cursor = 'arrow')
        self.boton_pop_up.grid(row = 2 , column = 0 , sticky = 'nswe' , padx = 2 , pady = 2)
        
        self.boton_log = ttk.Button(self.frame_log , text = "Log" , command = lambda: Logs.add_log(self , str(datetime.now())[:16] , "log" , 'hour'))
        self.boton_log.config(cursor = 'arrow')
        self.boton_log.grid(row = 1 , column = 7, padx = 2 , pady= 2 , sticky = "nswe" , rowspan = 2)

        # NÚMERO DE CONTACTOS/ESTADO
        
        self.contacts = StringVar()
        
        self.contacts_number = ttk.Frame(self.frame_tree)
        self.contacts_number.grid(row = 1 , column = 0 , columnspan = 2 , sticky = "nswe")
        
        self.contacts_var = CTkLabel(self.contacts_number , textvariable = self.contacts , anchor = 'center' , text_color = 'gray' , font = ("" , 12 , 'bold'))
        self.contacts_var.pack(fill = "both" , expand = True, side = "top" , pady = 3)
        
        self.side_frame = CTkFrame(self.crm_frame , fg_color = 'transparent')
        self.side_frame.grid(row = 1 , column = 1 , sticky = "nswe" , columnspan = 4 , rowspan = 2) 
        self.side_frame.grid_columnconfigure(0 , weight = 1)
        self.side_frame.grid_rowconfigure(3, weight=1)
        
        # FRAME EMPRESA
        
        self.frame_company = CTkFrame(self.side_frame, fg_color = "transparent" , border_width = 1 , border_color = "lightgray") 
        self.frame_company.grid(row = 0 , column = 0 , sticky = "nswe" ,  padx = 5)        
        self.frame_company.grid_columnconfigure(0 , weight = 1)
        
        self.header_company = CTkLabel(self.frame_company , text="Empresa", bg_color='LightBlue4' , text_color = "white")
        self.header_company.grid(row = 0 , column = 0 , columnspan = 3  , sticky=W+E)
        
        self.margin_frame_company = CTkFrame(self.frame_company , fg_color = "transparent") 
        self.margin_frame_company.grid(row = 1 , column = 0 , sticky = "nswe" , columnspan = 4, rowspan = 2 ,padx = 5 , pady = 5) 
        self.margin_frame_company.grid_columnconfigure(0 , weight = 1)
        self.margin_frame_company.grid_columnconfigure(1 , weight = 1)
        
        self.label_company_name = ttk.Label(self.margin_frame_company, text = "Empresa" , font = ("" , 9 , 'bold'), foreground='LightBlue4')
        self.label_company_name.grid(row = 1 , column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_company_name = ttk.Entry(self.margin_frame_company)
        self.entry_company_name.grid(row = 2, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        self.entry_company_name.bind("<Return>" , lambda e: Update.update_name(self , 'company_name', e))

        
        self.label_nif = ttk.Label(self.margin_frame_company  , text = "N.I.F.", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_nif.grid(row = 1 , column = 1 , sticky = W+E , padx = 2  , pady = 2)
        
        self.entry_nif = ttk.Entry(self.margin_frame_company )
        self.entry_nif.grid(row = 2 , column = 1 , padx = 2  , pady = 2 , sticky = W+E)
        self.entry_nif.bind("<Return>" , lambda e: Update.update_nif(self , e))

        
        self.label_adress = ttk.Label(self.margin_frame_company  , text = "Dirección" ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_adress.grid(row = 3 , column = 0 , columnspan = 2 , sticky = "we" , padx = 2 , pady = 2) 

        self.entry_adress = ttk.Entry(self.margin_frame_company )
        self.entry_adress.grid(row = 4 , column =0 , columnspan = 2 , sticky = "we" , padx = 2 , pady = 2)
        self.entry_adress.bind("<Button-1>" , lambda e: Update.update_adress(self , e))

        self.label_activity = ttk.Label(self.margin_frame_company  , text = "Actividad", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_activity.grid(row = 5 , column = 0, sticky=W+E , padx = 2 , pady = 2)
        
        self.entry_activity = ttk.Combobox(self.margin_frame_company , values = LoadInfo.nace_list())
        self.entry_activity.grid(row = 6 , column = 0 , sticky = W+E , padx = 2  , pady = 2)
        self.entry_activity.bind("<Return>" , lambda e: Update.update_activity(self , e)) 
        
        self.label_employees = ttk.Label(self.margin_frame_company , text = "Empleados", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_employees.grid(row = 5 , column = 1, sticky=W+E , padx = 2 , pady = 2)
        
        self.entry_employees = ttk.Combobox(self.margin_frame_company , values = [" < 10" , "10 - 50" , "50 - 250" , " > 250"], font = ("" , 9 , 'bold'))
        self.entry_employees.grid(row = 6 , column = 1 , sticky = W+E , padx = 2  , pady = 2)
        self.entry_employees.bind("<Return>" , lambda e: Update.update_employees(self , e)) 
        
        self.label_web = ttk.Label(self.margin_frame_company , text = "Web", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_web.grid(row = 7 , column = 0,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_web = ttk.Entry(self.margin_frame_company)
        self.entry_web.grid(row = 8 , column= 0 , padx = 2  , pady = 2 , sticky = W+E)
        self.entry_web.bind("<Return>" , lambda e: Update.update_web(self , e))
        
        self.web_button = ttk.Button(self.entry_web ,  image = self.web_icon , command = lambda: Actions.abrir_enlace(self, self.company_id.get()))
        self.web_button.config(cursor = 'arrow')
        self.web_button.pack(side = "right")
        
        self.label_mail = ttk.Label(self.margin_frame_company , text = "Mail", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_mail.grid(row = 7, column = 1, sticky = W+E , padx = 2 , pady = 2)
        
        self.entry_company_mail = ttk.Entry(self.margin_frame_company)
        self.entry_company_mail.grid(row = 8 , column = 1,  columnspan=2, padx = 2 , pady = 2 , sticky = W+E)
        self.entry_company_mail.bind("<Return>" , lambda e: Update.update_mail(self , 'company_mail' , e))
        
        self.mail_button = ttk.Button(self.entry_company_mail, image = self.mail_icon , command = lambda: Actions.send_mail(self , self.company_id.get()))
        self.mail_button.config(cursor = 'arrow')
        self.mail_button.pack(side = "right")
        
        self.label_phone = ttk.Label(self.margin_frame_company , text = "Teléfono", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_phone.grid(row = 9, column = 0 , sticky = W+E , padx = 2 ,  pady = 2)
        
        self.entry_company_phone = ttk.Entry(self.margin_frame_company)
        self.entry_company_phone.grid(row = 10, column= 0  , padx = 2  , pady = 2 , sticky = W+E)
        self.entry_company_phone.bind("<Return>" , lambda e: Update.update_phone(self , 'phone' , e))

        
        self.phone_button = ttk.Button(self.entry_company_phone , image = self.phone_icon , command = lambda: Actions.call_phone(self , self.company_id.get() , 'company_phone'))
        self.phone_button.config(cursor = 'arrow')
        self.phone_button.pack(side = "right")
        
        self.label_phone2 = ttk.Label(self.margin_frame_company , text = "Otro Teléfono", font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_phone2.grid(row = 9, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        
        self.entry_company_phone2 = ttk.Entry(self.margin_frame_company)
        self.entry_company_phone2.grid(row = 10, column= 1  , padx = 2  , pady = 2 , sticky = W+E)
        self.entry_company_phone2.bind("<Return>" , lambda e: Update.update_phone(self , 'phone2' , e))

        
        self.phone2_button = ttk.Button(self.entry_company_phone2 , image = self.mobile_icon, command = lambda: Actions.call_phone(self , self.company_id.get() , 'company_phone2'))
        self.phone2_button.config(cursor = 'arrow')
        self.phone2_button.pack(side = "right")     
        
         #FRAME BUTTONS 
        
        self.company_contact_buttons = CTkFrame(self.margin_frame_company, fg_color = 'transparent')        
        self.company_contact_buttons.grid(row = 11 , column = 0 , columnspan = 2 , sticky = 'nswe' , pady = 5 )
        self.company_contact_buttons.grid_columnconfigure(0, weight = 1)
        self.company_contact_buttons.grid_columnconfigure(1, weight = 1) 
        #self.company_contact_buttons.grid_rowconfigure(0, weight = 1)    
        
        self.button_a = CTkButton(self.company_contact_buttons , textvariable = self.button_a_value , height = 2 , fg_color = "#f4f4f4" , corner_radius = 4 , text_color = 'gray' , border_color = "Lightgray" , border_width = 1 , hover_color = 'LightBlue4' , command = lambda: States.change_state(self))
        self.button_a.grid(row = 0 , column = 0 , sticky = "we" , pady = 5 , padx = 5)
        
        self.decline_button = CTkButton(self.company_contact_buttons , text = "Decline" , height = 2 , fg_color = "#f4f4f4" , corner_radius = 4 , text_color = 'gray' , border_color = "Lightgray" , border_width = 1 , hover_color = 'LightBlue4' , command = lambda: States.change_state(self , True))
        self.decline_button.grid(row = 0 , column = 1 , sticky = "we" , pady = 5 , padx = 5)

        self.historical_button = CTkButton(self.company_contact_buttons , text = "Historial" , height = 2 , fg_color = "#f4f4f4" , text_color = 'LightBlue4' , border_color = "LightBlue4" , border_width = 2 , hover_color = 'LightBlue4' , command = lambda: OrderFunctions.sales_historical(self))
        self.historical_button.grid(row = 0 , column = 2 , sticky = "we" , pady = 5 , padx = 5)
        
        #FRAME CONTACTO
        
        self.contact_frame = CTkFrame(self.side_frame , fg_color = "transparent" , border_width = 1 , border_color = "lightgray" ) 
        self.contact_frame.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky='swe')
        self.contact_frame.grid_columnconfigure(1, weight=1)
        self.contact_frame.grid_columnconfigure(0, weight=1)   
        
        self.contact_header = Label(self.contact_frame , text = "Contacto" ,bg = 'LightBlue4' , fg = 'white')
        self.contact_header.grid(row = 0 , column = 0 , columnspan = 2  ,sticky=W+E)
        
        self.new_contact_button = CTkButton(self.contact_header , text = "+"  ,  command = lambda: Pops.create_contact(self) , width = 30 , corner_radius = 3 , fg_color = "#f4f4f4" , text_color = "gray")
        self.new_contact_button.pack(side = "right") 
        
        self.other_contact = CTkButton(self.contact_header , image = self.triangle_icon  , text = "" , width = 10 , command = lambda: ContactActions.other_contact_widnow(self) , corner_radius = 3 , fg_color = "#f4f4f4")
        self.other_contact.pack(side = "left" , fill = "y")
        
        self.margin_frame_contact = tk.Frame(self.contact_frame) 
        self.margin_frame_contact.configure(bg = "#f4f4f4")
        self.margin_frame_contact.grid(row = 1, column = 0 , sticky = "nswe" , columnspan = 4, rowspan = 2 ,padx = 5 , pady = 5) 
        self.margin_frame_contact.grid_columnconfigure(1, weight=1)
        self.margin_frame_contact.grid_columnconfigure(0, weight=1)

        self.label_contact_name = ttk.Label(self.margin_frame_contact , text = "Nombre  " ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_contact_name.grid(row = 1 , column = 0 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_contact_name = ttk.Entry(self.margin_frame_contact)
        self.entry_contact_name.grid(row = 2 , column = 0 ,  padx = 2 , pady = 2 , sticky = W+E)
        self.entry_contact_name.bind("<Return>" , lambda e: Update.update_name(self , 'contact_name' , e))
        
        self.label_contact_surname = ttk.Label(self.margin_frame_contact , text = "Apellidos" ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_contact_surname.grid(row = 1 , column = 1 , sticky = W+E, padx = 2 , pady = 2) 
        
        self.entry_contact_surname = ttk.Entry(self.margin_frame_contact)
        self.entry_contact_surname.grid(row = 2 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        self.entry_contact_surname.bind("<Return>" , lambda e: Update.update_name(self , 'surname' , e))
        
        self.label_job_title = ttk.Label(self.margin_frame_contact, text = "Cargo" ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_job_title.grid(row = 3 , column = 0, padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_job_title = ttk.Entry(self.margin_frame_contact)
        self.entry_job_title.grid(row = 4 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        self.entry_job_title.bind("<Return>" , lambda e: Update.update_name(self , 'job' , e))

        
        self.label_contact_mail = ttk.Label(self.margin_frame_contact , text = "Mail" ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_contact_mail.grid(row = 3 , column = 1 , padx = 2 , pady = 2  , sticky = W+E)
        
        self.entry_contact_mail = ttk.Entry(self.margin_frame_contact)
        self.entry_contact_mail.grid(row = 4, column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        self.entry_contact_mail.bind("<Return>" , lambda e: Update.update_mail(self , 'contact_mail' , e))

        self.contact_mail_button = ttk.Button(self.entry_contact_mail , image = self.mail_icon , command = lambda: Actions.send_mail(self , self.entry_contact_mail.get())) 
        self.mail_button.config(cursor = 'arrow')
        self.contact_mail_button.pack(side = "right")
        
        self.label_contact_phone = ttk.Label(self.margin_frame_contact , text = "Teléfono" ,  font = ("" , 9 , 'bold') , foreground = 'LightBlue4')
        self.label_contact_phone.grid(row = 5 , column = 0 , padx = 2, pady = 2 , sticky = W+E)
        
        self.entry_contact_phone = ttk.Entry(self.margin_frame_contact)
        self.entry_contact_phone.grid(row = 6 , column = 0 , padx = 2 , pady = 2 , sticky = W+E)
        self.entry_contact_phone.bind("<Return>" , lambda e: Update.update_phone(self , 'contact_phone' , e))

        
        self.contact_phone_button = ttk.Button(self.entry_contact_phone , image = self.phone_icon , command = lambda: Actions.call_phone(self , self.company_id.get() , 'contact_phone'))
        self.contact_phone_button.config(cursor = 'arrow')
        self.contact_phone_button.pack(side = "right")
        
        self.label_mobile = ttk.Label(self.margin_frame_contact , text = "Móvil" , font = ("" , 9 , 'bold'), foreground='LightBlue4')
        self.label_mobile.grid(row = 5 , column = 1 , padx = 2 , pady = 2 , sticky = W+E)
        
        self.entry_mobile = ttk.Entry(self.margin_frame_contact)
        self.entry_mobile.grid(row = 6 , column = 1 , pady = 2 , padx = 2 , sticky = W+E)
        self.entry_mobile.bind("<Return>" , lambda e: Update.update_phone(self , 'mobile' , e))
        
        self.mobile_button = ttk.Button(self.entry_mobile , image = self.mobile_icon , width = 2 , command = lambda: Actions.call_phone(self , self.company_id.get() , 'mobile'))
        self.mobile_button.config(cursor = 'arrow')
        self.mobile_button.pack(side = "right")
        
        self.notes = Text(self.contact_frame)
        self.notes.config(height = 3)
        self.notes.grid(row = 7, column = 0  , columnspan = 2 , sticky = 'we' , padx = 5 , pady = 10)
        self.notes.bind("<Return>" , lambda e: Update.update_client_notes(self , e))
        
        
        self.ids_frame = ttk.Frame(self.side_frame)
        self.ids_frame.grid(row = 3 , column = 0 , columnspan = 2 , sticky = 'swe')
        self.ids_frame .grid_columnconfigure(0,weight=1)
        self.ids_frame .grid_columnconfigure(1,weight=1)
        self.ids_frame .grid_columnconfigure(2,weight=1)
        self.ids_frame .grid_columnconfigure(3,weight=1)
         
        
        self.lcontact_label_bottom = Label(self.ids_frame , text = 'ID Empresa: ', bg = 'LightBlue4' , fg = 'white' , anchor = 'e')
        self.lcontact_label_bottom.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.lcontact_label_company_id = Label(self.ids_frame , textvariable = self.company_id , bg = 'LightBlue4' , fg = 'white' , anchor = "w")
        self.lcontact_label_company_id.grid(row = 0 , column = 1 , sticky = W+E)

        self.rcontact_label_bottom = Label(self.ids_frame , text = 'ID Responsable: ', bg = 'LightBlue4' , fg = 'white' , anchor = 'e')
        self.rcontact_label_bottom.grid(row = 0 , column = 2 , sticky = W+E)
        
        self.rcontact_label_responsable_id = Label(self.ids_frame , textvariable = self.active_employee_id , bg = 'LightBlue4' , fg = 'white' , anchor = "w")
        self.rcontact_label_responsable_id.grid(row = 0 , column = 3 , sticky = W+E)

        Tabs.select_tab(self , 'crm')
        
        self.main_window.protocol("WM_DELETE_WINDOW", self.cancel_timer)

        
    def cancel_timer(self):
        try:
            if self.timer is not None and self.timer.is_alive():
                self.timer.cancel()
                
            self.main_window.destroy()
        
        except Exception as e:
            print(f"[cancel_timer]: {e}")
    
    
    def sales_from_mofify(self):
        
        try:                                    
            if self.sales_frame.winfo_ismapped():
                self.sales_frame.grid_forget()   # Si no se elimina se crean mas Frames y no se vuelve a mostar la vista de CRM al ejecutar esta función
            
            
            SalesTab.sales_root(self)
                
        except AttributeError:
            SalesTab.sales_root(self)

        except Exception as e:
            print(f"[view_alert] (select_tab): {e}")
        
        
  
if __name__ == "__main__":
    
    db.Base.metadata.create_all(db.engine)
    root = ThemedTk(theme="arc")
    app = Main(root)
    root.mainloop()
    
