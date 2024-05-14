import tkinter as tk
from tkinter import ttk , filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
import webbrowser
from models import Employee , Client , Contact , ContactPerson
import db
import openpyxl
from sqlalchemy import and_ , or_ , func ,asc , desc
from datetime import datetime , timedelta
#import locale
from tkinter import messagebox as mb
import os
from sqlalchemy.exc import IntegrityError , SQLAlchemyError 
from customtkinter import *
import pandas as pd
import time
import threading
#locale.setlocale(locale.LC_ALL, '')   Si uso Locale customtkinter da problemas.  ----- "TO-DO"
 

alerts = []
active_timer = [False]

class Pops:
    
    def center_window(self, window):
        
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        
    def login(root):
                
        login_window = Toplevel()
        login_window.title("Login")
        login_window.configure(bg="#f4f4f4") 
        
        login_window.grid_columnconfigure(0 , weight = 1)
        
        frame = ttk.Labelframe(login_window , text = "Login")
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
        
        log_button = ttk.Button(login_window , text = "Login" , command = lambda: LoadInfo.check_employee(root , employee_password_entry.get() , employee_alias_entry.get() , login_window))
        log_button.grid(row = 1 , column = 0 , padx = 5 , pady = 5)
        
        login_window.lift()
        Pops.center_window(Pops , login_window)
        
     
    def create_contact(self , company = ""): # #ecibir el id de la empresa.
        
        frame = tk.Toplevel()
        frame.title("New Contact")
        frame.geometry("600x180")   
        frame.configure(bg = "#f4f4f4")
        frame.grid_columnconfigure(0 , weight = 1)
        
        Pops.center_window(Pops , frame)
        
        frame_info = ttk.Frame(frame)
        frame_info.grid(row = 0 , column = 0, padx = 5 , pady = 10 , sticky = W+E)
        frame_info.grid_columnconfigure(0 , weight = 1)
        
        frame_contact_person = ttk.Labelframe(frame_info , text = "Contact Person" , labelanchor = 'n')
        frame_contact_person.grid(row = 0 , column = 0)
        
        label_name = ttk.Label(frame_contact_person, text = "Nombre:")
        label_name.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_name = ttk.Entry(frame_contact_person)
        entry_name.grid(row = 1 , column = 0 , padx = 5 , sticky = W+E)
        
        label_surname = ttk.Label(frame_contact_person , text = "Apellidos")
        label_surname.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_surname = ttk.Entry(frame_contact_person)
        entry_surname.grid(row = 1 , column = 1 , padx = 5 , sticky = W+E)
        
        label_job_title = ttk.Label(frame_contact_person , text = "Cargo")
        label_job_title.grid(row = 0 , column = 2 , sticky = W+E , padx = 5 , pady = 5 )
        
        entry_job_title = ttk.Entry(frame_contact_person)
        entry_job_title.grid(row = 1 , column = 2, sticky = W+E , padx = 5)
        
        label_mail = ttk.Label(frame_contact_person , text = "Mail")
        label_mail.grid(row = 2 , column = 0 , sticky = W+E , padx = 5)
        
        entry_mail = ttk.Entry(frame_contact_person)
        entry_mail.grid(row = 3 , column = 0, sticky = W+E , padx = 5 , pady = 5)
        
        label_phone = ttk.Label(frame_contact_person , text = "Teléfono")
        label_phone.grid(row = 2 , column = 1 , sticky = W+E , padx = 5)
        
        entry_phone = ttk.Entry(frame_contact_person)
        entry_phone.grid(row = 3 , column = 1, sticky = W+E , padx = 5 , pady = 5)
        
        label_mobile = ttk.Label(frame_contact_person , text = "Móvil")
        label_mobile.grid(row = 2 , column = 2 , sticky = W+E , padx = 5)
        
        entry_mobile = ttk.Entry(frame_contact_person)
        entry_mobile.grid(row = 3 , column = 2, sticky = W+E , padx = 5 , pady = 5)
        
        save_button = ttk.Button(frame_info, text = "Guardar")  # Cambiar función
        save_button.grid(row = 6 , column = 0 , columnspan = 2 , padx = 200 , pady = 5 , sticky = W+E)
        
        
    def new_company(self, data = {"Nombre Empresa: " : '' , "N.I.F.: " : '' , "NACE: " : '' , "Empleados: " : '', "Dirección: " : ""  , "Web: " : '', "Mail Empresa: " : '', "Teléfono Empresa: " : '', "Teléfono2 Empresa: " : '', "Nombre Contacto: " : '', "Apellidos Contacto: " : '', "Cargo: " : '', "Mail Contacto: " :'', "Teléfono Contacto: " : '', "Móvil Contacto: " : ''}):
    
        #load_image= Image.open("recursos/upload.png")
        #load_image.resize((6,6))
        #load_image_icon = ImageTk.PhotoImage(load_image)

        add_company_frame = Toplevel()
        add_company_frame.title("Add Company")
        add_company_frame.configure(bg = "#f4f4f4")
        add_company_frame.grid_columnconfigure(0 , weight = 1)
        
        files_frame = tk.Frame(add_company_frame)
        files_frame.configure(bg = "#f4f4f4")
        files_frame.grid(row = 0 , column = 0 , columnspan = 2 , sticky = W+E)
        files_frame.grid_columnconfigure(0, weight=1)
        
        files_top = ttk.Label(files_frame , text = "")
        files_top.grid(row = 0 , column = 0, sticky = W+E ) 
        
        files_button = ttk.Button(files_frame , text = "Subir desde archivo (Varias Empresas)" , command = AddInfo.add_companies_from_file)
        files_button.grid(row = 1 , column = 0 , columnspan = 2 , sticky = W+E , padx = 20)        
        
        company_frame = ttk.Labelframe(add_company_frame , text = 'Empresa')
        company_frame.grid(row = 1 , column = 0 , columnspan = 4 , padx = 10 , pady = 5 , sticky = W+E)
        
        #company_frame.grid_columnconfigure(0 , weight = 1)   
        company_frame.grid_columnconfigure(1 , weight = 1)
        
        company_name = ttk.Label(company_frame , text ="Nombre: ")
        company_name.grid(row =0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_company_name = ttk.Entry(company_frame)
        entry_company_name.grid(row =0 , column = 1 , columnspan = 5 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_nif = ttk.Label(company_frame , text  = "N.I.F.: ")
        company_nif.grid(row =0 , column = 6 , padx = 5 , pady = 5)
        
        entry_company_nif = ttk.Entry(company_frame)
        entry_company_nif.grid(row =0 , column = 7 , padx = 5 , pady = 5)
        
        company_activity = ttk.Label(company_frame , text ="Actividad: ")
        company_activity.grid(row =1 , column = 0 , columnspan= 7 , padx = 5 , pady = 5 , sticky = "w")
        
        nace_list_combo = ttk.Combobox(company_frame, state = 'readonly' , values = LoadInfo.nace_list())
        nace_list_combo.grid(row =2 , column = 0 ,  columnspan= 7 , padx = 5 , pady = 5 , sticky = W+E)
        nace_list_combo.current(newindex = 0)
        #nace_list_combo.bind("<<ComboboxSelected>>" , self.test)
        
        number_of_employees = ttk.Label(company_frame, text = "Empleados: ")
        number_of_employees.grid(row = 1 , column = 7 , padx = 5 , pady = 5 , sticky = "w")
        
        number_of_employees_entry = ttk.Combobox(company_frame, state = 'readonly' , values =  [" < 10" , "10 - 50" , "50 - 250" , " > 250"])
        number_of_employees_entry.grid(row =2 , column = 7  , padx = 5 , pady = 5 , sticky = W+E)
        number_of_employees_entry.current(newindex = 0)
        number_of_employees_entry.bind("<<ComboboxSelected>>")
        
        company_adress = ttk.Labelframe(add_company_frame , text ="Dirección: ")
        company_adress.grid(row = 2 , column = 0 , columnspan = 4 , padx = 10 , pady = 5 , sticky = W+E)
        company_adress.grid_columnconfigure(0 , weight = 1)
        company_adress.grid_columnconfigure(1 , weight = 1)
        
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
        
        company_adress2 = ttk.Frame(company_adress)
        company_adress2.grid(row = 2 , column =0 , columnspan = 8 , padx = 5 , pady = 5 , sticky = W+E)  
        
        company_city = ttk.Label(company_adress2 , text = "Ciudad: ")
        company_city.grid(row = 0 , column = 0 , padx = 5 , pady = 5)# , sticky = W+E)
        
        company_city_entry = ttk.Entry(company_adress2)
        company_city_entry.grid(row = 0 , column = 1, columnspan = 2 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_province= ttk.Label(company_adress2 , text = "Provincia: ")
        company_province.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = E)
        
        company_province_entry = ttk.Entry(company_adress2)
        company_province_entry.grid(row = 0 , column = 4, columnspan = 2 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_postal_code = ttk.Label(company_adress2 , text = "C.P.: ")
        company_postal_code.grid(row = 0 , column = 6 , padx = 5 , pady = 5 )# , sticky = W+E)
        
        company_postal_code_entry = ttk.Entry(company_adress2)
        company_postal_code_entry.grid(row = 0 , column = 7 , padx = 5 , pady = 5 )# , sticky = W+E)
        
        company_contact = ttk.Labelframe(add_company_frame , text = "Contacto")   
        company_contact.grid(row = 3, column = 0 , columnspan = 4 , padx = 10 , pady = 5 , sticky = W+E)
        
        company_contact.grid_columnconfigure(1 , weight = 1)   
        company_contact.grid_columnconfigure(3 , weight = 1)       
        
        company_web = ttk.Label(company_contact , text ="Web: ")
        company_web.grid(row =2 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_company_web = ttk.Entry(company_contact)
        entry_company_web.grid(row = 2 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_mail = ttk.Label(company_contact , text ="Mail: ")
        company_mail.grid(row =2 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_company_mail = ttk.Entry(company_contact)
        entry_company_mail.grid(row =2 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_phone = ttk.Label(company_contact , text ="Teléfono: ")
        company_phone.grid(row =3 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_company_phone = ttk.Entry(company_contact)
        entry_company_phone.grid(row =3 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_phone2 = ttk.Label(company_contact , text ="Teléfono2: ")
        company_phone2.grid(row =3 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
        
        entry_company_phone2 = ttk.Entry(company_contact)
        entry_company_phone2.grid(row =3 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
        
        frame_contact_person = ttk.Labelframe(add_company_frame , text = "Contact Person")
        frame_contact_person.grid(row = 4 , column = 0  , padx = 10 , pady = 5 , sticky = W+E)
        
        frame_contact_person.grid_columnconfigure(0 , weight = 1)
        frame_contact_person.grid_columnconfigure(1 , weight = 1)
        frame_contact_person.grid_columnconfigure(2 , weight = 1)
        
        label_name = ttk.Label(frame_contact_person, text = "Nombre:")
        label_name.grid(row = 0 , column = 0 , padx = 5 , sticky = W+E)
        
        entry_name = ttk.Entry(frame_contact_person)
        entry_name.grid(row = 1 , column = 0 , padx = 5 , sticky = W+E)
        
        label_surname = ttk.Label(frame_contact_person , text = "Apellidos")
        label_surname.grid(row = 0 , column = 1 , padx = 5 , sticky = W+E)
        
        entry_surname = ttk.Entry(frame_contact_person)
        entry_surname.grid(row = 1 , column = 1 , padx = 5 , sticky = W+E)
        
        label_job_title = ttk.Label(frame_contact_person , text = "Cargo")
        label_job_title.grid(row = 0 , column = 2 , sticky = W+E , padx = 5)
        
        entry_job_title = ttk.Entry(frame_contact_person)
        entry_job_title.grid(row = 1 , column = 2, sticky = W+E , padx = 5)
        
        label_mail = ttk.Label(frame_contact_person , text = "Mail")
        label_mail.grid(row = 2 , column = 0 , sticky = W+E , padx = 5)
        
        entry_mail = ttk.Entry(frame_contact_person)
        entry_mail.grid(row = 3 , column = 0, sticky = W+E , padx = 5 , pady = 5)
        
        label_phone = ttk.Label(frame_contact_person , text = "Teléfono")
        label_phone.grid(row = 2 , column = 1 , sticky = W+E , padx = 5)
        
        entry_phone = ttk.Entry(frame_contact_person)
        entry_phone.grid(row = 3 , column = 1, sticky = W+E , padx = 5 , pady = 5)
        
        label_mobile = ttk.Label(frame_contact_person , text = "Móvil")
        label_mobile.grid(row = 2 , column = 2 , sticky = W+E , padx = 5)
        
        entry_mobile = ttk.Entry(frame_contact_person)
        entry_mobile.grid(row = 3 , column = 2, sticky = W+E , padx = 5 , pady = 5)
        
        save_company_button = ttk.Button(add_company_frame , text = "Add" , command = lambda: CheckInfo.test_add_company(self , add_company_frame , {"Nombre Empresa: " : entry_company_name.get(), "N.I.F.: " : entry_company_nif.get(), "NACE: " : nace_list_combo.get(), "Empleados: " : number_of_employees_entry.get(), "Dirección: " : f"{company_street.get()}-{company_street_number.get()}-{company_street_floor.get()}-{company_city_entry.get()}-{company_province_entry.get()}" , "Código Postal: ": company_postal_code_entry.get() , "Web: " : entry_company_web.get(), "Mail Empresa: " : entry_company_mail.get(), "Teléfono Empresa: " : entry_company_phone.get(), "Teléfono2 Empresa: " : entry_company_phone2.get(), "Nombre Contacto: " : entry_name.get(), "Apellidos Contacto: " : entry_surname.get(), "Cargo: " : entry_job_title.get(), "Mail Contacto: " : entry_mail.get(), "Teléfono Contacto: " : entry_phone.get(), "Móvil Contacto: " : entry_mobile.get()}))
        save_company_button.grid(row = 5 , column = 0 , pady = 10)
        
        Pops.center_window(Pops , add_company_frame)
    
       
    def show_new_company(company_name , contact_name , contact_surname , contact_job):
        
        show = Toplevel()
        show.title("Se ha creado una nueva Empresa") 
        show.configure(bg = "#f4f4f4")
        show.resizable(0,0)

        
        frame = LabelFrame(show , text = "Nueva Empresa" , labelanchor = 'n')
        frame.grid(row = 0 , column =0 , columnspan = 2 , padx = 20 , pady = 10 , sticky = W+E)
        message = Label(frame ,  text= 
        f"""
        Empresa:
        {company_name}

        Persona de Contacto: 
        {contact_name} {contact_surname} 
        
        Cargo
        {contact_job}
        """ , justify = 'left')
        message.grid(row = 0 , column =0 , columnspan = 2 ,  sticky = W+E)
        
        show_button = ttk.Button(show , text = "Ver Empresa" , width = 20)
        show_button.grid(row = 1 , column = 0 , padx = 10 , pady = 10 , sticky = W+E)
        
        continue_button = ttk.Button(show , text = "Continuar" , width = 20)
        continue_button.grid(row = 1 , column = 1 , padx = 10 , pady = 10 , sticky = W+E)
        
        Pops.center_window(Pops , show)
        
 
    def current_combo(data, combo):
        
        if combo == "employees":
            combo = [" < 10" , "10 - 50" , "50 - 250" , " > 250"]

        index = combo.index(data)
            
        return (index)   
     
 
 
class MyCalendar():
    
    def calendar_toggle_frame(self , place):
        
        if place == "general":
            frame = self.frame_calendar
            frame.place(x = 320, y = 50) 
            
        elif place == 'next':
            frame = self.frame_calendar_next
            frame.place(x = 0, y = 242) 
            
        
        elif place == "pop":
            frame = self.frame_calendar_pop
            frame.place(x = 0, y = 272) 
            
        frame.lift() 
        
        if frame.winfo_ismapped(): # Comprueba si self.frame_container_calendar es visible, si es visible lo oculta con self.frame_container_calendar.grid_forget()
            frame.place_forget()
                
    
    def calendar(self , place):  
        
        frame = MyCalendar.place_to_frame(self , place)
        
        hours_list = [
            "08:00", "08:15", "08:30", "08:45",
            "09:00", "09:15", "09:30", "09:45",
            "10:00", "10:15", "10:30", "10:45",
            "11:00", "11:15", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45",
            "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:15", "14:30", "14:45",
            "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45",
            "17:00", "17:15", "17:30", "17:45",
            "18:00", "18:15", "18:30", "18:45",
            "19:00", "19:15", "19:30", "19:45",
            "20:00", "20:15", "20:30", "20:45",
              ]
        
        header_calendar = StringVar(value = "View")
        
        label_calendar = tk.Label(frame , textvariable = header_calendar , bg = 'LightBlue4' , fg = "white")
        
        label_calendar.pack(fill = "x" , expand = True)
        
        frame.calendar = Calendar(frame , selectedmode = "day" , date_pattern = "yyyy-mm-dd" , selectbackground = 'LightBlue4') # Para poder ordenarlo en la DB "YYYY-MM-DD"
        frame.calendar.pack()
        
        if place == "general":
            
            frame.calendar.bind("<<CalendarSelected>>", lambda e: MyCalendar.general_calendar_date(self , place , frame.calendar.get_date() , e))
       
        elif place != "general":
            
            if place == 'next':
                header_calendar.set("Next Contact")
                log_type = 'next'
                
            else:
                header_calendar.set("Pop Up")
                log_type = "pop"
                
            hour = ttk.Combobox(frame , justify = "left" , values = hours_list , width = 10)
            hour.current(newindex = 0)
            hour.config(justify=CENTER)
            hour.pack(fill = "x" , expand = True , anchor = "center")
            send = ttk.Button(frame , text = "Save" , command = lambda: Logs.add_log(self , frame.calendar.get_date() , log_type , hour.get()))#lambda: MyCalendar.format_date(self , place , hour = hour.get()) )
            send.pack(pady = 5)
            

    def general_calendar_date(self , place , date , event):
        
        try:
            fecha_seleccionada = date ## Para poder ordenarlo en la DB "YYYY-MM-DD" 
            month = int(fecha_seleccionada[5:7])
            year = int(fecha_seleccionada[0:4])
            
            if int(fecha_seleccionada[-2]) == 0:
                day = int(fecha_seleccionada[-1])
                
            else:
                day = int(fecha_seleccionada[-2:])
            
            LoadInfo.load_contacts(self , self.employee.get() , fecha_seleccionada)
            
            self.fecha.set(datetime(year,month,day).strftime("%d %B")) 
            
            MyCalendar.calendar_toggle_frame(self , place)
        
        except AttributeError:
            pass  
        
        except Exception as e:
            print("general_calendar_date" , e)
            mb.showwarning("Error" , f"Ha habido un problema con las fechas {e}") 
                   
        frame = MyCalendar.place_to_frame(self , place)
        
        
    def format_date(self , place , hour): 
        frame = MyCalendar.place_to_frame(self , place)
        print(f"Date From: {place} - {frame.calendar.get_date()} {hour}") 
        MyCalendar.calendar_toggle_frame(self  , place)


    def place_to_frame(self , place):
        
        try:
            if place == "general":
                frame = self.frame_calendar 
            
            elif place == 'next':
                frame = self.frame_calendar_next
            
            elif place == "pop":
                frame = self.frame_calendar_pop 

            return frame
        
        except Exception as e:
            print("PlaceTo.." , e)
            
            
    def format_date_to_show(date):
        try:
            date = datetime.strptime(date,'%Y-%m-%d %H:%M').strftime("%d %B %Y %H:%M")
            
            return date

        except Exception as e:
            mb.showwarning("Error al Introducir la Hora" , f'\nFecha introducida: {date[-5:]}\n\nFormato Válid: 08:25 (HH:MM)')
        



class LoadInfo():

    def sales_root(self):
        
        print(f"-----------------------------LOAD INFO{self.active_employee_id.get()}")
    
    def check_employee(root , employee_password , alias , window):
                
        employees =  db.session.query(Employee).all()
        exists = False
        
        for employee in employees:
            if employee.employee_alias == alias and employee.password == str(employee_password):
                
                exists = True
                window.destroy()
                
                LoadInfo.load_contacts(root , employee.id_employee , date = datetime.now())
                print(f" Empleado {employee.id_employee}")
                
                alias = LoadInfo.employees_list().index(alias)
                    
                root.employee.current(newindex = alias)
                root.combo_state.current(newindex=2)
                
                root.active_employee_id.set(employee.id_employee)
                               
                Alerts.refresh_alerts(root , employee.id_employee)
               
        if not exists:
            mb.showwarning("Login Error" , "El usuario o la contraseña no son correctos")
            window.lift()

    
    
    def on_heading_click(self , query):
        
        if query == 'state':
            query = "state"
        elif query == 'days':
            query = "days"
        elif query == 'client':
            query = "name"
        elif query == 'last':
            query = "last"
        elif query == 'next':
            query = 'next'
        elif query == 'postal_code':
            query = 'cp'
        
        employee_id = self.active_employee_id.get()
        date = datetime.strptime(self.fecha.get() + f' {datetime.now().year}' , '%d %B %Y')
        
        LoadInfo.load_contacts(self , employee_id , date , query)
        


    def load_contacts(self , employee_id_sended , date , query = 'last' , state_sended = "Contact"): # last_gestion =db.session.query(func.max(Contact.contact_counter )).scalar() Hay que tener en cuenta el counter para que no muestre contactos de una gestión anterior
        
        dot = '◉'  # ASCII
        dataframe = {"state" : [] , "days" : [] , "name" : [] , "last" : [] , 'next' : [] , "cp" : [] , "pop" : []}
        pd_filter = query
        ascending_value = False
        state_view = state_sended

        if str(employee_id_sended).isdigit():
            pass
        
        else:
            employee_id_sended = db.session.query(Employee).filter(Employee.employee_alias == employee_id_sended).first()
            employee_id_sended = employee_id_sended.id_employee

        if not date:
            date = str(datetime.now())[:11]    

        try:
            clean = self.info.get_children()
            
            for x in clean: 
                self.info.delete(x)
                        
        except Exception as e:
            print("load_contacts" , e)
        
        contacts = 0
        bgcolor = 0
        
        clients = db.session.query(Client).filter(and_(Client.state == state_view , Client.employee_id == int(employee_id_sended))).all() # Cada objeto en la lista será el primer contacto dentro de su respectivo grupo de cliente
        
        self.info.tag_configure("odd", background="snow2" )
        self.info.tag_configure("even", background="white")
        self.info.tag_configure("font_red", foreground="red")
        
        scrollbar = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.info.yview)
        scrollbar.grid(row = 0, column = 1 , sticky = "ns")
        self.info.configure(yscroll=scrollbar.set)
        
        ordenado = LoadInfo.contacts_dataframe(self, clients, dataframe, pd_filter , ascending_value)
        
        contacts = LoadInfo.row_colors(self, clients , ordenado , date , bgcolor , contacts , dot)
                
        self.contacts.set(f"Contactos: {contacts}")
        print("*** Llamada desde load_contacts")
        Alerts.check_pop_ups(self , employee_id_sended )
    
    
    def contacts_dataframe(self, clients, dataframe, pd_filter , ascending_value): 
        
        for i , client in enumerate(clients):  
            # De aquí se deber cargar el útlimo contacto con el "dot" si fuera necesario
            contact = db.session.query(Contact).filter(Contact.client_id == client.id_client).order_by(Contact.id_contact.desc()).first()
            
            try:
                dataframe["state"].append(client.state)
                dataframe["days"].append(LoadInfo.get_days(client))
                dataframe["name"].append(client.name)
                
                if contact.last_contact_date:
                    dataframe["last"].append(contact.last_contact_date)
                    
                else:
                    dataframe["last"].append(".")
                    
                if contact.next_contact:
                    dataframe['next'].append(f'{contact.next_contact}')
                    
                else:
                    dataframe['next'].append(f'{"."}')

                dataframe["cp"].append(client.postal_code)  
                dataframe["pop"].append(contact.pop_up)
                #print(f"{client.name} - {contact.pop_up}")
            except Exception as e:
                print("load_contacts" , e)
            
            #print(dataframe)
        ordenado = pd.DataFrame(dataframe)
        ordenado = ordenado.sort_values(by = pd_filter , ascending = ascending_value)
        ordenado = ordenado.reset_index(drop = True)
        
        return ordenado
    
    
    def row_colors(self, clients , ordenado , date , bgcolor , contacts , dot):
        for i , client in enumerate(clients):

            if ordenado.at[i, 'next'] <= str(date)[:11] + "23:59":               
              
                if int(ordenado.at[i, "days"]) >= 80:
                    font = "font_red"
                    
                else:
                    font = ""
                
                if bgcolor % 2 == 0:
                    color= "odd"
                
                else:
                    color= "even"
                #print(ordenado.at[i, 'pop'])
                if ordenado.at[i, 'pop'] == True:
                    next_contact = f"{MyCalendar.format_date_to_show(ordenado.at[i, 'next'])} {dot}"
                
                else:
                    next_contact = f"{MyCalendar.format_date_to_show(ordenado.at[i, 'next'])}"
                    
                self.info.insert("" , 0 , text = ordenado.at[i, 'state'] , values = (str(ordenado.at[i, 'days']).lstrip("0") , ordenado.at[i, 'name'] , MyCalendar.format_date_to_show(ordenado.at[i, 'last'])  , next_contact , ordenado.at[i, 'cp']) , tags=(color, font) )
               
                contacts += 1
                bgcolor += 1
                
        return contacts

            
    def get_days(client):
        
        today = datetime.now()
        
        try:
            date = client.start_contact_date
            
            days = str(today - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).split(" ")[0] 
            
            if len(days) == 1:
                days = f'0{days}'
        
        except Exception as e:
            print("get_days" , e) 
            days = 0
            
        return days
    
    
    def get_client_name(tree , event):
        
        try:
            row = tree.info.focus()
            print(row)
            item = tree.info.item(row)
            client_name = item['values'][1]
            
            GetInfo.load_client_info(tree , client_name)
        
        except IndexError:
            pass
        
        except Exception as e:
            print(e , type(e))
            mb.showerror("Error en Get Client Name" ,  e)
        
        
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
                lista_nace.append( valor[0] + " - " + valor[1])
            
        return lista_nace
        
        
    def employees_list():
        
        employees_list = []
        employees = db.session.query(Employee).all()
        
        for alias in employees:
            employees_list.append(alias.employee_alias)
        
        return employees_list
        
        
    def companies_state(self, event):  # Recibir valor del Combobox
        
        item = self.combo_state.get()
        #frame = MyCalendar.place_to_frame(self , place)
        fecha_seleccionada = self.frame_calendar.calendar.get_date()
        print(item, fecha_seleccionada)
        
        if item == "Lead":
            state_sended = "Lead"
        
        if item == "Candidate":
            state_sended = "Candidate"
        
        if item == "Contact":
            state_sended = "Contact"
        
        if item == "Pool":
            state_sended = "Pool"
        
        if item == "All":
            state_sended = "All"
            
        LoadInfo.load_contacts(self , self.active_employee_id.get() , fecha_seleccionada , 'last' , state_sended) 
    
class GetInfo():
    
    def load_comments(self , nif):
        
        frame_log = CTkScrollableFrame(self.frame_tree, fg_color = "lightgray")
        frame_log.grid(row = 3 , pady = 5 , padx = 3 , sticky = 'nsew')
        
        try:
            for log in frame_log.winfo_children():
                log.destroy()
            
        except UnboundLocalError:
            print("NOT destroyed Logs")
        #contact = db.session.query(Contact).filter(Contact.client_id == client.id_client).order_by(Contact.last_contact_date).first()
        client = db.session.query(Client).filter(Client.nif == nif).first()
        comments = db.session.query(Contact).filter(Contact.client_id == client.id_client).order_by(Contact.id_contact.desc()).all()
        comments_counter = 0
        
        for comment in comments:
            
            log_frame = ttk.Frame(frame_log )
            log_frame.pack(fill = "x" , expand = True , pady = 2)
            
            label_info = tk.Label(log_frame , text = f"{GetInfo.load_info_log(comment.client_id , comment.last_contact_date , comment.contact_type)}" , bg = 'LightBlue4' , fg = "white")
            label_info.pack(fill = "x" , expand = True)
            
            #frame_log_content = CTkScrollableFrame(log_frame , height = 10)
            #frame_log_content.pack(fill = "x" , expand = True)
            
            label_content = tk.Label(frame_log , text = f"{comment.log}" , bg = "White" , anchor = 'w' ,  wraplength = 570 , justify = "left")
            label_content.pack(fill = "x" , expand = True)
            
            comments_counter += 1
            
        self.company_id.set(client.id_client)
        self.active_employee_id.set(client.employee_id)
        #print('client ID' , client.id_client)
        

    def load_info_log(client_by_id , last_contact , contact_type):
        
        dot = '◉'
        try:
            comment = db.session.query(Contact).filter(and_(Contact.client_id == client_by_id) , Contact.last_contact_date == last_contact).first()
            contact_person = db.session.get(ContactPerson , comment.contact_person_id)
            employee = db.session.get(Employee , comment.contact_employee_id)
            
            if 'pop' in contact_type:
                pop = dot
            else:
                pop = ""
                
            return f"{MyCalendar.format_date_to_show(last_contact)} {contact_person.contact_name} {contact_person.contact_surname} [{employee.employee_alias}] {pop}"
            
        except Exception as e:
            print("load_info_log" , e)


    def load_client_info(tree , client_name):
        
        client = db.session.query(Client).filter(Client.name == client_name).first()
        contact_person = db.session.get(ContactPerson , client.contact_person)
        
        try:
            tree.entry_company_name.delete(0 , END)
            
            tree.entry_nif.delete(0 , END)
            
            tree.entry_adress.delete(0 , END)
            
            tree.entry_web.delete(0 , END)
            
            tree.entry_company_mail.delete(0 , END)
            
            tree.entry_company_phone.delete(0 , END)
            
            tree.entry_company_phone2.delete(0 , END)
            
            tree.entry_contact_name.delete(0 , END)
            
            tree.entry_contact_surname.delete(0 , END)
            
            tree.entry_job_title.delete(0 , END)
            
            tree.entry_contact_mail.delete(0 , END)
            
            tree.entry_contact_phone.delete(0 , END)
            
            tree.entry_mobile.delete(0 , END)
            
            GetInfo.load_comments(tree , client.nif)
        
        except Exception as e:
            print(f'Error al borrar los datos: {e}')
            
        try:
            adress = GetInfo.format_adress_to_Show(client.adress , client.postal_code)
            tree.entry_company_name.insert(0 , client.name) # Es lo mismo que placeholder
            tree.entry_nif.insert(0, client.nif)
            tree.entry_adress.insert(0 , adress)
            tree.entry_activity.current(newindex = Pops.current_combo(client.activity , LoadInfo.nace_list()))
            tree.entry_employees.current(newindex = Pops.current_combo(client.number_of_employees , "employees"))
            tree.entry_web.insert(0, client.web)
            tree.entry_company_mail.insert(0 , client.mail)
            tree.entry_company_phone.insert(0, client.phone)
            tree.entry_company_phone2.insert(0, str(client.phone2))
            tree.entry_contact_name.insert(0, contact_person.contact_name)
            tree.entry_contact_surname.insert(0,contact_person.contact_surname)
            tree.entry_job_title.insert(0, contact_person.contact_job_title)
            tree.entry_contact_mail.insert(0,contact_person.contact_mail)
            tree.entry_contact_phone.insert(0, contact_person.contact_phone)
            tree.entry_mobile.insert(0 , contact_person.contact_mobile)
            tree.company_id.set(client.id_client)
        except Exception as e:
            print(f'Error al cargar los datos: {e}')
        
        #tree.notes.delete(0 , END)
        #tree.notes.insert(0 , "686289365")
    
    def format_adress_to_Show(adress , cp):
        
        street , number , floor , city , province = adress.split("-")
        
        adress_to_show = f'{street}, {number}  {floor} {city} ({str(cp)})'
        
        return adress_to_show
        
            
   
class CheckInfo:
    
        
    def check_name(self , name , wich_name , data , update = False):
        
        try:
            if name != "":
                return name
            
            else:
                data['Nombre Empresa: '] == False
                raise Exception
        
        except Exception as e:
            mb.showwarning(f"{wich_name}" , f"El formato del {wich_name} no es correcto, comprueba el {wich_name}.")
       
       
    def check_surname(self , surname , data , update = False):
        
        try:
            if surname != "":
                return surname
            
            else:
                data['Nombre Empresa: '] = False
                raise Exception
        
        except Exception as e:
            mb.showwarning("Persona de Contacto (Apellido)" , f"El formato del Apellido no es correcto, comprueba el Apellido.")

        
    def check_phones(self , phone , which_phone , data , update = False):
             
        try: 
            if len(phone) == 9 and str(phone).isdigit():
                return phone
            
            else:
                data['Nombre Empresa: '] = False
                raise Exception
        
        except Exception as e:
            mb.showwarning("Teléfonos" , f"El formato del {which_phone} no es correcto, comprueba el {which_phone}.")

    
    def check_mail(self , complete_mail , wich_mail , data , update = False):
          
        try: 
            mail = complete_mail.split(".")
            
            if mail[0] != "www" and "@" in complete_mail and len(mail[-1] < 2):
                return complete_mail
            
            else:
                data['Nombre Empresa: '] = False
                raise Exception
        
        except Exception as e:
            mb.showwarning("Teléfonos" , f"El formato del {wich_mail} no es correcto, comprueba el {wich_mail}.")
 

    def check_nif(self , nif , data , update = False):
        
        nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']
        try:             
            if nif[0] in nif_check or len(nif) == 9:
                return nif
            
            else:
                data['Nombre Empresa: '] = False
                raise Exception
        
        except Exception as e:
            mb.showwarning("N.I.F." , f"El formato del N.I.F. no es correcto, comprueba el N.I.F.")
 

    
    def check_postal_code(self , code , data , update = False):
        
        try:
            if len(code) == 5 and str(code).isdigit():
                
                if update is not False:
                    print('OK')
                    
                else:
                    print(code)
                    return code

            else:
                data['Nombre Empresa: '] = False
                raise Exception
        
        except Exception as e:
            mb.showwarning("Código Postal" , f"El formato del Código Postal no es correcto, comprueba el Código Postal")
 
 
    def check_web(self , web , data , update = False):
        
        try:
            web_test = web.split(".")
            
            if web_test[0] == "www":
                if len(web_test[-1]) >= 2:
                    return True
            else:
                data['Nombre Empresa: '] = False
                raise Exception
            
        except Exception as e:
            print(e)
            mb.showerror("Error en Web" , "\n\nEl formato de la web no correcto.\n\n")
            
    
    def test_add_company(self , add_company_frame , data):
        
        try:
            company_name = CheckInfo.check_name(self , data["Nombre Empresa: "] , data , 'Nombre Empresa' ,  'remplazar')
            nif = CheckInfo.check_nif(self , data["N.I.F.: "] ,  'remplazar')              
            postal_code = CheckInfo.check_postal_code(self , data["Código Postal: "] , data , 'remplazar') 
            web = CheckInfo.check_web(self , data["Web: "] , 'remplazar')  ####
            company_mail = CheckInfo.check_mail(self , data["Mail Empresa: "] , "Mail Empresa" , data ,  'remplazar') 
            company_phone = CheckInfo.check_phones(self , data["Teléfono Empresa: "] , 'Teléfono de Empresa' , data , 'remplazar')
            company_phone2 = CheckInfo.check_phones(self , data["Teléfono2 Empresa: "] , 'Teléfono de Empresa2' , data , 'remplazar')
            
            contact_name = CheckInfo.check_name(self , data["Nombre Contacto: "] , 'Nombre Contacto' , data ,  'remplazar')
            contact_surname = CheckInfo.check_surname(self , data["Apellidos Contacto: "] ,  data , 'remplazar')
            contact_phone = CheckInfo.check_phones(self , data["Teléfono Contacto: "] , 'Teléfono de Contacto' , data , 'remplazar')
            contact_mobile = CheckInfo.check_phones(self , data["Móvil Contacto: "] , 'Teléfono de Contacto' , data , 'remplazar')
            contact_mail = CheckInfo.check_mail(self , data["Mail Contacto: "] , "Mail Contacto" , data ,  'remplazar') 
            values_info = [company_name , nif , postal_code , web , company_mail , company_phone , company_phone2 , contact_name , contact_surname , contact_phone , contact_mobile , contact_mail]

            if data["Nombre Empresa: "]:
                
                AddInfo.add_company(self , data , add_company_frame)
                            
            else:
                mb.showwarning( "Faltan Datos:" , 
                f"""Faltan Datos o son incorrectos, compruebalos.
                
                    Empresa:                               
                
                    Nombre:   {data['Nombre Empresa: ']}   
                    N.I.F:    {data['N.I.F.: ']}       
                    Teléfono: {data['Teléfono Empresa: ']} 
                    Mail:     {data['Mail Empresa: '] }    
                    
                    Persona de Contacto: 
                
                    Nombre:    {data['Nombre Contacto: ']}
                    Apellidos: {data['Apellidos Contacto: ']}
                    Teléfono:  {data['Teléfono Contacto: ']}
                    Mail: {data["Mail Contacto: "]}
                """ 
                )
                
                add_company_frame.destroy()
                
                Pops.new_company(data)
            
        except Exception as e:
            print(e)
                

        
        
class AddInfo():
    
    
    def add_company(self, data , add_company_frame):
        
        
        try:
            employee_adder = self.active_employee_id.get()
            vcontact_person = AddInfo.add_contact_person(data , employee_adder)
            
            company = Client(data["Nombre Empresa: "] , data["N.I.F.: "] , data["Dirección: "] , data["Código Postal: "], data["Web: "] , data["Mail Empresa: "] , data["Teléfono Empresa: "] , data["Teléfono2 Empresa: "] , data["NACE: "] , vcontact_person.id_person , employee_adder , "Pool", data["Empleados: "] , datetime.now(),)
            vcontact_person.client_id = vcontact_person.id_person
            
            db.session.add(company)
            db.session.commit()
            
            
            vcontact_person.client_id = db.session.query(Client).order_by(Client.id_client.desc()).first() # Asignamos la persona de contacto creada.
            
            db.session.close()
            
            add_company_frame.destroy() 
             
            Pops.show_new_company(data['Nombre Empresa: '] , data['Nombre Contacto: '] , data['Apellidos Contacto: '] , data['Cargo: '])

        except Exception as e:
            
            if isinstance(e, IntegrityError) or isinstance(e, SQLAlchemyError) :
                print("add_company" , e)
                mb.showerror("Error de Integridad" , f"La empresa ya existe, el Nombre o el N.I.F. ya existen en la Base de Datos.")
                
            else:
                print("add_company" , e)
                mb.showerror("Ha ocurrido un error inesperado" , f"{e}")
                
            db.session.delete(vcontact_person.id_person)
            db.session.close()
            
            add_company_frame.destroy()    
            
            Pops.new_company(data)
 
            
    def add_companies_from_file():
    
        excel_paht = filedialog.askopenfilename(title = "Cargar desde Excel" , filetypes = (("Ficheros Excel" , "*.xlsx"),))
        excel = openpyxl.open(excel_paht)
        
        rows = []
        ready = []
        errores = []
        
        for row in excel["Sheet"].rows:
            
            for cell in row:
                rows.append(cell.value)
                
            ready.append(rows)
            rows = []
        
        for i , registro in enumerate(ready):

            new = Client(registro[0] , registro[1] , registro[2] , registro[3] , registro[4] , registro[5] , registro[6] , registro[7] , registro[8] , registro[9] , registro[10] , registro[11] , registro[12] , registro[13] , registro[14])
            
            try:
                db.session.add(new)
                db.session.commit()
                
            except Exception as e:   
                errores.append(i+1)
            
        db.session.close()
        
        if len(errores) > 0:
            
            mb.showwarning("Errores en la inserción de Empresas" , f"Empresas que no han podido ser insertadas: {errores}")    
            
     
    def add_contact_person(data , employee_adder):
        
        try:                                                                                                                                                                                                # TO-DO sustituir por la empresa adminstradora
            contact_person = ContactPerson(data["Nombre Contacto: "] , data["Apellidos Contacto: "] , data["Cargo: "] , data["Teléfono Contacto: "] , data["Móvil Contacto: "] , data["Mail Contacto: "] , "Id de la Empresa" , employee_adder)
                
            db.session.add(contact_person)
            db.session.commit()
            
            vcontact_person = db.session.query(ContactPerson).order_by(ContactPerson.id_person.desc()).first() # Se asigna el último empleado introducido en la DB, es decir el que se crea a la vez que la empresa.
            
            return vcontact_person
        
        except Exception as e:
            mb.showerror("Error al añadir Persona de Contacto" , f"{e}")
            

class Alerts():
    
    def check_pop_ups(self , employee_id  , log = False):
        
        date = str(datetime.now())
        print("Cheking pop Ups..." , date)
        old_alerts = alerts[:]     

        try:
            search = db.session.query(Contact).filter(and_(Contact.contact_employee_id == employee_id , Contact.pop_up == True)).all()

            for alert in search:

                if str(alert.next_contact) <= str(date)  and alert.id_contact not in alerts:

                    alerts.append(alert.id_contact)
    
            new_alerts = alerts
            
            if new_alerts != old_alerts and log == False:
                Alerts.pop_up_alert(self , employee_id , date , new_alerts)
            
        except Exception as e:
            print(e)

        


    def pop_up_alert(self , employee_id , date , now_alerts = alerts):
        
        window = Toplevel()
        window.configure(bg = "#f4f4f4")
        window.configure(bg = "#f4f4f4")
        window.title(f"Pop Ups [{len(alerts)}]")

        main_frame = CTkScrollableFrame(window , width = 600 , fg_color = "transparent")
        main_frame.grid(row = 0 , column = 0 , sticky = 'nswe')
        main_frame.grid_columnconfigure(0 , weight = 1)
        
            
        for i, id_contact in enumerate(now_alerts):
            
            show_alert_frame = CTkFrame(main_frame , fg_color = 'lightgray' , corner_radius = 3 )
            show_alert_frame.grid(row = i , column = 0 , sticky = 'we' , padx = 10 , pady = 5)
            show_alert_frame.grid_columnconfigure(0 , weight = 1)
            
            alert_content = Alerts.alert_info(self , id_contact)
            
            label_alert_name = ttk.Label(show_alert_frame , text = alert_content[0])
            label_alert_name.configure(background = "lightgray")
            label_alert_name.grid(row = 0 , column = 0 , sticky = 'we' , padx = 10 , pady = 5)
            
            label_alert_log = ttk.Label(show_alert_frame , text = alert_content[2] , wraplength = 250)
            label_alert_log.configure(background = "lightgray")
            label_alert_log.grid(row = 0 , column = 1 , sticky = 'we' , padx = 10 , pady = 5)
            
            label_alert_date = ttk.Label(show_alert_frame , text = alert_content[3])
            label_alert_date.configure(background = "lightgray")
            label_alert_date.grid(row = 0 , column = 2 , sticky = 'we' , padx = 10 , pady = 5)
            
            show_client_button = CTkButton(show_alert_frame , text = 'Ver' , corner_radius = 2 , fg_color = '#f4f4f4' , text_color = 'snow3' , hover_color = 'LightBlue4' , width = 60 , command = lambda name = alert_content[1]: Alerts.view_alert(self , name , window ,  employee_id , date))
            show_client_button.grid(row = 0 , column = 3 , padx = 10 , pady = 5)          
            
            Pops.center_window(self , window)
            window.lift()

    
    def alert_info(self , id_contact):
        
        contact_info = db.session.get(Contact , id_contact)
        client = db.session.get(Client , contact_info.client_id)
        text_to_label_alert = [f"[{contact_info.id_contact}] {client.name}" , client.name , contact_info.log ,MyCalendar.format_date_to_show(contact_info.next_contact)]
        
        return text_to_label_alert
    
    
    def refresh_alerts(self , employee_id):
        
        threading.Timer(60 , Alerts.refresh_alerts, args=[self , employee_id]).start()
 
        print("*** Refresh Alerts" , datetime.now() , "***")

        try:
            Alerts.check_pop_ups(self, employee_id)
            
        except Exception as e:
            print(e)
            exit()

    
        
    def view_alert(self , name , window , employee_id_sended , date):
        
        LoadInfo.load_contacts(self , employee_id_sended , date , query = 'last' , state_sended = "Contact")
        
        tree = self.info.get_children()
        
        for item in tree:
            if self.info.item(item , 'values')[1]== name:
                                
                item = self.info.selection_set(item)
                
                GetInfo.load_client_info(self , name)

                window.destroy()
                
            
        
class Logs:

    def add_log(self , calendar_date , log_type , hour):
        
        client = self.company_id.get()#
        company_info = db.session.get(Client , client)#
        employee = self.active_employee_id.get()# 
        
        if log_type == 'next':
            
            try:                                                     
                Logs.log_type_next_pop(self , calendar_date , company_info , hour , 'next')
            
            except Exception as e:
                print(f"add_log (log_type_next): {e}")
                
        elif log_type == 'log':
            try:
                Logs.log_type_log(self , employee , company_info)
                 
            except Exception as e:
                print(f"add_log (log_type_log): {e}")           
                           
        else:
            try:
                Logs.log_type_next_pop(self , calendar_date , company_info , hour , 'pop')
              
            except Exception as e:
                print(f"add_log (log_type_pop): {e}") #add_log (log_type_pop): cannot unpack non-iterable bool object 
                     
        self.text_log.delete(1.0 , 'end')        
    
    
    def save_log(self , all_ok , new_comment , row_text_values_item):

        log = False
        
        Logs.confirm_unique_pop(new_comment)

        row = row_text_values_item
        
        if all_ok:  
       
            db.session.add(new_comment)
            db.session.commit()
            
            row_text_values_item[1][2] = MyCalendar.format_date_to_show(f'{str(datetime.now())[:16]}')
            self.info.item( row[2] , text = row[0] , values = row[1])
            
            GetInfo.load_comments(self , self.entry_nif.get())
            
            if 'log' in new_comment.contact_type:
                log = True
            
            Alerts.check_pop_ups(self , new_comment.contact_employee_id , log)

        db.session.close()
    
    
    def confirm_unique_pop(new_comment):
        contacts =  db.session.query(Contact).filter(and_(Contact.client_id == new_comment.client_id , Contact.contact_employee_id == new_comment.contact_employee_id , Contact.pop_up == True)).all()   
       
        try:
            for i , contact in enumerate(contacts):
                if contact.id_contact in alerts:
                    print(f"*** [{contact.id_contact}]({len(contacts)}/{i+1}) < Alerts Antes de remover : {alerts} ***")
                    
                    if contact.id_contact in alerts:
                        alerts.remove(contact.id_contact)
                        
                contact.pop_up = False
                
            print(f"********* Cleanning Old PopUps... > {alerts}************\n")
            
        except Exception as e:
            print(f'[confirm_unique_pop]: {e}')
        
        
    def row_to_change(self , client_name):
        
        text = ""
        values = ""
        tree = self.info.get_children()
        
        for item in tree: #self.info.item(item , 'values')[1]
            
            if self.info.item(item , 'values')[1] == client_name:

                values = list(self.info.item(item , 'values'))
                text = self.info.item(item , 'text')

                return [text , values , item]
    

    def log_type_log(self , employee , company_info):
        
        row_text_values_item = Logs.row_to_change(self , company_info.name)
        dot = ' ◉'
        
        try:
            last_comment = db.session.query(Contact).filter(and_(Contact.contact_employee_id == employee , Contact.client_id == company_info.id_client)).order_by(Contact.last_contact_date.desc()).all()
        
            new_comment = Contact(str(datetime.now())[:16] , last_comment[0].next_contact , self.text_log.get(1.0, "end") , company_info.id_client , employee , company_info.contact_person , f'{company_info.state}/log' , company_info.counter , False)
            
            all_ok = True
            
            for comment in last_comment:
                if comment.pop_up:
                    row_text_values_item[1][3] = MyCalendar.format_date_to_show(f'{comment.next_contact}') + dot
                    new_comment.pop_up = True
            
            Logs.save_log(self , all_ok , new_comment , row_text_values_item)
        
        except Exception as e:
            print("add_log" , e)
            
            if isinstance(e , IntegrityError):
                pass
            else:
                mb.showerror("Datos No Válidos (Log)" , f"\n\nDatos incompletos o erróneos.\n\n")
                
   
    def log_type_next_pop(self , calendar_date , company_info , hour , calendar): 
        
        try:
            
            hour = Logs.check_hour(hour)
            
            date = f'{calendar_date} {hour}'
            
            row_text_values_item = Logs.row_to_change(self , company_info.name)
            
            if calendar == 'pop':
                pop = True
                state = f'{company_info.state}/pop'
                
            else:
                pop = False
                state = f'{company_info.state}/next'
                
            new_comment = Contact(str(datetime.now())[:16] , date , self.text_log.get(1.0, "end") , company_info.id_client , self.active_employee_id.get() , company_info.contact_person , state , company_info.counter , pop)
           
            Logs.log_next_pop(self , calendar_date , hour, row_text_values_item , new_comment , calendar)
       
        except Exception as e:
            print("add_log" , e)
            
            mb.showerror("Datos No Válidos (Next Contact)" , f"\n\nDatos incompletos o erróneos.\n\n")
            
                                    
    def log_next_pop(self , calendar_date , hour, row_text_values_item , new_comment , calendar):
        
        dot = '◉'  # ASCII
        
        try:
            MyCalendar.calendar_toggle_frame(self , calendar) 
            
            if calendar == 'pop':
                pop = f' {dot}'
            else:
                pop = ""
            row_text_values_item[1][3] = MyCalendar.format_date_to_show(f'{calendar_date} {hour}') + pop
            row_text_values_item[1][2] = MyCalendar.format_date_to_show(f'{calendar_date} {hour}') 
            all_ok = True
            
            Logs.save_log(self , all_ok , new_comment , row_text_values_item) 
       
        except Exception as e:
            print(f"[log_next_pop]: {e}")   
            
            
    def check_hour(hour):

        test = hour.split(":")
        
        try:
            if (test[0].isdigit() and len(test[0]) == 2) and (test[1].isdigit() and len(test[1])): 
                if int(test[0]) <=24 and int(test[1]) < 60:
                    ok = hour

                return ok 
            
            else:
                raise Exception
        
        except Exception as e:
            mb.showerror('Hora' , f'\n\nEl formato de la hora no es correcto: {hour}\n\nFormato Correcto: 08:30 (HH:MM)')
                    
            
class Update:
    
    def update_info_entries(self, data , event):
        
        
        try:
            identificator = self.entry_nif.get()
            company = db.session.query(Client).filter(and_(Client.nif == identificator , Client.state == 'Contact')).first()
            new_data = data.get()
            
        except Exception as e:
            print(f'[] {e}')
            
        if data not in [self.entry_adress , self.entry_employees , self.entry_activity]:
            try:
            
                ""
        
            except Exception as e:
                print(f'[] {e}')
        
        elif data == self.entry_adress :
            try:
                print("ADRESS:" , data.get())
        
            except Exception as e:
                print(f'[] {e}')
        
        else:
            try:
                print("COMBO:" , data.get())
                
            except Exception as e:
                print(f'[] {e}')
                
    def test(self , data , event):
        
        fields =  {'name' : Update.pnt(data) }
        
        fields[data]
        #variable = self.entry_nif.get()
        #data = str(variable).split("_")[0]
        #client = db.session.query(Client).filter(Client.nif == variable).first()  
        
          
        #print(f"--------{data}----------")
        #print(client)
        
    def pnt(algo):
        print('*********algo*********')
        
class Tabs:
    
    def toggle_view(self , view):
        
        if view == 'CRM':
            self.sales_frame.grid_forget()
            self.frame_tree.grid(row = 1 , column = 0 , sticky = "nswe" ,  rowspan=3)
            self.frame_company.grid(row = 1 , column = 5 , sticky = "nswe" , columnspan = 4, padx = 5) 
            self.contact_frame.grid(row = 3 , column = 5 , columnspan=2 , rowspan = 2 ,  padx = 5 , sticky='nsew')
            self.company_contact_buttons.grid(row = 2 , column = 5 , columnspan = 2 ,sticky = 'nswe' , padx   = 5 )
        
        else:
            self.frame_tree.grid_forget()
            self.frame_company.grid_forget() 
            self.contact_frame.grid_forget()
            self.company_contact_buttons.grid_forget()
        