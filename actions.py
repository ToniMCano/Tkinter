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
from datetime import datetime
#import locale
from tkinter import messagebox as mb
import os
from sqlalchemy.exc import IntegrityError
import customtkinter

#locale.setlocale(locale.LC_ALL, '')   Si uso Locale customtkinter da problemas.  ----- "TO-DO"
 



 
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
        
        
    def new_company(data = {"Nombre Empresa: " : '' , "N.I.F.: " : '' , "NACE: " : '' , "Empleados: " : '', "Dirección: " : ""  , "Web: " : '', "Mail Empresa: " : '', "Teléfono Empresa: " : '', "Teléfono2 Empresa: " : '', "Nombre Contacto: " : '', "Apellidos Contacto: " : '', "Cargo: " : '', "Mail Contacto: " :'', "Teléfono Contacto: " : '', "Móvil Contacto: " : ''}):
    
        #load_image= Image.open("recursos/upload.png")
        #load_image.resize((6,6))
        #load_image_icon = ImageTk.PhotoImage(load_image)

        add_company_frame = Toplevel()
        add_company_frame.title("Add Company")
        add_company_frame.grid_columnconfigure(0 , weight = 1)
        
        files_frame = tk.Frame(add_company_frame)
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
        
        save_company_button = ttk.Button(add_company_frame , text = "Add" , command = lambda: AddInfo.test_add_company(add_company_frame , {"Nombre Empresa: " : entry_company_name.get(), "N.I.F.: " : entry_company_nif.get(), "NACE: " : nace_list_combo.get(), "Empleados: " : number_of_employees_entry.get(), "Dirección: " : f"{company_street.get()}, {company_street_number.get() } {company_street_floor.get()} {company_city_entry.get()}, ({company_province_entry.get()}) {company_postal_code_entry.get()}"  , "Web: " : entry_company_web.get(), "Mail Empresa: " : entry_company_mail.get(), "Teléfono Empresa: " : entry_company_phone.get(), "Teléfono2 Empresa: " : entry_company_phone2.get(), "Nombre Contacto: " : entry_name.get(), "Apellidos Contacto: " : entry_surname.get(), "Cargo: " : entry_job_title.get(), "Mail Contacto: " : entry_mail.get(), "Teléfono Contacto: " : entry_phone.get(), "Móvil Contacto: " : entry_mobile.get()}))
        save_company_button.grid(row = 5 , column = 0 , pady = 10)
        
        Pops.center_window(Pops , add_company_frame)
    
       
    def show_new_company(company_name , contact_name , contact_surname , contact_job):
        
        show = Toplevel()
        show.title("Se ha creado una nueva Empresa") 
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
    
    def calendar_toggle_frame(frame , place):
        
        if frame.winfo_ismapped(): # Comprueba si self.frame_container_calendar es visible, si es visible lo oculta con self.frame_container_calendar.grid_forget()
            frame.place_forget()

        else:
            if place == "general":
                frame.place(x = 320, y = 50) 
                frame.lift()  # Elevar el Frame al frente 
                
            elif place == 'next':
                frame.place(x = 0, y = 242) 
                frame.lift() 
            
            elif place == "pop":
                frame.place(x = 0, y = 272) 
                frame.lift() 
                
    
    def calendar(frame , place , date = "" ):  
        
        hours_list = [
            "8:00", "8:15", "8:30", "8:45", "9:00",
            "9:00", "9:15", "9:30", "9:45", "10:00",
            "10:00", "10:15", "10:30", "10:45", "11:00",
            "11:00", "11:15", "11:30", "11:45", "12:00",
            "12:00", "12:15", "12:30", "12:45", "13:00",
            "13:00", "13:15", "13:30", "13:45", "14:00",
            "14:00", "14:15", "14:30", "14:45", "15:00",
            "15:00", "15:15", "15:30", "15:45", "16:00",
            "16:00", "16:15", "16:30", "16:45", "17:00",
            "17:00", "17:15", "17:30", "17:45", "18:00",
            "18:00", "18:15", "18:30", "18:45", "19:00",
            "19:00", "19:15", "19:30", "19:45", "20:00",
            "20:00", "20:15", "20:30", "20:45", "20:00",
              ]
        
        header_calendar = StringVar(value = "View")
        
        label_calendar = tk.Label(frame , textvariable = header_calendar , bg = "black" , fg = "white")
        
        label_calendar.pack(fill = "x" , expand = True)
        
        frame.calendar = Calendar(frame , selectedmode = "day" , date_pattern = "yyyy-mm-dd") # Para poder ordenarlo en la DB "YYYY-MM-DD"
        frame.calendar.pack()
        
        if place == "general":
            
            frame.calendar_date = frame.calendar.bind("<<CalendarSelected>>", lambda e: MyCalendar.general_calendar_date(frame , place , date , e))
       
        elif place != "general":
            
            if place == "next":
                header_calendar.set("Next Contact")
                
            else:
                header_calendar.set("Pop Up")
                
            hour = ttk.Combobox(frame , justify = "left" , values = hours_list , width = 10)
            hour.current(newindex = 0)
            hour.config(justify=CENTER)
            hour.pack(fill = "x" , expand = True , anchor = "center")
            #frame.calendar_date = frame.calendar.bind("<<CalendarSelected>>")
            send = ttk.Button(frame , text = "Save" , command = lambda: MyCalendar.format_date(frame , place , hour = hour.get()) )
            send.pack(pady = 5)
            

    def general_calendar_date(self , place , date , event):
        
        try:
            fecha_seleccionada = self.calendar.get_date() ## Para poder ordenarlo en la DB "YYYY-MM-DD" 
            
            month = int(fecha_seleccionada[5:7])
            year = int(fecha_seleccionada[0:4])
            
            if int(fecha_seleccionada[-2]) == 0:
                day = int(fecha_seleccionada[-1])
                
            else:
                day = int(fecha_seleccionada[-2:])
            
            date.set(datetime(year,month,day).strftime("%d %B")) 
            
            MyCalendar.calendar_toggle_frame(self , place)
            
        except Exception as e:
            print(e)
            mb.showwarning("Error" , f"Ha habido un problema con las fechas {e}") 
                   
    
    def format_date(self , place , hour): #  (YYYY-MM-DD HH:MM:SS)  Para poder ordenarlo en la DB 
        print(f"Date From: {place} - {self.calendar.get_date()} {hour}") 
        MyCalendar.calendar_toggle_frame(self , place)

    

