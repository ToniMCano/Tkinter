

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
            self.statistics_date_from.set(datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y"))
            
        else:
            self.statistics_date_to.set(datetime.strptime(date,'%Y-%m-%d').strftime("%d %B %Y"))
               
        StatisticsActions.forget_calendar(self , e)
        
        print(f"Desde {self.statistics_date_from.get()} Hasta {self.statistics_date_to.get()}")
        

class StatisticsDataFrame:
    
    def totals():
        sum_total_products_sold =  db.session.query(func.sum(Orders.product_units)).scalar()
        sum_total_orders = len(db.session.query(Orders).all())
        
        return sum_total_orders , sum_total_products_sold
    
        
    def statistics_dataframe(self , e):
        
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
            order_product_price.append(db.session.get(Products , order.product_reference).price)
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
        print('orders_dataframe\n\n')
        print(orders_dataframe.head(int(self.statistics_number_views.get())))
        # DEBE EJECUTARSE DESDE LA FUNCIÓN DE LOGIN SOLO.
        return orders_dataframe
    
    
class StatisticsValues:
    
    
    def switch_dates_all(self):
        
        if self.statistics_dates_all.get():
            self.all_time.set(True)
            
            self.statistics_date_from.set('All Time')
        
            self.statistics_date_to.set('All Time')
            
        else:
            self.all_time.set(False)
            
            self.statistics_date_from.set(datetime.now().strftime("%d %B %Y")) 
            
            self.statistics_date_to.set(datetime.now().strftime("%d %B %Y")) 
        
        
    def statistics_values(self):
        
        employee_company = self.statistics_employee.get()
        
        types = self.statistics_type.get()

        quantity = int(self.statistics_number_views.get())

        #quantity = self.statistics_wich.get()
        
        if not self.all_time.get():

            date_from = self.statistics_date_from.get()
        
            date_to = self.statistics_date_to.get()
            
        else:
            date_from = ""
        
            date_to = ""
            
            
        values =  [date_from , date_to , types , quantity , employee_company]
         
        print(values)

    
class Graphics:
    
    def example(self):
    
        sum_products = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()
        
        Graphics.get_number_of_products(self , len(sum_products))
        
        self.grapics_container = CTkFrame(self.view_graphics_frame)
        self.grapics_container.grid(row = 0 , column = 0 , sticky = "nswe")
        self.grapics_container.grid_columnconfigure(0 , weight = 1)
        self.grapics_container.grid_rowconfigure(0 , weight = 1)
        
        self.grapics = CTkScrollableFrame(self.grapics_container , orientation =  'horizontal' , fg_color = 'transparent')
        self.grapics.grid(row = 0 , column = 0 , sticky = "nswe")

        
        for i, product in enumerate(sum_products[0: self.number_of_products]):
            
            self.grapics.grid_columnconfigure(i , weight = 1)
            
            column_height = product[1] // 5
            
            units_label = CTkLabel(self.grapics , fg_color = "transparent" , text = str(product[1]), width = 40 , corner_radius = 4)
            units_label.grid(row = 1 , column = i , sticky = "swe" , padx = 10)
            
            row = CTkFrame(self.grapics , fg_color = "DeepSkyBlue2" , height = column_height , width = 40 , corner_radius = 4)
            row.grid(row = 2 , column = i , sticky = "swe" , padx = 10)
            
            label_refernce = CTkButton(self.grapics , fg_color = "Lightblue4" , text = str(product[0]) , width = 40, corner_radius = 4 , text_color = "white" , command = lambda reference = product[0]: DataGraphic.data_to_charge(self, reference))
            label_refernce.grid(row = 0 , column = i , padx = 10 , pady = 10 , sticky = 'swe')
            
    
    def get_number_of_products(self , len_products):
        
        if self.statistics_number_views.get() != "Todo" and len_products > int(self.statistics_number_views.get()):
            self.number_of_products = int(self.statistics_number_views.get())
                                          
        else:
            self.number_of_products = -1            
            
class DataGraphic:
    
    
    def data_to_charge(self , reference):
        
        product = db.session.get(Products , reference)
        
        self.units = db.session.query(Orders.product_reference , func.sum(Orders.product_units)).filter(Orders.product_reference == product.reference).first()[-1]

        self.data_graphic_reference = product.reference
        
        self.data_graphic_name = product.product_name
        
        self.data_graphic_price = product.price
        
        self.order_count = db.session.query(Orders).filter(Orders.product_reference == product.reference).group_by(Orders.id_order).all()

        self.products_by_order = self.units // len(self.order_count)

        self.total_product_import = self.units * product.price
        
        self.order_periodicity = DataGraphic.peridicity(self , reference , len(self.order_count))
        
        data = {
            'reference' : str(product.reference) ,
            'name' : product.product_name ,
            'units' : str(self.units) ,
            'price' : str(self.data_graphic_price) ,
            'orders' : str(len(self.order_count)) ,
            'product_by_order' : str(self.products_by_order) ,
            'total_import' : str(round(self.total_product_import , 2)) , 
            'periodicity' : str(self.order_periodicity) ,
            'category' : product.category ,
            'subcategory' : product.subcategory 
        }
        
        
        DataGraphic.charge_data(self , data)
    
    
    def peridicity(self , reference , len_orders):
        
        first = db.session.query(Orders).filter(Orders.product_reference == reference).order_by(Orders.order_date).first()
        last = db.session.query(Orders).filter(Orders.product_reference == reference).order_by(Orders.order_date.desc()).first()
        
        first_date = first.order_date.split('-')
        last_date = last.order_date.split('-')
        
        period = datetime(int(last_date[0]) , int(last_date[1]) , int(last_date[2][:2])) - datetime(int(first_date[0]) , int(first_date[1]) , int(first_date[2][:2]))
        
        days =  round(int(period.days) / int(len_orders) , 2)

        return days
        
        
    
    def charge_data(self , data):
        
        self.view_data_header = CTkFrame(self.view_data_frame , fg_color = 'transparent' , corner_radius = 4 , height = 40)
        self.view_data_header.grid(row = 1 , column = 0 , sticky = 'nswe')
   
        self.view_data_header.grid_columnconfigure(0, weight = 1)
        self.view_data_header.grid_columnconfigure(1, weight = 1)
        self.view_data_header.grid_rowconfigure(1, weight = 1)
        self.view_data_header.grid_rowconfigure(2, weight = 1)
        self.view_data_header.grid_rowconfigure(3, weight = 1)
        self.view_data_header.grid_rowconfigure(4, weight = 1)
        self.view_data_header.grid_rowconfigure(5, weight = 1)
        
        #Productos Más: referencia, nombre, precio, unidades, número de pedidos  pedido , media unidades ,  importe total , fecha

        self.product_reference_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.product_reference_view_frame.grid(row = 1 , column = 0 , sticky = 'nswe' ,  padx = 6 , pady = 3)
        self.product_reference_view_frame.grid_rowconfigure(0 , weight = 1)
        self.product_reference_view_frame.grid_columnconfigure(0, weight = 1)
        self.product_reference_view_frame.grid_columnconfigure(1, weight = 1)

        self.product_reference_view_label = CTkLabel(self.product_reference_view_frame , text = 'Referencia' , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.product_reference_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.product_reference_info = CTkLabel(self.product_reference_view_frame , text = data['reference'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.product_reference_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)

        self.name_view_frame = CTkFrame(self.view_data_header  , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.name_view_frame.grid(row = 2 , column = 0 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.name_view_frame.grid_rowconfigure(0 , weight = 1)
        self.name_view_frame.grid_columnconfigure(0, weight = 1)
        self.name_view_frame.grid_columnconfigure(1, weight = 1)

        self.name_view_label = CTkLabel(self.name_view_frame  , text = 'Nombre' , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.name_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.name_view_info = CTkLabel(self.name_view_frame , text = data['name'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.name_view_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.price_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.price_view_frame.grid(row = 3 , column = 0 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.price_view_frame.grid_rowconfigure(0 , weight = 1)
        self.price_view_frame.grid_columnconfigure(0, weight = 1)
        self.price_view_frame.grid_columnconfigure(1, weight = 1)

        self.price_view_label = CTkLabel(self.price_view_frame , text = "Precio" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.price_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.price_view_info = CTkLabel(self.price_view_frame , text = data['price'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.price_view_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.category_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.category_frame.grid(row = 4 , column = 0 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.category_frame.grid_rowconfigure(0 , weight = 1)
        self.category_frame.grid_columnconfigure(0, weight = 1)
        self.category_frame.grid_columnconfigure(1, weight = 1)

        self.category_label = CTkLabel(self.category_frame , text = "Categoría" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.category_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.category_info = CTkLabel(self.category_frame , text = data['category'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.category_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.subcategry_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.subcategry_frame.grid(row = 5 , column = 0 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.subcategry_frame.grid_rowconfigure(0 , weight = 1)
        self.subcategry_frame.grid_columnconfigure(0, weight = 1)
        self.subcategry_frame.grid_columnconfigure(1, weight = 1)

        self.subcategry_label = CTkLabel(self.subcategry_frame , text = "Subcategoría" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.subcategry_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.subcategry_info = CTkLabel(self.subcategry_frame , text = data['subcategory'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.subcategry_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.units_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.units_view_frame.grid(row = 1 , column = 1 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.units_view_frame.grid_rowconfigure(0 , weight = 1)
        self.units_view_frame.grid_columnconfigure(0, weight = 1)
        self.units_view_frame.grid_columnconfigure(1, weight = 1)

        self.units_view_label = CTkLabel(self.units_view_frame , text = "Unidades" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.units_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.units_view_info = CTkLabel(self.units_view_frame , text = data['units'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.units_view_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.orders_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.orders_view_frame.grid(row = 2 , column = 1 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.orders_view_frame.grid_rowconfigure(0 , weight = 1)
        self.orders_view_frame.grid_columnconfigure(0, weight = 1)
        self.orders_view_frame.grid_columnconfigure(1, weight = 1)

        self.orders_view_label = CTkLabel(self.orders_view_frame , text = "Pedidos" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.orders_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.orders_view_info = CTkLabel(self.orders_view_frame , text = data['orders'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.orders_view_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)

        self.order_units_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.order_units_view_frame.grid(row = 3 , column = 1 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.order_units_view_frame.grid_rowconfigure(0 , weight = 1)
        self.order_units_view_frame.grid_columnconfigure(0, weight = 1)
        self.order_units_view_frame.grid_columnconfigure(1, weight = 1)

        self.order_units_view_label = CTkLabel(self.order_units_view_frame , text = " Unidades/Pedido " , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.order_units_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.order_units_info = CTkLabel(self.order_units_view_frame , text = data['product_by_order'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.order_units_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)

        self.total_import_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.total_import_view_frame.grid(row = 4 , column = 1 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.total_import_view_frame.grid_rowconfigure(0 , weight = 1)
        self.total_import_view_frame.grid_columnconfigure(0, weight = 1)
        self.total_import_view_frame.grid_columnconfigure(1, weight = 1)

        self.total_import_view_label = CTkLabel(self.total_import_view_frame , text = "Importe" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.total_import_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.total_import_views_info = CTkLabel(self.total_import_view_frame , text = data['total_import'] , text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.total_import_views_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)

        self.date_view_frame = CTkFrame(self.view_data_header , corner_radius = 3 , border_width = 1 , border_color = 'gray')
        self.date_view_frame.grid(row = 5 , column = 1 , sticky = 'nswe' , padx = 6 , pady = 3)
        self.date_view_frame.grid_rowconfigure(0 , weight = 1)
        self.date_view_frame.grid_columnconfigure(0, weight = 1)
        self.date_view_frame.grid_columnconfigure(1, weight = 1)

        self.date_view_label = CTkLabel(self.date_view_frame , text = "Periodicidad" , text_color = "white" , fg_color = 'Lightblue4' , corner_radius = 3 , width = 120)
        self.date_view_label.grid(row = 0 , column = 0 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        
        self.date_view_info = CTkLabel(self.date_view_frame , text = f"{data['periodicity']} días", text_color = "gray" , font = ("" , 16 , 'bold') , fg_color = 'transparent' , corner_radius = 3 , width = 120)
        self.date_view_info.grid(row = 0 , column = 1 , sticky = 'nswe' ,  padx = 2 , pady = 2)
        


                
    
    def data_graphic(self , reference):
        
        print(reference)
        
             

        
    
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

