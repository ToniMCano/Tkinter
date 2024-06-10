

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
    
        
    def product_statistics(self):
        
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

