
import openpyxl
from openpyxl import Workbook
import random
import sqlalchemy
from sqlalchemy import and_ , or_ , func ,asc , desc
import db
from models import Client , ContactPerson , Employee , Contact , Products , Orders
from datetime import datetime , timedelta
import os
from tkinter import messagebox as mb
import customtkinter
from actions import GetInfo,LoadInfo , MyCalendar
import pandas as pd
import threading
import time
from tkinter import * 
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np

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
    alias = 151
    alias2 = 1
    employee = 1
    starts = start_date()



    for x in excel["Hoja 1"]:
        if len(x[0].value.split(" - ")[0]) >= 2:
            nace.append(x[0].value)
            
    for employee_id in range(3):
        for data_row in range(50):
            row.append("Company".lower() + str(alias))
            row.append(random.choice(nif_check).capitalize() + "".join(random.choices(nif , k=8)))
            row.append(f"Street{str(alias)}-{str(alias)}-{str(random.randint(1,20))} {random.choice(nif_check).capitalize()}-City{str(alias)}-Province{str(alias)}")
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
            row.append(starts[alias2 - 1])
            row.append(random.randint(0,1))
            row.append(0) # created_by
            
            if row[-2] == 0:
                row[-5] = "Lead"
            else:
                row[-5] = "Candidate"

            data.append(row)
            
            row = []
            
            alias += 1
            alias += 2
            
        employee += 1
            
    for x in data: 
        active_sheet.append(x) # Añadimos las filas
        
    wb.save("data2.xlsx")    
    
    
def start_date():
    
    day =random.randint(1,25) 
    month = random.randint(3,4)
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
                contact_random = Contact(contact_type = company.state, last_contact_date = f"{last[i]} {str(random.randint(8,19))}:00" , next_contact = f"{next[i]} {str(random.randint(8,19))}:00"  , log =  "No localizado, estará a parir de las 16:00" ,client_id =  company.id_client , contact_counter = 1 , contact_employee_id = company.employee_id , contact_person_id =  company.contact_person)
            
                db.session.add(contact_random)
                db.session.commit()
    
    db.session.close()


def date():
    
    last = []
    next = []
    
    for x in range(25):
        
        day = str(random.randint(1 , 28))
        month = str(random.randint(1, 12))
        hours = str(random.randint(10, 21)) 
        minutes = str(random.randint(10, 59))
        
        if len(day) < 2:
            day =f"0{day}"
        if len(month) < 2:   
            month =f"0{month}"
        
        date_s = f"2024-{month}-{day} {hours}:{minutes}"

        
    return date_s
     
        
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
   
    
def optimizar2():
    clients = db.session.query(Client).all()
    for dates in clients:
        
        dates.start_contact_date = date()
    db.session.commit()
    db.session.close()
        
        
def otro():    

    clients = db.session.query(Client).all()
    contact_people = db.session.query(ContactPerson).all()
    clients_list = []
    contact_people_list = []
    
            
    for x in clients:
        clients_list.append(x.id_client)

    for x in contact_people:
        contact_people_list.append(x.id_person)
        
    for x in clients:
        
        if x.id_client not in contact_people_list:
            #contact_name , contact_surname , contact_job_title, contact_phone , contact_mobile , contact_mail ,client_id , notes = "" , added_by = 0):
            new_person = ContactPerson(f"Name{x.id_client}" , f"Surame{x.id_client}" , "General Manager" , int("9" + ''.join(random.choices(nif , k = 8))) , int("6" + ''.join(random.choices(nif , k = 8))) , f"mail@{x.name}.com" , x.id_client)  
            
            db.session.add(new_person)
            db.session.commit()
            
            new_person.id_person = x.id_client 
            db.session.commit()
            
            clients_list.remove(x.id_client)
            
import random


        
def fecha():

    caducidad = f'{random.randint(2024,2025)}-{random.randint(6,12)}-{random.randint(1,28)}'
    caducidad = caducidad.split("-")
    if len(caducidad[1]) == 1:
        
        caducidad[1] = f"0{caducidad[1]}"

    if len(caducidad[2]) == 1:    
        caducidad[2] = f"0{caducidad[2]}"
    #new = Products(product[0] , product[1] , product[2] , product[3] , product[4] , product[5] , product[6])
    caducidad = "-".join(caducidad)   
    return caducidad
            
