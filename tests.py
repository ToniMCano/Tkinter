
import openpyxl
from openpyxl import Workbook
import random
import sqlalchemy
from sqlalchemy import and_ , or_
import db
from models import Client , ContactPerson , Employee , Contact
from datetime import datetime , timedelta
import os
from tkinter import *
import customtkinter
from actions import GetInfo,LoadInfo
import pandas as pd



nif = ['0','1','2','3','4','5','6','7','8','9']

def datos_muestra(): # EXCEL CON MUESTRA DE DATOS PARA PRUEBAS

    nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']

    excel = openpyxl.load_workbook("recursos/NACE.xlsx")

    wb = Workbook()   # Creamos un WB de 0

    active_sheet = wb.active  # Seleccionamos la hoja activa (la primera)

    data = []
    row = []
    nace = []
    
    employees =  [" < 10" , "10 - 50" , "50 - 250" , " > 250"]
    alias = 1
    employee = 1
    starts = start_date()



    for x in excel["Hoja 1"]:
        if len(x[0].value.split(" - ")[0]) >= 2:
            nace.append(x[0].value)
            
    for employee_id in range(3):
        for data_row in range(50):
            start = start_date()
            row.append("Company".lower() + str(alias))
            row.append(random.choice(nif_check).capitalize() + "".join(random.choices(nif , k=8)))
            row.append(f"adress{str(alias)},{str(alias)} {str(random.randint(1,20))} - {random.choice(nif_check).capitalize()}  City{str(alias)}, (Province{str(alias)})")
            row.append(''.join(random.choices(nif , k = 5)))
            row.append(f"www.web{str(alias)}.com")  
            row.append(f"{row[0]}@{row[4][4:]}")
            row.append(int("9" + ''.join(random.choices(nif , k = 8)) )) 
            row.append("")
            row.append(random.choice(nace))
            row.append(alias)
            row.append(employee)
            row.append("Contact")
            row.append(random.choice(employees))
            row.append(starts[alias - 1])
            row.append(random.randint(0,1))
            row.append(0) # created_by
            
            if row[-2] == 0:
                row[-5] = "Pool"

            data.append(row)
            
            row = []
            
            alias += 1
            
        employee += 1
            
    for x in data: 
        active_sheet.append(x) # Añadimos las filas
        
    wb.save("data2.xlsx")    
    
    
def start_date():
    
    day =1 
    month = 1
    new_date = datetime(2024,month,day,8,0,0)
    dated = []

    for x in range(150):
        try:
            dated.append(str(new_date))
            new_date = new_date + timedelta(hours = random.randint(1,12))
        
        except ValueError:
            day = 1
            month +=1
            
    return dated


def contacts():   # UN CONTACTO PARA CADA EMPRESA
    
    registro = []
    
    clients = db.session.query(Client).all()
    
    for i , person in enumerate(clients):
                                                                                                                                                                                                      # added_by
        contact = ContactPerson(f"Name{str(person.id_client)}" , f"Surname{str(person.id_client)}" , f"General Manager" , int(f"9{''.join(random.choices(nif , k = 8))}") , "" , f"contact{str(person.id_client)}@mail.com" , person.id_client , "Notes" , 0 )        
        try:
            db.session.add(contact)
            db.session.commit()
            print("ok")
            
        except Exception as e:
            print(e)
        
    db.session.close()
            
 

def empleados():
     
    for i , x in enumerate(range(3)):
        
        employee = Employee(f"EA{str(i+1)}", f"Name{str(i+1)}" , f"Surname{str(i+1)}" , f"ea{str(i+1)}@company.com", int(f"9652293{str(i+1)}") ,"Comercial" , 1234 , 1)
        db.session.add(employee)
        db.session.commit()
    db.session.close()
    
#last_contact_date , last_contact_hour , log , client_id , contact_counter , contact_employee_id , contact_person_id , company_state = 'pool' , contact_state = None):

 
def contact(): 
    
    clients = db.session.query(Client).all()
    last , next = date()
    
    for company in clients:
            
        if company.state == "Contact":
            print(company.state , company.id_client)
            for i, contact in enumerate(range(25)):
                print(contact)
                contact_random = Contact(company_state = company.state, last_contact_date = f"{last[i]} {str(random.randint(8,19))}:00" , next_contact = f"{next[i]} {str(random.randint(8,19))}:00"  , log =  "No localizado, estará a parir de las 16:00" ,client_id =  company.id_client , contact_counter = 1 , contact_employee_id = company.employee_id , contact_person_id =  company.contact_person)
            
                db.session.add(contact_random)
                db.session.commit()
    
    db.session.close()


def date():
    
    last = []
    next = []
    
    for x in range(25):
        
        day = str(random.randint(1 , 15))
        month = str(random.randint(1 , 4))
        
        if len(day) < 2:
            day =f"0{day}"
            
        month =f"0{month}"
        
        last.append(f"2024-{month}-{day}")
        
        day = str(random.randint(15 , 30))
        
        next.append(f"2024-{month}-{day}")
        
        
    return last , next
     
        
