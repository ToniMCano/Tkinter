

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
        


    
class StatisticsValues:  
    
    
    def switch_witch(self , value):
        
        if value == "+":
            self.less.deselect()
            self.all.deselect()
            
            self.statistics_wich.set("+")
            
        elif value == "-":
            self.more.deselect()
            self.all.deselect()
            
            self.statistics_wich.set("-")
            
        elif value == "all":
            self.more.deselect()
            self.less.deselect()
            self.statistics_wich.set("all")
            
        return value
    

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
        
        types = StatisticsValuesColors.choosed_types(self , 'product') if self.statistics_type.get() == "" else self.statistics_type.get()

        quantity = Graphics.get_number_of_products(self)

        wich =  StatisticsValues.switch_witch(self , "+") if self.statistics_wich.get() == "" else self.statistics_wich.get()
        
        if not self.all_time.get():
                                          
            date_from = datetime.strptime(self.statistics_date_from.get(),"%d %B %Y").strftime('%Y-%m-%d')
        
            date_to = datetime.strptime(self.statistics_date_to.get(),"%d %B %Y").strftime('%Y-%m-%d')
            
        else:
            date_from = False
        
            date_to = False
            
        values =  [date_from , date_to , types , quantity , wich , employee_company]
        
        print(values)
        
        Graphics.generate_graphic(self , values)



class StatisticsValuesColors:
    
    def choosed_types(self , choosed):
        
        StatisticsValuesColors.unchoosed_types(self)
        
        selected_color = "deep sky blue"
        
        if choosed == "product":
            self.statistics_type.set('product')

            self.products.configure(fg_color = selected_color )
        
        elif choosed == "price":
            self.statistics_type.set('price')

            self.price.configure(fg_color =  selected_color)
        
        elif choosed == "category":
            self.statistics_type.set('category')

            self.category.configure(fg_color =  selected_color)
        
        elif choosed == "subcategory":
            self.statistics_type.set('subcategory')

            self.subcategory.configure(fg_color =  selected_color)
        
        elif choosed == "order":
            self.statistics_type.set('order')

            self.orders.configure(fg_color =  selected_color)
        
        elif choosed == "order_import":
            self.statistics_type.set('order_import')

            self.orders_import.configure(fg_color =  selected_color)
        
        elif choosed == "client":
            self.statistics_type.set('client')

            self.client.configure(fg_color =  selected_color)
        
        else:
            self.statistics_type.set('client_all')

            self.clients.configure(fg_color =  selected_color)
            
        return choosed
        

    def unchoosed_types(self):
        
        selected_color = "Lightblue4"

        self.products.configure(fg_color = selected_color )
        self.price.configure(fg_color =  selected_color)
        self.category.configure(fg_color =  selected_color)
        self.subcategory.configure(fg_color =  selected_color)
        self.orders.configure(fg_color =  selected_color)
        self.orders_import.configure(fg_color =  selected_color)
        self.client.configure(fg_color =  selected_color)
        self.clients.configure(fg_color =  selected_color)
        

