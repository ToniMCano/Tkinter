
import openpyxl
from openpyxl import Workbook
import random
import sqlalchemy
from sqlalchemy import and_ , or_
import db
from models import Client , ContactPerson , Employee , Contact
from datetime import datetime
import os



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


    for x in excel["Hoja 1"]:
        nace.append(x[0].value)
            
    for employee_id in range(3):
        for data_row in range(50):
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
            row.append(start_date())
            row.append(random.randint(0,1))
            
            if row[-1] == 0:
                row[-4] = "Pool"

            data.append(row)
            
            row = []
            
            alias += 1
            
        employee += 1
            
    for x in data: 
        active_sheet.append(x) # Añadimos las filas
        
    wb.save("data.xlsx")    
    
    
def start_date():
    
    date = ["2024", str(random.randint(1,3)) , str(random.randint(1,30))]
    
    if len(date[1]) == 1:
        date[1] = f"0{date[1]}"
        
        if date[1] == "02":
            date[2] = str(random.randint(1,28))
        
    if len(date[2]) == 1:
        date[2] = f"0{date[2]}"
        
    row = "-".join(date)  
    return row


def contacts():   # UN CONTACTO PARA CADA EMPRESA
    
    registro = []
    
    for i , person in enumerate(range(150)):
        
        contact = ContactPerson(f"Name{str(i+1)}" , f"Surname{str(i+1)}" , f"General Manager" , int(f"9{''.join(random.choices(nif , k = 8))}") , "" , f"contact{str(i+1)}@mail.com" , i+1 , "Notes")        
        try:
            db.session.add(contact)
            db.session.commit()
            print("ok")
            
        except Exception as e:
            print(e)
        
    db.session.close()
            
    
def insertar(excel):  # excel debe ser la referencia a una hoja (excel["Sheet"])
    rows = []
    ready = []
    
    for row in excel.rows:
        for cell in row:
            rows.append(cell.value)
        ready.append(rows)
        rows = []
    
    for registro in ready:
        new = Client(registro[0] , registro[1] , registro[2] , registro[3] , registro[4] , registro[5] , registro[6] , registro[7] , registro[8] , registro[9] , registro[10] , registro[11])
        db.session.add(new)
        db.session.commit()
    db.session.close()    
              

def empleados():
     
    for i , x in enumerate(range(3)):
        
        employee = Employee(f"EA{str(i)}", f"Name{str(i)}" , f"Surname{str(i)}" , f"ea{str(i)}@company.com", int(f"9652293{str(i)}") ,"Comercial" , 1234 , 1)
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


def check_employee(window , employee_password = 1234 , alias = "EA1"):
    employees =  db.session.query(Employee).all()
    exists = False
    for employee in employees:
        if employee.employee_alias == alias and employee.password == str(employee_password):
            load_contacts()
            exists = True
            window.destroy()
            load_contacts(employee.id_employee)
    if not exists:
        print("El usuario o la contraseña no son correctos")
            
        
        
def test3():
    clientes = db.session.query(Client)
    #contactss = db.session.query(Contact).filter(Contact.contact_person_id == ).all()
    
    for x in clientes:
        contactss = db.session.query(Contact).filter(Contact.contact_person_id == x.id_client ).all()
        for y in contactss:
            y.contact_counter = x.counter
        

datos_muestra()
contact()
contacts()
empleados()
