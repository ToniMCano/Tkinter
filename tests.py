
import openpyxl
from openpyxl import Workbook
import random
import sqlalchemy
from sqlalchemy import and_ , or_
import db
from models import Client , ContactPerson



nif = ['0','1','2','3','4','5','6','7','8','9']

def datos_muestra(): # EXCEL CON MUESTRA DE DATOS PARA PRUEBAS

    nif_check = ['a','b','c','e','f','g','h','j','p','q','r','s','u','v' , 'w' , 'n']

    excel = openpyxl.load_workbook("recursos\\NACE.xlsx")

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
        for data_row in range(20):
            row.append("Company".lower() + str(alias))
            row.append(random.choice(nif_check).capitalize() + "".join(random.choices(nif , k=8)))
            row.append(f"adress{str(alias)}-{str(alias)}-{str(alias + int(random.choice(nif)))}- City{str(alias)}- Province{str(alias)}-C.P:{"".join(random.choices(nif , k = 5))}")
            row.append(f"www.web{str(alias)}.com")  
            row.append(f"{row[0]}@{row[3][4:]}")
            row.append(int("9" + ''.join(random.choices(nif , k = 8)) )) 
            row.append("")
            row.append(random.choice(nace))
            row.append(0)
            row.append(employee)
            row.append("Pool")
            row.append(random.choice(employees))
            data.append(row)
            row = []
            alias += 1
        employee += 1
            
    for x in data: 
        active_sheet.append(x) # Añadimos las filas
        
    wb.save("data.xlsx")    
    

def contacts():   # UN CONTACTO PARA CADA EMPRESA
    
    registro = []
    
    for i , person in enumerate(range(60)):
        
        contact = ContactPerson(f"Name{str(i)}" , f"Surname{str(i)}" , f"General Manager" , int(f"9{"".join(random.choices(nif , k = 8))}") , "" , f"contact{str(i)}@mail.com" , i , "Notes")        
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
              
contacts()