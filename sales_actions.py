from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs
import tkinter as tk
from tkinter import ttk , filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
from models import Employee , Client , Contact , ContactPerson , Products , Orders
import db
import openpyxl
from sqlalchemy import and_ , or_ , func ,asc , desc
from datetime import datetime , timedelta
from tkinter import messagebox as mb
from sqlalchemy.exc import IntegrityError , SQLAlchemyError 
from customtkinter import *
import pandas as pd



class OrderFunctions:
    
    def show_products(self): 
        
        self.products_tree.tag_configure("odd", background="snow2" )
        self.products_tree.tag_configure("even", background="white")
        self.products_tree.tag_configure("font_red", foreground="red")
        self.products_tree.tag_configure("font_green", foreground="green")
        
        try:
            clean = self.products_tree.get_children()
            
            for x in clean: 
                self.products_tree.delete(x)
                        
        except Exception as e:
            print("[show_products]: (Clean): " , e)

        products = db.session.query(Products).order_by(Products.category).all()
        
        for i , product in enumerate(products):
            font = ""
            
            if product.units == 0:
                font = 'font_red'
                
            self.products_tree.insert("" , 0 , text = product.reference , values = (product.product_name , product.price , product.units , product.category , product.subcategory) , tags=(font))

        try:
            client = db.session.get(Client , self.company_id.get())
            
            if client is not None:
                self.order_header.set(f'[{client.id_client}] {client.name}')
                                
            else:
                self.order_header.set('Pedido')
            
            
            
        except Exception as e:
            print(f'[sales_view]: {e}')
            
            
        
    def row_colors(self, clients , ordenado , date , bgcolor , contacts , dot):
        for i , client in enumerate(clients):

            if ordenado.at[i, 'next'] <= str(date)[:11] + "23:59":               
                
                if int(ordenado.at[i, "days"]) >= 60:
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
                    
                if len(str(ordenado.at[i, 'cp'])) == 4:
                    postal_code = f"0{ordenado.at[i, 'cp']}"
                    
                else:
                    postal_code = ordenado.at[i, 'cp']
                    
                self.infoproducts_tree.insert("" , 0 , text = ordenado.at[i, 'state'] , values = (str(ordenado.at[i, 'days']).lstrip("0") , ordenado.at[i, 'name'] , MyCalendar.format_date_to_show(ordenado.at[i, 'last'])  , next_contact , postal_code) , tags=(color, font) )
                
                contacts += 1
                bgcolor += 1
                
        return contacts
    
    
    def get_product(self , e):

        try:
            reference = LoadInfo.get_item(self , "products" , self.products_tree , e)
            print(reference)
            product = db.session.query(Products).filter(Products.reference == reference).first()
            
            OrderFunctions.load_product(self , product)
            
            if e == "order":
                OrderFunctions.add_product(self , product)
            
        except Exception as e:
            print(f'[get_product]: {e}')
        
    
    def load_product(self , product):
       
        try:
            self.header_description.set(f"[{product.reference}] {product.product_name}")
            self.product_description.delete(1.0 , 'end')
            self.product_description.insert('end' , product.description)
            self.expiration.set(MyCalendar.format_date_to_show(f'{product.expiration} 08:00')[0:-6])
        
        except Exception as e:
            print(f"[load_product]: {e}")
        
        
    def add_product(self , product):
        
        client = db.session.get(Client , self.company_id.get())
        
        if self.product_units_entry.get().isdigit():      
            row_import = round(int(self.product_units_entry.get()) * product.price , 2)
            
            if product.discount != 0:
                row_import = row_import - (row_import * int(product.discount) / 100)
                
            self.order_tree.insert('' , 0 , text = product.reference , values = (product.product_name , product.price , self.product_units_entry.get() , f"{product.discount} %" , row_import))
            self.product_description.delete(1.0 , 'end')
            self.product_description.insert('end' , product.description)
            
            OrderFunctions.calculate_import(self)
            
        else:
            mb.showwarning("Unidades" , "Las unidades deben ser un número entero.")
            
            
    def calculate_import(self , e = ""):
        
        order = self.order_tree.get_children()
        total = []
        for item in order:
            row_import = float(self.order_tree.item(item , 'values')[-1])

            total.append(row_import)
                                
        self.order_import.set(round(sum(total) , 2))
        
        if self.discount.get():
            width_discount =  sum(total) - (sum(total) * int(self.discount.get()) / 100)
            total_order_import = width_discount + width_discount * 8 / 100
            
        else:
            total_order_import = sum(total) + (sum(total) * 8 / 100)
            
        self.total_order_import.set(round(total_order_import , 2))
        #item = self.info.selection_set(item)
        
        
    def eliminate_product(self):
        
        item = self.order_tree.focus()
        
        self.order_tree.delete(item)
        
        OrderFunctions.calculate_import(self , e = "")
        
        
    def send_order(self): 
        
        id_order = db.session.query(Orders).order_by(Orders.id_order.desc()).first()
        
        if id_order is not None:
            id_order = id_order.id_order + 1
                           
        else:    
            id_order = 1 
               
        order = self.order_tree.get_children()
        
        for x in order:#         id_order , product_reference ,                product_units ,                        order_client_id ,                 seller_id ,                   order_date ,                total_import                         , order_notes):
        
            order_entry = Orders(id_order ,self.order_tree.item(x , 'text') , self.order_tree.item(x , 'values')[2] , self.company_id.get() , self.active_employee_id.get() , str(datetime.now())[0:16] , self.order_tree.item(x , 'values')[4] , self.oreder_notes.get(1.0, "end") )
            
            db.session.add(order_entry)
            db.session.commit()
            
        db.session.close()