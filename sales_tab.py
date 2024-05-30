from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs 
from sales_actions import OrderFunctions , ModifyDeleteOrder
import tkinter as tk
from tkinter import ttk , filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
from models import Employee , Client , Contact , ContactPerson , Products , Orders
import db
from sqlalchemy import and_ , or_ , func ,asc , desc
from datetime import datetime , timedelta
from tkinter import messagebox as mb
from customtkinter import *
import pandas as pd



class SalesTab:
    
    def sales_root(self):

        self.main_window.update()
        
        self.sales_frame = ttk.Frame(self.main_window)  
        
        Tabs.select_tab(self , 'sales')
        
        self.sales_frame.grid(row = 2, column = 0 , rowspan = 2 , sticky = 'nswe')
        self.sales_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_frame.grid_rowconfigure(1 , weight = 1)
        
        self.order_header = StringVar()
        self.order_header.set('Pedido')
        
        self.header_description = StringVar()
        self.header_description.set('Descripción Producto')
            
        self.description = StringVar() 
        
        self.expiration = StringVar()
        
        self.product_units = StringVar()
        
        self.add_units_button_text = StringVar()
        self.add_units_button_text.set('Añadir')
        
        self.order_import = StringVar() 
               
        self.discount = StringVar()    
        
        self.total_order_import = StringVar() 
        
        self.delivery_date_text = StringVar()
        
        self.delivery_date_text.set(MyCalendar.format_date_to_show(str(datetime.now() + timedelta(days = 2))[:16])[:-5])
        
        # HEADER 
        
        self.sales_header = CTkFrame(self.sales_frame , fg_color = 'transparent' , height = 50 , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_header.grid(row = 0 , column = 0 , columnspan = 2 , sticky = W+E, padx = 3 , pady = 3)
        
        # CONTENT
        
        self.sales_content_frame = CTkFrame(self.sales_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.sales_content_frame.grid(row = 1 , column = 0 , sticky = 'nswe')
        self.sales_content_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_content_frame.grid_rowconfigure(0, weight = 1)
        
        #self.sales_content_frame.grid_rowconfigure(1 , weight = 1)
        
        self.products_frame = CTkFrame(self.sales_content_frame , bg_color='transparent')
        self.products_frame.grid(row = 0 , column =  0 , rowspan=2 , sticky = 'nswe')
        self.products_frame.grid_columnconfigure(0 , weight = 1)
        self.products_frame.grid_rowconfigure(0 , weight = 1)
        
        self.products_tree = ttk.Treeview(self.products_frame , style="mystyle.Treeview" )
        self.products_tree.grid(row = 0 , column = 0 ,  sticky = 'nsew')
        
        scrollbar = ttk.Scrollbar(self.products_frame, orient="vertical", command=self.products_tree.yview)
        scrollbar.grid(row = 0, column = 1 , sticky = "ns")
        self.products_tree.configure(yscroll=scrollbar.set)
               
        self.products_tree["columns"] = ( "#0" , "#1" , "#2" , "#3" ,  "#4")
        self.products_tree.heading("#0" , text = "Referencia" , command = lambda: OrderFunctions.show_products(self , "reference"))
        self.products_tree.heading("#1" , text = "Nombre" , command = lambda: OrderFunctions.show_products(self , "name"))
        self.products_tree.heading("#2" , text  ="Precio" , command = lambda: OrderFunctions.show_products(self , "price"))
        self.products_tree.heading("#3" , text = "Stock" , command = lambda: OrderFunctions.show_products(self , "stock"))
        self.products_tree.heading("#4" , text = "Categoría" , command = lambda: OrderFunctions.show_products(self , "category"))
        self.products_tree.heading("#5" , text = "Subcategoría" , command = lambda: OrderFunctions.show_products(self , "subcategory"))
        
        self.products_tree.column("#0" , width = 40 , anchor="center")  
        self.products_tree.column("#1" , width = 220 , anchor="center")
        self.products_tree.column("#2" , width = 25)
        self.products_tree.column("#3" , width = 25 , anchor="center")
        self.products_tree.column("#4" , width = 80 , anchor="w")
        self.products_tree.column("#5" , width = 80 , anchor="w")
        self.products_tree.bind("<ButtonRelease-1>" , lambda event: OrderFunctions.get_product(self , "products" , event))       
                
        OrderFunctions.show_products(self)
        
        self.product_description_label = CTkLabel(self.sales_content_frame , textvariable = self.header_description , fg_color = 'Lightblue4' , corner_radius = 3 , text_color = "white")
        self.product_description_label.grid(row = 2 , column = 0 , sticky = W+E)
        
        self.product_description_frame = CTkScrollableFrame(self.sales_content_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.product_description_frame.grid(row = 3 , column =  0, sticky = 'nswe', padx = 3 , pady = 3)
        self.product_description_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_content_frame.grid_rowconfigure(1 , weight=1)
        
        self.product_description = Text(self.product_description_frame , wrap = WORD  )
        self.product_description.grid(row =0 , column = 0 , padx = 5 , pady = 5 , sticky = 'we')
        
        self.product_expiration = CTkLabel(self.product_description_frame , textvariable = self.expiration , text_color = 'white' , fg_color = "Lightblue4" , width = 10 , corner_radius = 3 , )
        self.product_expiration.grid(row =1 , column = 0 , padx = 5 , pady = 5 , sticky = 'w')
        
        #ORDER
        
        self.sales_order_frame = CTkFrame(self.sales_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_frame.grid(row = 1 , column = 1 , sticky = 'nswe', rowspan = 3 , padx = 3 , pady = 3)
        self.sales_order_frame.grid_rowconfigure(1 , weight = 1)
        
        self.order_label = CTkLabel(self.sales_order_frame , textvariable = self.order_header , fg_color = 'Lightblue4' , corner_radius = 3 , text_color = "white")
        self.order_label.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.sales_oreder_view = ttk.Frame(self.sales_order_frame)
        self.sales_oreder_view.grid(row = 1 , column = 0 , sticky = 'nswe', padx = 5 , pady = 5)
        self.sales_oreder_view.grid_columnconfigure(0 , weight = 1)
        self.sales_oreder_view.grid_rowconfigure(0 , weight = 1)
        
        self.order_tree = ttk.Treeview(self.sales_oreder_view , style="mystyle.Treeview")
        self.order_tree.grid(row = 0 , column = 0 , sticky = 'nsew')
        
        order_scrollbar = ttk.Scrollbar(self.sales_oreder_view , orient="vertical", command=self.order_tree.yview)
        order_scrollbar.grid(row = 0, column = 1 , sticky = "ns")
        self.order_tree.configure(yscroll=order_scrollbar.set)
        
        self.order_tree["columns"] = ( "#0" , "#1" , "#2" , "#3" , "#4")
        self.order_tree.heading("#0" , text = "Referencia" , command = lambda: LoadInfo.on_heading_click(self , "state"))
        self.order_tree.heading("#1" , text = "Nombre" , command = lambda: LoadInfo.on_heading_click(self , "days"))
        self.order_tree.heading("#2" , text  ="Precio" , command = lambda: LoadInfo.on_heading_click(self , "client"))
        self.order_tree.heading("#3" , text = "Unidades" , command = lambda: LoadInfo.on_heading_click(self , "last"))
        self.order_tree.heading("#4" , text = "Descuento" , command = lambda: LoadInfo.on_heading_click(self , "last"))
        self.order_tree.heading("#5" , text = "Importe" , command = lambda: LoadInfo.on_heading_click(self , "last"))
        
        self.order_tree.column("#0" , width = 80 , anchor="center")  
        self.order_tree.column("#1" , width = 80 , anchor="center")
        self.order_tree.column("#2" , width = 40)
        self.order_tree.column("#3" , width = 40 , anchor="center")
        self.order_tree.column("#4" , width = 40 , anchor="w")
        self.order_tree.column("#5" , width = 40 , anchor="w")
        
        self.order_tree.bind("<ButtonRelease-1>" , lambda event: ModifyDeleteOrder.focus_product_list(self , event))
        
        
        OrderFunctions.show_products(self)
        
        #ORDER DASHBOARD
        
        self.sales_order_dashboard = CTkFrame(self.sales_order_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_dashboard.grid(row = 2 , column = 0 , sticky = 'nswe', padx = 5)
        
        self.product_units_entry = CTkLabel(self.sales_order_dashboard , text = "Unidades: " , text_color = 'gray' , width = 30)
        self.product_units_entry.grid(row = 0 , column = 0 , sticky = W , padx = 5 , pady = 5)
        
        self.product_units_entry = CTkEntry(self.sales_order_dashboard , textvariable = self.product_units , corner_radius = 4 , fg_color = '#f4f4f4' , height = 15 , text_color = 'gray' , border_width = 2 , border_color = "Lightblue4" , width = 35)
        self.product_units_entry.grid(row = 0 , column = 0 , sticky = E , padx = 5 , pady = 5)
        self.product_units_entry .focus()
        #Añadir
        self.add_units_button = CTkButton(self.sales_order_dashboard , textvariable = self.add_units_button_text , corner_radius = 2 , fg_color = 'Lightblue4' , height = 15 , text_color = 'white' , width = 50 , command = lambda: OrderFunctions.get_product(self , 'order' , ""))
        self.add_units_button.grid(row = 0 , column = 1 , sticky = W+E , padx = 5 , pady = 5)
        
        self.delete_button = CTkButton(self.sales_order_dashboard , text = 'Eliminar' , corner_radius = 2 , fg_color = '#f4f4f4' , height = 15 , text_color = 'gray' , border_width = 1 , border_color = "gray" , width = 50 , command = lambda: ModifyDeleteOrder.delete_product(self))
        self.delete_button.grid(row = 0 , column = 2 , sticky = W+E , padx = 5 , pady = 5)
        
        self.send_order = CTkButton(self.sales_order_dashboard , text = 'Realizar Pedido' , corner_radius = 2 , fg_color = '#f4f4f4' , height = 15 , text_color = 'Lightblue4' , border_width = 2 , border_color = "Lightblue4" , width = 50 , command = lambda: OrderFunctions.send_order(self))
        self.send_order.grid(row = 0 , column = 3 , sticky = W+E , padx = 5 , pady = 5)
        
        self.sales_order_info = CTkFrame(self.sales_order_dashboard , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_info.grid(row = 1 , column = 0 , columnspan = 4 , sticky = 'nswe', padx = 5 , pady = 5)
        
        self.sales_order_info.grid_columnconfigure(0 , weight = 1)
        self.sales_order_info.grid_columnconfigure(1 , weight = 1)
        self.sales_order_info.grid_columnconfigure(2 , weight = 1)
        
        self.import_frame = CTkFrame(self.sales_order_info , fg_color = "transparent")
        self.import_frame.grid(row = 0 , column = 0 ,  sticky = W+E , padx = 10 , pady = 10 )
        
        self.order_import_label = CTkLabel(self.import_frame , text = "Importe" , anchor = 'w' , text_color = 'gray')
        self.order_import_label.grid(row = 0 , column = 0 ,  sticky = W+E , padx = 5 , pady = 5)
        
        self.order_import_info = CTkEntry(self.import_frame , textvariable = self.order_import , fg_color = 'transparent' , state = 'disabled' , text_color = 'gray' , border_color = "Lightblue4" , width = 120)
        self.order_import_info.grid(row = 1 , column = 0 , sticky = W+E , padx = 5 , pady = 5)
        
        self.euro_label = CTkLabel(self.import_frame , text = '€' , fg_color = 'transparent' , state = 'disabled' , text_color = 'gray')
        self.euro_label.grid(row = 1 , column = 1 , sticky = W , padx = 5 , pady = 5)
        
        self.discount_frame = CTkFrame(self.sales_order_info , fg_color = "transparent")
        self.discount_frame.grid(row = 0 , column = 1 ,  sticky = W+E , padx = 10 , pady = 10)
                
        self.discount_label = CTkLabel(self.discount_frame , text = 'Descuento' , anchor = 'w' , text_color = 'gray')
        self.discount_label.grid(row = 0 , column = 0 ,  sticky = W+E , padx = 5 , pady = 5)
                
        self.discount_info = CTkEntry(self.discount_frame , textvariable = self.discount , fg_color = 'transparent' , text_color = 'gray' , border_color = "Lightblue4" , width = 60)
        self.discount_info.focus_set()
        self.discount_info.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = W )
        self.discount_info.bind("<Return>" , lambda e: OrderFunctions.calculate_import(self , e))
        
        self.percentage_label = CTkLabel(self.discount_frame , text = '%' , fg_color = 'transparent' , state = 'disabled' , text_color = 'gray' )
        self.percentage_label.grid(row = 1 , column = 1 , sticky = W , padx = 5 , pady = 5)
        
        self.total_import_frame = CTkFrame(self.sales_order_info , fg_color = "transparent")
        self.total_import_frame.grid(row = 0 , column = 2 ,  sticky = W+E , padx = 10 , pady = 10)
        
        self.total_import_label = CTkLabel(self.total_import_frame , text = "Total (IVA Incl.)" , anchor = 'w' , text_color = 'gray')
        self.total_import_label.grid(row = 0 , column = 0  ,  sticky = W+E , padx = 5 , pady = 5)
                
        self.total_import_info = CTkEntry(self.total_import_frame , textvariable = self.total_order_import , fg_color = 'transparent' , state = 'disabled' , text_color = 'gray' , border_color = "Lightblue4" , width = 120)
        self.total_import_info.grid(row = 1 , column = 0 , padx = 5 , pady = 5)
        
        self.euro2_label = CTkLabel(self.total_import_frame , text = '€' , fg_color = 'transparent' , state = 'disabled' , text_color = 'gray')
        self.euro2_label.grid(row = 1 , column = 1 , sticky = W , padx = 5 , pady = 5)
        
        self.aditional_order_info = CTkFrame(self.sales_order_dashboard , fg_color = "lightgray")
        self.aditional_order_info.grid(row = 2 , column = 0 , columnspan = 4 ,  sticky = W+E , padx = 10 , pady = 10)
        
        self.oreder_notes = Text(self.aditional_order_info , wrap = 'word' , height = 5 , width = 55)
        self.oreder_notes.grid(row = 0 , column = 0 , sticky = 'nswe', padx = 10 , pady = 10)
        
        # FECHA DE ENTREGA (Se podrá elegir en el futuro)
        
        self.delivery_date_frame = CTkFrame(self.sales_order_dashboard , fg_color = "lightgray", height = 30)
        self.delivery_date_frame.grid(row = 3 , column = 0 , columnspan = 4 ,  sticky = W+E , padx = 10 , pady = 10)
        self.delivery_date_frame.grid_columnconfigure(3, weight = 1)

        
        self.delivery_date_label = CTkLabel(self.delivery_date_frame , text = "Fecha de Entrega: " , anchor = 'w' , text_color = 'gray')
        self.delivery_date_label.grid(row = 0 , column = 0  ,  sticky = W , padx = 5 , pady = 5)
                
        self.delivery_date = CTkLabel(self.delivery_date_frame , textvariable = self.delivery_date_text , anchor = 'w' , text_color = 'gray')
        self.delivery_date.grid(row = 0 , column = 1  ,  sticky = W , padx = 5 , pady = 5)
        
        self.historical_button = CTkButton(self.delivery_date_frame , text = "Historial" , height = 2 , fg_color = "LightBlue4" , text_color = 'white' ,  hover_color = 'LightBlue4' , command = lambda: OrderFunctions.sales_historical(self) , corner_radius = 4)
        self.historical_button.grid(row = 0 , column = 3 , sticky = "e" , pady = 5 , padx = 5)
        