
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
from actions import GetInfo



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
            row.append(f"adress{str(alias)},{str(alias)} {str(random.randint(1,20))} - {random.choice(nif_check).capitalize()}  City{str(alias)}, (Province{str(alias)}) {''.join(random.choices(nif , k = 5))}")
            row.append(f"www.web{str(alias)}.com")  
            row.append(f"{row[0]}@{row[3][4:]}")
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
    
    for i , person in enumerate(range(150)):
                                                                                                                                                                                                      # added_by
        contact = ContactPerson(f"Name{str(i+1)}" , f"Surname{str(i+1)}" , f"General Manager" , int(f"9{''.join(random.choices(nif , k = 8))}") , "" , f"contact{str(i+1)}@mail.com" , i+1 , "Notes" , 0 )        
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
        
    for i , company in enumerate(range(150)):
        for contact in range(25):
            contact_random = Contact(company_state = "Contact" , last_contact_date = f"{date()} {str(random.randint(8,19))}:00" , next_contact = f"{date()} {str(random.randint(8,19))}:00"  , log =  "No localizado, estará a parir de las 16:00" ,client_id =  i+1 , contact_counter = random.randint(0,3) , contact_employee_id = random.randint(1,3) , contact_person_id =  i+1)
            db.session.add(contact_random)
            db.session.commit()
    db.session.close()

def date():
    day = str(random.randint(1 , 30))
    month = str(random.randint(1 , 12))
    
    if len(day) < 2:
        day =f"0{day}"
        
    if len(month) < 2:
        month =f"0{month}"
        

        
    return f"2024-{month}-{day}"
        
def load_contacts():
    contacts = db.session.query(Contact).filter(and_(Contact.company_state == "Contact" , Contact.contact_employee_id == 1 )).all()
    
    for client in contacts:
        company_name = db.session.query(Client).filter(Client.contact_person == client.contact_person_id).first()
        print(company_name.name)
               
#print ((str(datetime(2024,6,19 ) - datetime.now())[:3]))



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
datos_muestra()
            