class LoadInfo():

    
    def check_employee(root , employee_password , alias , window):
        
        employees =  db.session.query(Employee).all()
        exists = False
        
        for employee in employees:
            if employee.employee_alias == alias and employee.password == str(employee_password):
                
                exists = True
                window.destroy()
                
                LoadInfo.load_contacts(root , employee.id_employee)
                print(f" Empleado {employee.id_employee}")
                
                alias = GetInfo.employees_list().index(alias)
                    
                root.employee.current(newindex = alias)
                
               
        if not exists:
            mb.showwarning("Login Error" , "El usuario o la contraseña no son correctos")
            window.lift()


    def load_contacts(self , employee_id_sended ): # last_gestion =db.session.query(func.max(Contact.contact_counter )).scalar() Hay que tener en cuenta el counter para que no muestre contactos de una gestión anterior
        
        #state == "Contact")).order_by(Contact.last_contact_date.desc()).group_by(Contact.client_id).all() # Cada objeto en la lista será el primer contacto dentro de su respectivo grupo de cliente
        contacts = 0
        clients = db.session.query(Client).filter(and_(Client.state == "Contact" , Client.employee_id == employee_id_sended)).all()
        # Cada objeto en la lista será el primer contacto dentro de su respectivo grupo de cliente

        for client in clients:
            contact = db.session.query(Contact).filter(Contact.contact_person_id == client.contact_person).order_by(Contact.last_contact_date.desc()).group_by(Contact.contact_person_id).first()
            
            self.info.insert("" , 0 , text = client.state , values = (LoadInfo.get_days(client) , client.name, contact.last_contact_date   , contact.next_contact , client.adress[-5:]))
            contacts += 1
        self.contacts.set(f"Contactos: {contacts} ID: Empleado: {employee_id_sended}")
    
    
    def get_days(client):
        
        today = datetime.now()
        
        try:
            date = client.start_contact_date
            
            days = str(today - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).split(" ")[0] 
        
        except Exception as e:
            print(e) 
            days = 0
            
        return days
    
    
    def get_client_name(tree , event):

        row = tree.info.focus()
        item = tree.info.item(row)
        client_name = item['values'][1]
        
        GetInfo.load_client_info(tree , client_name)
        
        
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
        
        
    