# Definición de categorías y subcategorías
categorias = ['Frutas', 'Vegetales', 'Lácteos', 'Carnes']
subcategorias = {
    'Frutas': ['Frescas', 'Congeladas', 'Enlatadas'],
    'Vegetales': ['Frescos', 'Congelados', 'Enlatados'],
    'Lácteos': ['Leche', 'Queso', 'Yogur'],
    'Carnes': ['Res', 'Pollo', 'Pescado']
}

# Función para generar productos aleatorios
def generar_producto():
    referencia = random.randint(1000, 9999)
    nombre = f"Producto {referencia}"
    precio = round(random.uniform(1, 10), 2)
    unidades = random.randint(50, 200)
    caducidad = fecha()
    categoria = random.choice(categorias)
    subcategoria = random.choice(subcategorias[categoria])
    return [referencia, nombre, precio, unidades, caducidad , categoria, subcategoria]

'''listado = []
# Generar 500 productos
productos = [generar_producto() for _ in range(500)]

# Mostrar algunos productos para verificar
for i in range(500):
    listado.append(productos[i])
    
#  reference , product_name , price , units , expiration , category , subcategory):
 
              
for product in listado:
    try:
        new = Products(product[0] , product[1] ,  product[2] , product[3] , product[4] , product[5] , product[6])
        db.session.add(new)
        db.session.commit()
    except Exception as e:
        product[0] = product[0] + 1
db.session.close()'''

'''refact = db.session.query(Client).all()
today = datetime.now()

for x in refact:

    dates = x.start_contact_date

    days = str(today - datetime.strptime(dates, "%Y-%m-%d %H:%M")).split(" ")[0]
    if len(days) > 3:
        days = '0'
    if len(days) == 1:
        days = f"0{days}"
    
    print(days)
    
    
   ''' 
   

def check_mail(complete_mail):
          
        try: 
            print(complete_mail.split("@")[0].rsplit(".")[0])
            print(complete_mail.split("@")[-1].split(".")[-1])
            if '@' in complete_mail and '.' in complete_mail:
                if len(complete_mail.split("@")[0].rsplit(".")[0]) >= 1 and len(complete_mail.split("@")[-1].split(".")[-1]) > 2:

                   return complete_mail
                   
                else:
                   raise Exception
               
        
        except Exception as e:
            mb.showwarning("Teléfonos" , f"{complete_mail}")
                           
                           
                           
def delete_peson_by_error(self):
        
        query = db.session.query(ContactPerson).filter(ContactPerson.client_id == 'Id de la Empresa')
        
        for contact in query:
            print(contact)
            db.session.delete(contact)
        
        db.session.commit()
        db.session.close()

delete_peson_by_error("self")


def test_orders():
    clients = db.session.query(Client).all()
    products = db.session.query(Products).all()
    employees = db.session.query(Employee).all()
    order_id = 0
    # id_order , product_reference , product_units , order_client_id , seller_id , buyer_id, order_date , total_import , order_notes , order_discount = 0 , order_product_discount = 0):
        
    for order in range(5000):
        client = clients[random.randint(1,len(clients) -1)]
        order_id += 1 
        seller_id =  employees[random.randint(0,2)].id_employee
        buyer_id = client.contact_person
        order_date = date()
        order_client_id = client.id_client 
        
        for product_entry in range(1,18):
            id_order = order_id
            product_reference = products[random.randint(1,len(products)) - 1].reference
            product_units = random.randint(1,24)
            price = db.session.get(Products , product_reference).price
            total_import = product_units * price
            
            order = Orders(id_order, product_reference , product_units , order_client_id , seller_id , buyer_id , order_date , total_import , "" , 0 , 0)
            db.session.add(order)
    db.session.commit()
    db.session.close()
        
    