def load_contacts():
    contacts = db.session.query(Contact).filter(and_(Contact.company_state == "Contact" , Contact.contact_employee_id == 1 )).all()
    
    for client in contacts:
        company_name = db.session.query(Client).filter(Client.contact_person == client.contact_person_id).first()
        print(company_name.name)
               

def test3():
    clientes = db.session.query(Client)
    #contactss = db.session.query(Contact).filter(Contact.contact_person_id == ).all()
    
    for x in clientes:
        contactss = db.session.query(Contact).filter(Contact.contact_person_id == x.id_client ).all()
        for y in contactss:
            y.contact_counter = x.counter
            

def load_comments():
        comments = db.session.query(Contact).filter(Contact.client_id == 1).order_by(Contact.last_contact_date.desc())
        comments_counter = 0
        
        for comment in comments:
            print(comment)
            comments_counter += 1
        print (comments_counter)
        
        
def info_log():
        contact_date = f"{datetime.now().strftime('%d %B %Y %H:%M')}"
        return f"{contact_date} Pepito Grillo [EA1]"


def index():  
    alias = 'EA1'
    index = GetInfo.employees_list().index(alias)
                        
    print (index , alias)
    
    
def muestra(): 

    excel = openpyxl.load_workbook("recursos/NACE.xlsx")
    nace = []

    for x in excel["Hoja 1"]:
        if len(x[0].value.split("-")[0].strip(" ")) > 1:
            nace.append(x[0].value)
    print(nace[0])

#datos_muestra()
#empleados()
#contact()
#contacts()




def load_contacts(): # last_gestion =db.session.query(func.max(Contact.contact_counter )).scalar() Hay que tener en cuenta el counter para que no muestre contactos de una gestión anterior
    
    bell = '◉'  # ASCII
    dot = '🔔'
    alert = ""
    dataframe = {"estado" : [] , "días" : [] , "nombre" : [] , "último" : [] , "próximo" : [] , "cp" : []}
    
    '''if str(employee_id_sended).isdigit():
        pass
    
    else:
        employee_id_sended = db.session.query(Employee).filter(Employee.employee_alias == employee_id_sended).first()
        employee_id_sended = employee_id_sended.id_employee

    if not date:
        date = str(datetime.now()) + " 23:59"    

    try:
        clean = self.info.get_children()
        
        for x in clean: 
            self.info.delete(x)
                    
    except Exception as e:
        print(e)
    
    contacts = 0
    bgcolor = 0
    clients = db.session.query(Client).filter(and_(Client.state == "Contact" , Client.employee_id == int(employee_id_sended))).all() # Cada objeto en la lista será el primer contacto dentro de su respectivo grupo de cliente
    self.info.tag_configure("odd", background="lightgray" )
    self.info.tag_configure("even", background="white")
    self.info.tag_configure("font_red", foreground="red")
    scrollbar = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.info.yview)
    scrollbar.grid(row = 0, column = 1 , sticky = "ns")
    self.info.configure(yscroll=scrollbar.set)
    '''
    clients = db.session.query(Client).filter(and_(Client.state == "Contact" , Client.employee_id == 1)).all() # Cada objeto en la lista será el primer contacto dentro de su respectivo grupo de cliente
    
    #self.treeview.insert("", "end", text="Fila 3", tags=("odd",))
    for i , client in enumerate(clients):
        
        contact = db.session.query(Contact).filter(Contact.client_id == client.id_client).order_by(Contact.next_contact.desc()).first()
        
        dataframe["estado"].append(client.state)
        dataframe["días"].append(LoadInfo.get_days(client))
        dataframe["nombre"].append(client.name)
        dataframe["último"].append(contact.last_contact_date)
        dataframe["próximo"].append(f'{contact.next_contact}')
        dataframe["cp"].append(client.postal_code)
        
        insert = pd.DataFrame(dataframe)
        
    ''' 
    for i , client in enumerate(clients):

        
        if contact.next_contact[:10] <= str(date)[:10]:               
            
            if int(LoadInfo.get_days(client)) > 110:
                font = "font_red"
                
            else:
                font = ""
            
            if bgcolor % 2 == 0:
                color= "odd"
            
            else:
                color= "even"
                
                
            self.info.insert("" , 0 , text = client.state , values = (LoadInfo.get_days(client) , client.name, contact.last_contact_date   , f'{contact.next_contact}', client.postal_code) , tags=(color, font) )
            contacts += 1
            bgcolor += 1
            
    self.contacts.set(f"Contactos: {contacts}")'''
    ordenado = insert.sort_values(by = ["cp"])
    print(ordenado)
    print(ordenado.iat[0,-1])
    print(len(ordenado))


    
def optimizar():
    replace_date = db.session.query(Contact).all()

    for new in replace_date:
        if len(new.next_contact) == 15:
            print(new.next_contact)
            new.next_contact = new.next_contact.replace(" " , " 0")
            print(new.next_contact)
            
        if len(new.last_contact_date) == 15:
            print(new.last_contact_date)
            new.last_contact_date = new.last_contact_date.replace(" " , " 0")
            print(new.last_contact_date)
    db.session.commit()
    db.session.close()
    
def dates(date = "2024-05-25 19:00"):
    
    date = datetime.strptime(date,'%Y-%m-%d %H:%M').strftime("%d %B %Y %H:%M")
    
    return date