class GetInfo():
    
    def load_comments(self , nif):
        
        frame_log = customtkinter.CTkScrollableFrame(self.frame_tree, fg_color = "lightgrey")
        frame_log.grid(row = 3 , pady = 5 , padx = 3 , sticky = 'nsew')
        
        try:
            for log in frame_log.winfo_children():
                log.destroy()
            
        except UnboundLocalError:
            print("NOT destroyed")

        client = db.session.query(Client).filter(Client.nif == nif).first()
        comments = db.session.query(Contact).filter(Contact.client_id == client.id_client).order_by(Contact.last_contact_date.desc()).all()
        comments_counter = 0
        
        for i, comment in enumerate(comments):
            log_frame = f"log_{str(i)}"
            label_info = f"label_{str(i)}"
            label_content = f"content_{str(i)}"
            
            log_frame = tk.Frame(frame_log , bg = "white" , height = 10 , bd = 1 , relief = "solid")
            log_frame.pack(fill = "x" , expand = True , pady = 2)
            
            label_info = tk.Label(log_frame , text = f"{GetInfo.load_info_log(comment.client_id , comment.last_contact_date)}" , bg = "black" , fg = "white")
            label_info.pack(fill = "x" , expand = True)
            
            label_content = tk.Label(log_frame , text = f"{comment.log}" , bg = "White")
            label_content.pack(fill = "x" , expand = True)
            
            comments_counter += 1
        print(comments_counter)
        
        
    def load_info_log(client_by_id , last_contact):
        
        try:
            client = db.session.get(Client , client_by_id)
            contact_person = db.session.get(ContactPerson , client.contact_person)
            employee = db.session.get(Employee , client.employee_id)
            return f"{datetime.strptime(last_contact, '%Y-%m-%d %H:%M').strftime('%d %B %Y %H:%M').title()} {contact_person.contact_name} {contact_person.contact_surname} [{employee.employee_alias}]"
            
        except Exception as e:
            print(e)


    def load_client_info(tree , client_name):
        
        client = db.session.query(Client).filter(Client.name == client_name).first()
        contact_person = db.session.get(ContactPerson , client.contact_person)
        
        tree.entry_company_name.delete(0 , END)
        tree.entry_company_name.insert(0 , client.name) # Es lo mismo que placeholder
        
        tree.entry_nif.delete(0 , END)
        tree.entry_nif.insert(0, client.nif)
        
        tree.entry_adress.delete(0 , END)
        tree.entry_adress.insert(0 , client.adress)
        
        tree.entry_activity.current(newindex = Pops.current_combo(client.activity , LoadInfo.nace_list()))
        
        tree.entry_employees.current(newindex = Pops.current_combo(client.number_of_employees , "employees"))
        
        tree.entry_web.delete(0 , END)
        tree.entry_web.insert(0, client.web)
        
        tree.entry_mail_empresa.delete(0 , END)
        tree.entry_mail_empresa.insert(0 , client.mail)
        
        tree.entry_company_phone.delete(0 , END)
        tree.entry_company_phone.insert(0, client.phone)
        
        tree.entry_company_phone2.delete(0 , END)
        tree.entry_company_phone2.insert(0, str(client.phone2))
        
        tree.entry_contact_name.delete(0 , END)
        tree.entry_contact_name.insert(0, contact_person.contact_name)
        
        tree.entry_contact_surname.delete(0 , END)
        tree.entry_contact_surname.insert(0,contact_person.contact_surname)
        
        tree.entry_job_title.delete(0 , END)
        tree.entry_job_title.insert(0, contact_person.contact_job_title)
        
        tree.entry_contact_mail.delete(0 , END)
        tree.entry_contact_mail.insert(0,contact_person.contact_mail)
        
        tree.entry_contact_phone.delete(0 , END)
        tree.entry_contact_phone.insert(0, contact_person.contact_phone)
        
        tree.entry_mobile.delete(0 , END)
        tree.entry_mobile.insert(0 , contact_person.contact_mobile)
        
        GetInfo.load_comments(tree , client.nif)
        
        #tree.notes.delete(0 , END)
        #tree.notes.insert(0 , "686289365")
        
    def employees_list():
        
        employees_list = []
        employees = db.session.query(Employee).all()
        
        for alias in employees:
            employees_list.append(alias.employee_alias)
        
        return employees_list
        
        
