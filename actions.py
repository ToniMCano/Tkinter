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
from sqlalchemy.exc import IntegrityError
locale.setlocale(locale.LC_ALL, '')
   
nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']
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


employee = int()
 
class Actions:

    global employee
    
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
        log_button.grid(row = 1 , column = 0 , padx = 5 , pady = 5)
        
        Actions.center_window(Actions , login)
        
     
     
    def load_contacts(self , employee):
        #self.info.insert("" , 0 , text = 'client[0]' , values =['client[1]' , 'client[2]' , 'client[3]' , 'client[4]' , 'client[5]' , "Cantidad" , "Porcentaje"])
        #contacts = db.session.query(Client).filter(and_(Client.state == "Lead" , Client.employee_id == employee )).all()
        
        #for client in contacts:
        self.info.insert("" , 0 , text = 'client[0]' , values =['client[1]' , 'client[2]' , 'client[3]' , 'client[4]' , 'client[5]' , "Cantidad" , "Porcentaje"])
               
               
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
        
    
    def create_contact(self):
        
        frame = tk.Toplevel()
        frame.title("New Contact")
        frame.geometry("600x180")
        #frame.minsize(400, 400)    # Establecer un tamaño mínimo de 300x200
        frame.grid_columnconfigure(0 , weight = 1)
        Actions.center_window(Actions , frame)
        
        
        frame_info = ttk.Frame(frame)
        frame_info.grid(row = 0 , column = 0, padx = 5 , pady = 10 , sticky = W+E)
        frame_info.grid_columnconfigure(0 , weight = 1)
        
        frame_contact_person = ttk.Labelframe(frame_info , text = "Contact Person")
        frame_contact_person.grid(row = 0 , column = 0)
        
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
        
        save_button = ttk.Button(frame_info, text = "Guardar" , command=Actions.olvidar)
        save_button.grid(row = 6 , column = 0 , columnspan = 2 , padx = 200 , pady = 5 , sticky = W+E)
        
        
    def new_company(data = {"Nombre Empresa: " : '' , "N.I.F.: " : '' , "NACE: " : '' , "Empleados: " : '', "Dirección " : f"{''} - {''} - {''}"  , "Web: " : '', "Mail Empresa: " : '', "Teléfono Empresa: " : '', "Teléfono2 Empresa: " : '', "Nombre Contacto: " : '', "Apellidos Contacto: " : '', "Cargo: " : '', "Mail Contacto: " :'', "Teléfono Contacto: " : '', "Móvil Contacto: " : ''}):
    
   
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
        
        entry_company_name = ttk.Entry(company_frame)
        entry_company_name.grid(row =0 , column = 1 , columnspan = 5 , padx = 5 , pady = 5 , sticky = W+E)
        
        company_nif= ttk.Label(company_frame , text ="N.I.F: ")
        company_nif.grid(row =0 , column = 6 , padx = 5 , pady = 5)
        
        entry_company_nif = ttk.Entry(company_frame)
        entry_company_nif.grid(row =0 , column = 7 , padx = 5 , pady = 5)
        
        company_activity = ttk.Label(company_frame , text ="Actividad: ")
        company_activity.grid(row =1 , column = 0 , columnspan= 7 , padx = 5 , pady = 5 , sticky = "w")
        
        nace_list_combo = ttk.Combobox(company_frame, state = 'readonly' , values = Actions.nace_list())
        nace_list_combo.grid(row =2 , column = 0 ,  columnspan= 7 , padx = 5 , pady = 5 , sticky = W+E)
        nace_list_combo.current(newindex = 0)
        #nace_list_combo.bind("<<ComboboxSelected>>" , self.test)
        
        number_of_employees = ttk.Label(company_frame, text = "Empleados: ")
        number_of_employees.grid(row = 1 , column = 7 , padx = 5 , pady = 5 , sticky = "w")
        
        number_of_employees_entry = ttk.Combobox(company_frame, state = 'readonly' , values =  [" < 10" , "10 - 50" , "50 - 250" , " > 250"])
        number_of_employees_entry.grid(row =2 , column = 7  , padx = 5 , pady = 5 , sticky = W+E)
        number_of_employees_entry.current(newindex = 0)
        #number_of_employees_entry.bind("<<ComboboxSelected>>" , self.test) 
        
        
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
        frame_contact_person.grid(row = 4 , column = 0)
        
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
        
        save_company_button = ttk.Button(add_company_frame , text = "Add" , command = lambda: Actions.test_add_company(add_company_frame , {"Nombre Empresa: " : entry_company_name.get(), "N.I.F.: " : entry_company_nif.get(), "NACE: " : nace_list_combo.get(), "Empleados: " : number_of_employees_entry.get(), "Dirección " : f"{company_street.get()} - {company_street_number.get() } - {company_street_floor.get()}"  , "Web: " : entry_company_web.get(), "Mail Empresa: " : entry_company_mail.get(), "Teléfono Empresa: " : entry_company_phone.get(), "Teléfono2 Empresa: " : entry_company_phone2.get(), "Nombre Contacto: " : entry_name.get(), "Apellidos Contacto: " : entry_surname.get(), "Cargo: " : entry_job_title.get(), "Mail Contacto: " : entry_mail.get(), "Teléfono Contacto: " : entry_phone.get(), "Móvil Contacto: " : entry_mobile.get()}))
        save_company_button.grid(row = 5 , column = 0 , pady = 5 )

        Actions.center_window(Actions , add_company_frame)
        
        entry_company_name.insert(0 , data["Nombre Empresa: "])
        entry_company_nif.insert(0 , data["N.I.F.: "])
        company_street.insert(0 , data["Dirección "].split("-")[0])
        company_street_number.insert(0 , data["Dirección "].split("-")[1])      
        company_street_floor.insert(0 , data["Dirección "].split("-")[2])
        entry_company_web.insert(0 , data["Web: "])
        entry_company_mail.insert(0 , data["Mail Empresa: "])      
        entry_company_phone.insert(0 , data["Teléfono Empresa: "])
        entry_company_phone2.insert(0 , data["Teléfono2 Empresa: "])
        entry_name.insert(0 , data["Nombre Contacto: "])
        entry_surname.insert(0 , data["Apellidos Contacto: "])
        entry_mail.insert(0 , data["Mail Contacto: "])
        entry_phone.insert(0 , data["Teléfono Contacto: "])
        entry_job_title.insert(0 , data["Cargo: "])
        entry_mobile.insert(0 , data["Móvil Contacto: "])
        
            
    def test_add_company(add_company_frame , data):

        if data["Nombre Contacto: "] != "" and data['Apellidos Contacto: '] != "" and data['Teléfono Contacto: '] != "" and data['Mail Contacto: '] and data['Nombre Empresa: '] != ""  and data['N.I.F.: '] != ""  and data['Mail Empresa: '] != ""  and data['Teléfono Empresa: '] != "":
            
            if data['N.I.F.: '][0].lower() in nif_check and len(data['N.I.F.: ']) == 9:
                
                if data["Web: "].split(".")[0] == "www" and len(data["Web: "].split(".")[-1]) >= 2:
                       
                    if ("@" in data['Mail Empresa: '] and data['Mail Empresa: '].split("@")[0] != "" and len(data['Mail Empresa: '].split(".")[-1])) >= 2 and ("@" in data['Mail Contacto: '] and data['Mail Contacto: '].split("@")[0] != "" and len(data['Mail Contacto: '].split(".")[-1]) >= 2):
                        
                        if (str(data['Teléfono Contacto: ']).isdigit() and len(data['Teléfono Contacto: ']) == 9)  and (str(data["Teléfono Empresa: "]).isdigit() and len(data["Teléfono Empresa: "]) == 9):
                
                        
                            Actions.add_company(data , add_company_frame)
                        
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
            Actions.new_company(data)
      
      
    def add_company(data , add_company_frame):
        
        try:
            contact_person = ContactPerson(data["Nombre Contacto: "] , data["Apellidos Contacto: "] , data["Cargo: "] , data["Teléfono Contacto: "] , data["Móvil Contacto: "] , data["Mail Contacto: "] , "Id de la Empresa")
            
            db.session.add(contact_person)
            db.session.commit()
            
            vcontact_person = db.session.query(ContactPerson).order_by(ContactPerson.id_person.desc()).first() # Se asigna el último empleado introducido en la DB, es decir el que se crea a la vez que la empresa.
            
            company = Client(data["Nombre Empresa: "] , data["N.I.F.: "] , data["Dirección "] , data["Web: "] , data["Mail Empresa: "] , data["Teléfono Empresa: "] , data["Teléfono2 Empresa: "] , data["NACE: "] , vcontact_person.id_person , employee , "Pool", data["Empleados: "])
            
            db.session.add(company)
            db.session.commit()
            
            vcontact_person.client_id = db.session.query(Client).order_by(Client.id_client.desc()).first() # Asignamos la persona de contacto creada.
            
            db.session.close()
            
            add_company_frame.destroy() 
             
            Actions.show_new_company(data['Nombre Empresa: '] , data['Nombre Contacto: '] , data['Apellidos Contacto: '] , data['Cargo: '])

        except Exception as e:
            
            if isinstance(e, IntegrityError):
                print(e)
                db.session.close()
                mb.showerror("Error de Integridad" , f"La empresa ya existe, el Nombre o el N.I.F. ya existen en la Base de Datos.")
                
            else:
                print(e)
                mb.showerror("Ha ocurrido un error inesperado" , f"{e}")
            add_company_frame.destroy()    
            Actions.new_company(data)
 
            
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
        
        Actions.center_window(Actions , show)
        
    
    def show_company(company_id):
        pass


    def calendar(frame , place , date = "" ):
        
        header_calendar = StringVar(value = "View")
        label_calendar = tk.Label(frame , textvariable = header_calendar , bg = "black" , fg = "white")
        label_calendar.pack(fill = "x" , expand = True)
        frame.calendar = Calendar(frame , selectedmode = "day" , date_pattern = "dd-mm-yyyy")
        frame.calendar.pack()
        
        if place == "general":
            frame.calendar_date = frame.calendar.bind("<<CalendarSelected>>", lambda e: Actions.general_calendar_date(frame , place , date , e))
       
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
            send = ttk.Button(frame , text = "Save" , command = lambda: Actions.tst(frame , place , hour = hour.get()) )
            send.pack(pady = 5)

    def toggle_frame_visibility(frame , place):
        
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


    def general_calendar_date(self , place , date , event):
        
        try:
            fecha_seleccionada = self.calendar.get_date() # 10-04-2024 Comprobar si se puede ordenar así en la DB.
            month = int(fecha_seleccionada[3:5])
            year = int(fecha_seleccionada[6:])
            
            if int(fecha_seleccionada[0]) == 0:
                day = int(fecha_seleccionada[1])
            
            else:
                day = int(fecha_seleccionada[0:2])
            
            date.set(datetime(year,month,day).strftime("%d %B")) 
            Actions.toggle_frame_visibility(self , place)
            
        except Exception as e:
            mb.showwarning("Error" , f"Ha habido un problema con las fechas {e}")
                     
                    
    def olvidar():
       #app.grid_forget()
       vcontact_person = db.session.query(ContactPerson).order_by(ContactPerson.id_person.desc()).first()
       print(vcontact_person.id_person , employee)
       
    def tst(self , place , hour):
        print(f"Date From: {place} - {self.calendar.get_date()} - {hour}")
        Actions.toggle_frame_visibility(self , place)