class InfoDB:
    
    def get_info_from_db(self, values): # values = [date_from , date_to , types , quantity , wich , employee_company]
        
        if values[-1] == 'Company':
            if not values[0]: 
                query = InfoDB.info_db_company_without_date(self, values)
                
            else:
               query = InfoDB.info_db_company(self, values)
               
        else:                
            try:
                employee = db.session.query(Employee).filter(Employee.employee_alias == values[-1]).first().id_employee
            
                if not values[0]:
                    query = InfoDB.info_db_without_date(self, values , employee)
                
                else:
                    if values[2] == 'product':
                        print("IF [get_info_from_db]")
                        
                        query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(and_(Orders.seller_id == employee , Orders.order_date > values[0] , Orders.order_date <= values[1])).group_by(Orders.seller_id, Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                    
                    else:
                        print("ELSE [get_info_from_db]")
                        query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()
                
            except Exception as e:
                print(f"[get_info_from_db]: {e}")
        
        return query

     
    def info_db_without_date(self , values , employee_id):
        
        try:
            if values[2] == 'product':
                print("IF [info_db_without_date]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all() 
                
            elif values[2] == 'price':
               query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units') , Products.price , func.sum(Orders.product_units).label('height')).join(Products , Orders.product_reference == Products.reference ).filter(Orders.seller_id == employee_id).group_by(Products.price).order_by(desc('total_units')).all()
   
            elif values[2] == 'category':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all() 
                
            elif values[2] == 'subcategory':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order_import':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'client':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).filter(Orders.seller_id == employee_id).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            else:
                print("ELSE [info_db_without_date]")
                query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()
        
        except Exception as e:
            print(f"[info_db_without_date]: {e}")
        
        return query
        
    
    def info_db_company_without_date(self , values):
        
        try:
            if values[2] == 'product':
                print("IF [info_db_company_without_date]")
                
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()

            elif values[2] == 'price': 
                query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units') , Products.price , func.sum(Orders.product_units).label('height')).join(Products , Orders.product_reference == Products.reference ).group_by(Products.price).order_by(desc('total_units')).all()
  
            elif values[2] == 'category':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'subcategory':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order_import':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'client':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(func.sum(Orders.product_units).desc()).all()
                
            else:
                print("ELSE [info_db_company_without_date]")
                query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()

            return query
        
        except Exception as e:
            print(f"[info_db_company]: {e}")
        
        
            
    
    
    def info_db_company(self , values):
        
        try:
            if values[2] == 'product':
                print("IF [info_db_company]")
                
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'price':
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units'),Products.price,func.sum(Orders.product_units).label('height')).join(Products, Orders.product_reference == Products.reference).filter(Orders.order_date >= '2024-05-21',Orders.order_date <= '2024-06-01').group_by(Products.price).order_by(desc('total_units')).all()
           
            elif values[2] == 'category':
                print("[category]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'subcategory':
                print("[subcategory]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order':
                print("[order]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'order_import':
                print("[order_import]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            elif values[2] == 'client':
                print("[client]")
                query = db.session.query(Orders.product_reference,func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).filter(and_(Orders.order_date > values[0] , Orders.order_date < values[1])).order_by(func.sum(Orders.product_units).desc()).all()
                
            else:
                print("ELSE [info_db_company]")
                query = db.session.query(Orders.product_reference , func.sum(Orders.product_units).label('total_units')).group_by(Orders.product_reference).order_by(desc('total_units')).all()
        
        except Exception as e:
            print(f"[info_db_company]: {e}")

        return query
        
        
        
class Graphics:
    
    def generate_graphic(self , values):  # values = [date_from , date_to , types , quantity , wich , employee_company]
        
        query = InfoDB.get_info_from_db(self, values) 
        
        self.grapics_container = CTkFrame(self.view_graphics_frame)
        self.grapics_container.grid(row = 0 , column = 0 , sticky = "nswe")
        self.grapics_container.grid_columnconfigure(0 , weight = 1)
        self.grapics_container.grid_rowconfigure(0 , weight = 1)
        
        self.grapics = CTkScrollableFrame(self.grapics_container , orientation =  'horizontal' , fg_color = 'transparent')
        self.grapics.grid(row = 0 , column = 0 , sticky = "nswe")
        self.grapics.grid_rowconfigure(2 , weight = 1)
  
        try:
            for i, product in enumerate(query[0:values[3]]): #query = db.session.query(func.sum(Orders.product_units).label('total_units') , Products.price , func.sum(Orders.product_units).label('height')).join(Products , Orders.product_reference == Products.reference ).group_by(Products.price).order_by(desc('total_units')).all()
                
                self.grapics.grid_columnconfigure(i , weight = 1)

                if len(product) > 3:
                    column_height = product[-1] / 15
                else:    
                    column_height = product[-1] / 8
                    
                print(f'Altura: {column_height}')

                units_label = CTkLabel(self.grapics , fg_color = "transparent" , text = str(product[-1]), width = 40 , corner_radius = 4)
                units_label.grid(row = 1 , column = i , sticky = "swe" , padx = 10)
                
                row = CTkFrame(self.grapics , fg_color = "DeepSkyBlue2" , height = column_height , width = 40 , corner_radius = 4)
                row.grid(row = 3 , column = i , sticky = "s" , padx = 10)
                
                label_refernce = CTkButton(self.grapics , fg_color = "Lightblue4" , text = str(product[-2]) , width = 40, corner_radius = 4 , text_color = "white" , command = lambda reference = product[-2]: DataGraphic.data_to_charge(self, reference))
                label_refernce.grid(row = 0 , column = i , padx = 10 , pady = 10 , sticky = 'swe')
                
        except Exception as e:
            print(f"[generate_graphic]: {e}")
            
    
    def get_number_of_products(self):
        
        try:
            if self.statistics_number_views.get() != "Todo":
                number_of_products = int(self.statistics_number_views.get())
                                            
            else:
                number_of_products = None
        
        except Exception as e:
            print(f"[get_number_of_products]: {e}")
            number_of_products = 10
            
        finally:
            return number_of_products
        
            
                
            
class DataGraphic:
    
    
    def data_to_charge(self , reference):
        
        try:
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
            
        except AttributeError:
            pass
        
        except Exception as e:
            print(f"[data_to_charge]{e}")
            
    
    
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
        
           
             
class StatisticsDataFrame:
    
    def totals():
        sum_total_products_sold =  db.session.query(func.sum(Orders.product_units)).scalar()
        sum_total_orders = len(db.session.query(Orders).all())
        
        return sum_total_orders , sum_total_products_sold
    
        
    def statistics_dataframe(self , e):   # DE MOMENTO NO SE USA
        
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