class AddInfo():
    
    def test_add_company(add_company_frame , data):
        
        nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']

        if data["Nombre Contacto: "] != "" and data['Apellidos Contacto: '] != "" and data['Teléfono Contacto: '] != "" and data['Mail Contacto: '] and data['Nombre Empresa: '] != ""  and data['N.I.F.: '] != ""  and data['Mail Empresa: '] != ""  and data['Teléfono Empresa: '] != "":
            
            if data['N.I.F.: '][0].lower() in nif_check and len(data['N.I.F.: ']) == 9:
                
                if data["Web: "].split(".")[0] == "www" and len(data["Web: "].split(".")[-1]) >= 2:
                       
                    if ("@" in data['Mail Empresa: '] and data['Mail Empresa: '].split("@")[0] != "" and len(data['Mail Empresa: '].split(".")[-1])) >= 2 and ("@" in data['Mail Contacto: '] and data['Mail Contacto: '].split("@")[0] != "" and len(data['Mail Contacto: '].split(".")[-1]) >= 2):
                        
                        if (str(data['Teléfono Contacto: ']).isdigit() and len(data['Teléfono Contacto: ']) == 9)  and (str(data["Teléfono Empresa: "]).isdigit() and len(data["Teléfono Empresa: "]) == 9):
                
                        
                            AddInfo.add_company(data , add_company_frame)
                        
                        else:
                            mb.showwarning("Teléfono" , f"El formato del Teléfono no es correcto, comprueba Teléfono Empras y Teléfono Contacto.")
                            add_company_frame.lift()
                    
                    else:
                        mb.showwarning("Mail" , f"El formato del Mail no es correcto, comprueba los Mails.")
                        add_company_frame.lift()
                
                else:
                    mb.showwarning("Web" , f'El formato de la Web no es correcto [{data["Web: "]}]')
                    add_company_frame.lift()
                    
            else:
                mb.showwarning("N.I.F." , f"El formato del N.I.F. no es correcto [{data['N.I.F.: ']}]")
                add_company_frame.lift()                    
               
        else:
            print("else")
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
      
    
    def add_company(data , add_company_frame , employee_adder = 0 , company_to_add = 0):
        
        
        try:
            
            vcontact_person = AddInfo.add_contact(data , employee_adder)
            
            company = Client(data["Nombre Empresa: "] , data["N.I.F.: "] , data["Dirección: "] , data["Web: "] , data["Mail Empresa: "] , data["Teléfono Empresa: "] , data["Teléfono2 Empresa: "] , data["NACE: "] , vcontact_person.id_person , active_employee , "Pool", data["Empleados: "])
            vcontact_person.client_id = vcontact_person.id_person
            
            db.session.add(company)
            db.session.commit()
            
            
            vcontact_person.client_id = db.session.query(Client).order_by(Client.id_client.desc()).first() # Asignamos la persona de contacto creada.
            
            db.session.close()
            
            add_company_frame.destroy() 
             
            Pops.show_new_company(data['Nombre Empresa: '] , data['Nombre Contacto: '] , data['Apellidos Contacto: '] , data['Cargo: '])

        except Exception as e:
            
            if isinstance(e, IntegrityError):
                print(e)
                db.session.close()
                mb.showerror("Error de Integridad" , f"La empresa ya existe, el Nombre o el N.I.F. ya existen en la Base de Datos.")
                
            else:
                print(e)
                mb.showerror("Ha ocurrido un error inesperado" , f"{e}")
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
            
     
    def add_contact(data , employee_adder):
        
        try:                                                                                                                                                                                                # TO-DO sustituir por la empresa adminstradora
            contact_person = ContactPerson(data["Nombre Contacto: "] , data["Apellidos Contacto: "] , data["Cargo: "] , data["Teléfono Contacto: "] , data["Móvil Contacto: "] , data["Mail Contacto: "] , "Id de la Empresa" , employee_adder)
                
            db.session.add(contact_person)
            db.session.commit()
            
            vcontact_person = db.session.query(ContactPerson).order_by(ContactPerson.id_person.desc()).first() # Se asigna el último empleado introducido en la DB, es decir el que se crea a la vez que la empresa.
            
            return vcontact_person
        
        except Exception as e:
            mb.showerror("Error al añadir Persona de Contacto" , f"{e}")
            
