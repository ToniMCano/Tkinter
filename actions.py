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
from datetime import datetime
import locale
from tkinter import messagebox as mb
import os
locale.setlocale(locale.LC_ALL, '')
   



def nace_list():
    
    if os.name == "nt":
        excel = openpyxl.load_workbook("recursos\\NACE.xlsx")
    
    else:
        excel = openpyxl.load_workbook("recursos/NACE.xlsx")

    nace = excel['Hoja 1']['A']

    lista_nace = []

    for x in nace:
        valor = x.value.split(" - ")
        
        if len(valor[0]) > 1:
            lista_nace.append( valor[0] + " " + valor[1])
        
    return lista_nace

 
class Actions:
    
    def center_window(self, window):
        
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    
    def login():
            
        login = Toplevel()
        login.title("Login")
        #login.geometry("300x200")
        
        login.grid_columnconfigure(0 , weight = 1)
        #login.grid_rowconfigure(0 , weight = 1)
        
        frame = ttk.Labelframe(login , text = "Login")
        frame.grid(row = 0 , column = 0 , padx = 10 , pady = 5 , sticky = "we")
        frame.grid_columnconfigure(1, weight = 1)        
        
        employee_alias = ttk.Label(frame, text = "Employee: ")
        employee_alias.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = "w")
        
        employee_alias_entry = ttk.Entry(frame)
        employee_alias_entry.grid(row = 0 , column = 1 , padx = 5 , pady = 10 , sticky = W+E)
        
        employee_password = ttk.Label(frame, text = "Password: ")
        employee_password.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = "w")
        
        employee_password_entry = ttk.Entry(frame)
        employee_password_entry.grid(row =1 , column = 1 , padx = 5 , pady = 10 , sticky = W+E)
        
        log_button = ttk.Button(login , text = "Login")
        log_button.grid(row = 1 , column = 0 , padx = 10 , pady = 10)
        
        Actions.center_window(Actions , login)
        
     
     
    def load_contacts(self , employee):
        #self.info.insert("" , 0 , text = 'client[0]' , values =['client[1]' , 'client[2]' , 'client[3]' , 'client[4]' , 'client[5]' , "Cantidad" , "Porcentaje"])
        #contacts = db.session.query(Client).filter(and_(Client.state == "Lead" , Client.employee_id == employee )).all()
        
        #for client in contacts:
        self.info.insert("" , 0 , text = 'client[0]' , values =['client[1]' , 'client[2]' , 'client[3]' , 'client[4]' , 'client[5]' , "Cantidad" , "Porcentaje"])
               
               
    
        
    
    def create_contact(self):
        
        frame = tk.Toplevel()
        frame.title("Nuevo Contacto")
        frame.geometry("400x200")
        #frame.minsize(400, 400)    # Establecer un tamaño mínimo de 300x200
        frame.grid_columnconfigure(0 , weight = 1)
        Actions.center_window(Actions , frame)
        
        
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
        
        
    def add_company(self):
    
        add_company_frame = Toplevel()
        add_company_frame.title("Add Company")
        #add_company_frame.geometry("600x300")
        
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
        self.nace_list_menu.bind("<<ComboboxSelected>>" , self.test) # Cambiar la función ######################################
        
        
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

        Actions.center_window(Actions , add_company_frame)
            
    
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
            Actions.toggle_frame_visibility(self.frame_container_calendar)
            
        except Exception as e:
            mb.showwarning("Error" , f"Ha habido un problema con las fechas {e}")
            
            
    def toggle_frame_visibility(frame):
        
        frame.config(bg='')
        
        if frame.winfo_ismapped(): # Comprueba si self.frame_container_calendar es visible, si es visible lo oculta con self.frame_container_calendar.grid_forget()
            frame.grid_forget()
            
        else:
            frame.grid(row=1, column=0) # Si lo pongo en 0 desplaza el contenido que hay en el mismo nivel
            frame.lift()  # Elevar el Frame al frente    
                
    def olvidar(app):
       app.grid_forget()
       
    def tst(self):
        pass