def graficos():
    # Generar datos de ejemplo
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Crear la gráfica
    plt.plot(x, y)
    plt.title("Gráfica de seno")
    plt.xlabel("x")
    plt.ylabel("sin(x)")

    # Mostrar la gráfica y bloquear la ejecución del programa
    plt.show(block=True)

    # Este código se ejecutará después de cerrar la ventana de la gráfica
    print("La ventana de la gráfica se ha cerrado.")


def product_statistics():
        
        all_products = db.session.query(Products).all()
        all_orders = db.session.query(Orders).all()
      
        product_reference = list(product.reference for product in all_products)
        product_stock = list(product.units for product in all_products)
        product_price = list(product.price for product in all_products)
        
        
        order_reference = []
        order_product = []
        order_product_units = []
        order_date = []
        order_client = []
        order_buyer = []
        order_seller = []
        order_import = []
        order_product_discount = []
        order_discount = []
        
        for order in all_orders:
            order_reference.append(order.id_order)
            order_product.append(order.product_reference)
            order_product_units.append(order.product_units)
            order_date.append(order.order_date)
            order_client.append(order.order_client_id)
            order_buyer.append(order.buyer_id)
            order_seller.append(order.seller_id)
            order_import.append(order.total_import)
            order_product_discount.append(order.order_product_discount)
            order_discount.append(order.order_discount)
        
        orders_dict = {
            'order_reference' : order_reference ,
            'order_product' :  order_product ,
            'order_product_units' : order_product_units ,
            'order_date' : order_date ,
            'order_client' : order_client  ,
            'order_buyer' : order_buyer ,
            'order_seller' : order_seller ,
            'order_import' : order_import ,
            'order_product_discount' : order_product_discount ,
            'order_discount' : order_discount
        }
            
        orders_dataframe = pd.DataFrame(orders_dict)
        
        print(orders_dataframe.head())

    


'''
GRÁFICAS CON MATPLOTLIB

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel('fruit supply')
ax.set_title('Fruit supply by kind and color')
ax.legend(title='Fruit color')

plt.show()


'''

def example():
    #2526
    product = db.session.get(Products , 9903)
    
    units = db.session.query(Orders).filter(Orders.product_reference == product.reference).group_by(Orders.id_order).all()
    
    print(len(units))    


class Test:   
        
    def statistics_dataframe(self):
            
            all_products = db.session.query(Products).all()
            all_orders = db.session.query(Orders).all()
        
            product_reference = list(product.reference for product in all_products)
            product_stock = list(product.units for product in all_products)
            
            
            
            orders_id = [order.id_order for order in all_orders]
            orders_product_reference = [order.product_reference for order in all_orders]
            orders_product_name = [db.session.get(Products , order.product_reference).product_name for order in all_orders]
            product_price = [db.session.get(Products , order.product_reference).price for order in all_orders] ###
            orders_product_units = [order.product_units for order in all_orders]
            orders_import = [order.total_import for order in all_orders]
            product_catgory = [db.session.get(Products , order.product_reference).category for order in all_orders]
            product_subcatgory = [db.session.get(Products , order.product_reference).subcategory for order in all_orders]
            
            
            data = {
                'orders_id' : orders_id ,
                'orders_product_reference' : orders_product_reference ,
                'orders_product_name' : orders_product_name ,
                'product_price' : product_price ,
                'orders_product_units' : orders_product_units ,
                'orders_import' : orders_import ,
                'product_catgory' : product_catgory ,
                'product_subcatgory' : product_subcatgory 
            }
            
            
            data_frame = pd.DataFrame(data)
            
            data_frame['total_products_solded'] = data_frame.groupby('orders_product_reference')['orders_product_units'].sum()
            

                
def series():

    time_now = datetime(2025,12,28) 
    time_formated = time_now.strftime('%Y-%m-%d')
    time_formated2 = datetime.strptime(time_formated , '%Y-%m-%d').strftime("%d %B %Y")
    
    print(time_now , type(time_now))
    print(time_formated , type(time_formated))
    print(time_formated2 , type(time_formated2))
    
series()

