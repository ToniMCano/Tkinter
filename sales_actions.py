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
        buyer = db.session.get(Client , self.company_id.get())
        buyer = buyer.contact_person
        
        if id_order is not None:
            id_order = id_order.id_order + 1
                           
        else:    
            id_order = 1 
               
        order = self.order_tree.get_children()
        
        for x in order:#         id_order , product_reference ,                product_units ,                        order_client_id ,                 seller_id ,         buyer_id ,            order_date ,                total_import                         , order_notes):
            
            order_entry = Orders(id_order ,self.order_tree.item(x , 'text') , self.order_tree.item(x , 'values')[2] , self.company_id.get() , self.active_employee_id.get() , buyer,  str(datetime.now())[0:16] , self.order_tree.item(x , 'values')[4] , self.oreder_notes.get(1.0, "end") )
            
            db.session.add(order_entry)
            db.session.commit()
            
        db.session.close()
        
        OrderFunctions.clean_order(self)
    
    
    def clean_order(self):
        
        clean = self.order_tree.get_children()
        
        for x in clean:
            self.order_tree.delete(x)
        
        self.discount.set("")
        self.total_order_import.set("")
        self.order_import.set("")
    
    
    def sales_historical(self):
        
        window = Toplevel()  
        window.configure(bg = "#f4f4f4")
        window.geometry("800x300")
        window.resizable(0,0)
        window.title(f"Historial de Ventas")
        window.grid_columnconfigure(0 , weight = 1)
        window.grid_rowconfigure(0 , weight = 1)
        
        client = db.session.get(Client , self.company_id.get())
 
        self.historial_frame = CTkFrame(window , fg_color = 'transparent')
        self.historial_frame.grid(row = 0 , column = 0 , padx = 10 , pady = 10 , sticky = "nswe")
        self.historial_frame.grid_columnconfigure(0 , weight = 1)
        #self.historial_frame.grid_rowconfigure(1 , weight = 1)
        
        self.historial_header = CTkFrame(self.historial_frame , border_width = 1 , border_color = 'gray' , fg_color = 'transparent' , height = 40)
        self.historial_header.grid(row = 0 , column = 0 ,  sticky = W+E , padx = 3 , pady = 3)
        self.historial_header.grid_columnconfigure(0 , weight = 1)
        self.historial_header.grid_columnconfigure(1 , weight = 1)
        self.historial_header.grid_columnconfigure(2 , weight = 1)
        self.historial_header.grid_columnconfigure(3 , weight = 1)
        self.historial_header.grid_columnconfigure(4 , weight = 1)
        
        self.reference_view_header = CTkLabel(self.historial_header , text = f"Referencia" , text_color = 'gray')
        self.reference_view_header.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.units_view_header = CTkLabel(self.historial_header , text = "Total Productos", text_color = 'gray')
        self.units_view_header.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W)
        
        self.price_view_header = CTkLabel(self.historial_header , text ="Importe" , text_color = 'gray')
        self.price_view_header.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W)
        
        self.date_view_header = CTkLabel(self.historial_header , text = "Fecha" , text_color = 'gray')
        self.date_view_header.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = W)
        
        self.date_view_header = CTkLabel(self.historial_header , text = f"Hasta: {MyCalendar.format_date_to_show(str(datetime.now())[:16])}" , width = 100 , fg_color = 'Lightblue4' , corner_radius = 4)
        self.date_view_header.grid(row = 0 , column = 4 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.historial_content = CTkScrollableFrame(self.historial_frame , border_width = 1 , border_color = 'gray' , fg_color = 'transparent' , scrollbar_fg_color = 'transparent' )
        self.historial_content.grid(row = 1 , column = 0 ,  sticky = W+E , padx = 3 , pady = 3)
        self.historial_content.grid_columnconfigure(0 , weight = 1)
        
        Pops.center_window(self , window)
        
        window.lift()
        
        OrderFunctions.group_orders(self)
        
        
    def group_orders(self):
        
        orders = db.session.query(Orders).filter(Orders.order_client_id == self.company_id.get()).all()
        
        orders_id = []
        
        for order in orders:          # Obtenemos un único id por pedido
            
            if order.id_order not in orders_id:
                orders_id.append(order.id_order)
            print(f"Lista de Ids: {orders_id}")
        for i, single_id in enumerate(orders_id):  # Obtenemos todos los productos del pedido con ese id
            single_order = db.session.query(Orders).filter(Orders.id_order == single_id).all()
            
            products = []
            imports = []
            
            self.orders_view = CTkFrame(self.historial_content , fg_color = 'lightgray' , corner_radius = 4)
            self.orders_view.grid(row = i , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            self.orders_view.grid_columnconfigure(0 , weight = 1)
            self.orders_view.grid_columnconfigure(1 , weight = 1)
            self.orders_view.grid_columnconfigure(2 , weight = 1)
            self.orders_view.grid_columnconfigure(3 , weight = 1)
            self.orders_view.grid_columnconfigure(4 , weight = 1)
            
            
            for order_view in single_order:   # Recorremos los productos y ...
                products.append(order_view.product_units)
                imports.append(order_view.total_import)
                product = db.session.get(Products , order_view.product_reference)
            
    
            self.reference_view = CTkLabel(self.orders_view , text = f"Pedido ID[{orders_id[i]}]" , text_color = 'gray')
            self.reference_view.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.units_view = CTkLabel(self.orders_view , text = str(sum(products)) , text_color = 'gray')
            self.units_view.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.price_view = CTkLabel(self.orders_view , text ="{:.2f}".format((sum(imports))) , text_color = 'gray' , anchor = "e")
            self.price_view.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.date_view = CTkLabel(self.orders_view , text = MyCalendar.format_date_to_show(order_view.order_date) , text_color = 'gray')
            self.date_view.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.date_view = CTkButton(self.orders_view , text = "Ver Pedido" , width = 80 , fg_color = 'Lightblue4' , corner_radius = 4 , command = lambda order_id_to = orders_id[i]: OrderFunctions.view_single_order(self , order_id_to))
            self.date_view.grid(row = 0 , column = 4 , padx = 5 , pady = 5 , sticky = E)
            
            
    def view_single_order(self , order_id):
                
        orders = db.session.query(Orders).filter(Orders.order_client_id == self.compnay_id.get()).all()
        orders_id = []
        
        for order in orders:          # Obtenemos un único id por pedido
            if order.order_client_id not in orders_id:
                orders_id.append(order.id_order)

        for single_id in orders_id:  # Obtenemos todos los productos del pedido con ese id
            single_order = db.session.query(Orders).filter(Orders.id_order == single_order).all()
            
            self.orders_view = ttk.Frame(self.historial_content)
            self.orders_view.grid(row = i , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            for i, order_view in enumerate(single_order):   # Recorremos los productos y ...

                product = db.session.get(Products , order_view.product_reference)
            
                self.reference_view = CTkLabel(self.orders_view , text = order_view.product_reference)
                self.reference_view.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
                
                self.product_name_view = CTkLabel(self.orders_view , text = product.product_name)
                self.product_name_view.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
                
                self.units_view = CTkLabel(self.orders_view , text = order_view.product_units)
                self.units_view.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
                
                self.price_view = CTkLabel(self.orders_view , text = product.price)
                self.price_view.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
                
                self.date_view = CTkLabel(self.orders_view , text = order_view.order_date)
                self.date_view.grid(row = 0 , column = 4 , padx = 5 , pady = 5 , sticky = W+E)