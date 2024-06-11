

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


class StatisticsActions:
    
    def show_calendar(self, place , e):
        
        self.statistics_dates.grid(row = 2 , column = 0 , columnspan = 2 , sticky = W+E)

        if place == "from":
            self.statistics_dates.calendar.grid(row = 2 , columnspan = 2 , column = 0 , sticky = W+E)
            self.place.set("from")
            self.calendar_from.configure(fg_color = "Lightblue4" , text_color = 'white')
            
        else:
            self.statistics_dates.calendar.grid(row = 2 , columnspan = 2 , column = 0 , sticky = W+E)
            self.place.set("to")
            self.calendar_to.configure(fg_color = "Lightblue4" , text_color = 'white')
            
        
    def forget_calendar(self , e):

        self.statistics_dates.calendar.grid_forget()
        self.calendar_from.configure(fg_color = "white" , text_color = 'gray')
        self.calendar_to.configure(fg_color = "white" , text_color = 'gray')
        
        
    def test_calendar(self , e):
        
        date = self.statistics_dates.calendar.get_date() 

        if self.place.get() == "from":
            self.date_from.set(datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y"))
            
        else:
            self.date_to.set(datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y"))
               
        StatisticsActions.forget_calendar(self , e)
        
        print(self.date_from.get() , self.date_to.get())
        

class Statistics:
    
    def totals():
        sum_total_products_sold =  db.session.query(func.sum(Orders.product_units)).scalar()
        sum_total_orders = len(db.session.query(Orders).all())
        
        return sum_total_orders , sum_total_products_sold
    
        
    def statistics_dataframe(self):
        
        all_products = db.session.query(Products).all()
        all_orders = db.session.query(Orders).all()
      
        product_reference = list(product.reference for product in all_products)
        product_stock = list(product.units for product in all_products)
        product_price = list(product.price for product in all_products)
        
        order_reference = []
        order_product_reference = []
        order_product_name = []
        order_product_price = []
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
            order_product_reference.append(order.product_reference)
            order_product_name.append(db.session.get(Products , order.product_reference).product_name)
            order_product_price.append(db.session.get(Products , order.product_reference).product_name)
            order_product_units.append(order.product_units)
            order_date.append(order.order_date)
            order_client.append(order.order_client_id)
            order_buyer.append(order.buyer_id)
            order_seller.append(order.seller_id)
            order_import.append(order.total_import)
            order_product_discount.append(order.order_product_discount)
            order_discount.append(order.order_discount)
            
         #Productos Más: referencia, nombre, precio, unidades, número de pedidos  pedido , media unidades ,  importe total , fecha
         
        orders_dict = {
            'order_reference' : order_reference,
            'order_product_reference' :  order_product_reference ,
            'order_product_name' : order_product_name,
            'order_product_price' : order_product_price ,
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
        
        return orders_dataframe
    
    
class Graphics:
    
    def example(self):
        
        sum_products = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()[0:30]
        
        self.grapics_container = CTkFrame(self.view_graphics_frame)
        self.grapics_container.grid(row = 0 , column = 0 , sticky = "nswe")
        self.grapics_container.grid_columnconfigure(0 , weight = 1)
        self.grapics_container.grid_rowconfigure(0 , weight = 1)
        
        self.grapics = CTkScrollableFrame(self.grapics_container , orientation =  'horizontal' , fg_color = 'transparent')
        self.grapics.grid(row = 0 , column = 0 , sticky = "nswe")

        
        for i, product in enumerate(sum_products):
            
            column_height = product[1] // 5
            
            units_label = CTkLabel(self.grapics , fg_color = "transparent" , text = str(product[1]), width = 30 , corner_radius = 4)
            units_label.grid(row = 1 , column = i , sticky = "s" , padx = 10)
            
            row = CTkFrame(self.grapics , fg_color = "DeepSkyBlue2" , height = column_height , width = 30 , corner_radius = 4)
            row.grid(row = 2 , column = i , sticky = "s" , padx = 10)
            
            label_refernce = CTkButton(self.grapics , fg_color = "Lightblue4" , text = str(product[0]) , width = 30 , corner_radius = 4 , text_color = "white" , command = lambda reference = product[0]: DataGraphic.data_graphic(self, reference))
            label_refernce.grid(row = 0 , column = i , padx = 10 , pady = 10 , sticky = 'we')
            
            
            
       
    
    
class DataGraphic:
    
    def data_graphic(self , reference):
        
        print("")
        
        
        
        
        
    
# Productos Más: precio, unidades, importe total , número de pedidos , media unidades pedido

# Productos Menos: precio, unidades, importe total , número de pedidos ,  media unidades pedido

# Precio Más: precio, unidades, importe total , número de pedidos , media veces pedido

# Precio Menos: precio, unidades, importe total , número de pedidos media unidades pedido

# Categuría Más: precio, unidades, importe total , número de pedidos ,  elementos en subcategoría ,media veces pedido , Porcentajes subcatgorías

# Categuría Menos: precio, unidades, importe total , número de pedidos , elementos en subcategoría ,media unidades pedido , Porcentajes subcatgorías

# Pedidos Importe Más:  importe total , número de pedidos , media unidades pedido , cantidad de categorías y subcategorías

# Pedidos Importe Menos:  importe total , número de pedidos media unidades pedido , cantidad de categorías y subcategorías

# Pedidos Unidades Más:  importe total , número de pedidos , media unidades pedido , cantidad de categorías y subcategorías

# Pedidos Unidades Menos:  importe total , número de pedidos media unidades pedido , cantidad de categorías y subcategorías

