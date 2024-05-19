# REVISAR
# toggle_view

from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs
from sales_actions import ProductsClass , LoadProducts
import tkinter as tk
from tkinter import ttk , messagebox
from tkinter import *
from ttkthemes import ThemedTk
from customtkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
import webbrowser
from models import Employee , Client , Contact , ContactPerson
import db
import openpyxl
from sqlalchemy import and_ , or_  
from datetime import datetime , timedelta


class SalesTab:
    
    def sales_root(self):
        
        LoadInfo.combo_state_values(self , 'sales')
        
        self.ventana_principal.update()
        
        self.sales_frame.grid(row = 2, column = 0, columnspan = 6 , rowspan = 2 , sticky = 'nswe')
        self.sales_frame.grid_columnconfigure(0 , weight = 6)
        #self.sales_frame.grid_columnconfigure(1 , weight = 2)
        self.sales_frame.grid_rowconfigure(1 , weight = 1)
        
        
        
        self.description = StringVar() 
        self.description.set('Descripción Producto') # Será el nombre del producto seleccionado
        
        self.order_import = StringVar() 
        self.order_import.set('215')
        
        self.discount = StringVar()
        self.discount.set('10')        
        
        self.total_order_import = StringVar() 
        self.total_order_import.set('238') 
                       
        self.sales_header = CTkFrame(self.sales_frame , fg_color = 'transparent' , height = 50 , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_header.grid(row = 0 , column = 0 , columnspan = 2 , sticky = W+E, padx = 3 , pady = 3)
        
        self.sales_content_frame = CTkFrame(self.sales_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.sales_content_frame.grid(row = 1 , column = 0 , sticky = 'nswe')
        self.sales_content_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_content_frame.grid_rowconfigure(0 , weight = 1)
        
        self.products_frame = CTkFrame(self.sales_content_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.products_frame.grid(row = 0 , column =  0, sticky = 'nswe')
        self.products_frame.grid_columnconfigure(0 , weight = 1)
        
        self.products_tree = ttk.Treeview(self.products_frame, height = 15 , style="mystyle.Treeview")
        self.products_tree.grid(row = 0 , column = 0 , sticky = 'nsew')
        
        scrollbar = ttk.Scrollbar(self.products_frame, orient="vertical", command=self.products_tree.yview)
        scrollbar.grid(row = 0, column = 1 , sticky = "ns")
        self.products_tree.configure(yscroll=scrollbar.set)
        
        self.products_tree["columns"] = ( "#0" , "#1" , "#2" , "#3" ,  "#4")
        self.products_tree.heading("#0" , text = "Referencia" , command = lambda: LoadInfo.on_heading_click(self , "state"))
        self.products_tree.heading("#1" , text = "Nombre" , command = lambda: LoadInfo.on_heading_click(self , "days"))
        self.products_tree.heading("#2" , text  ="Precio" , command = lambda: LoadInfo.on_heading_click(self , "client"))
        self.products_tree.heading("#3" , text = "Stock" , command = lambda: LoadInfo.on_heading_click(self , "last"))
        self.products_tree.heading("#4" , text = "Categoría" , command = lambda: LoadInfo.on_heading_click(self , "next"))
        self.products_tree.heading("#5" , text = "Subcategoría" , command = lambda: LoadInfo.on_heading_click(self , "postal_code"))
        
        self.products_tree.column("#0" , width = 40 , anchor="center")  
        self.products_tree.column("#1" , width = 220 , anchor="center")
        self.products_tree.column("#2" , width = 25)
        self.products_tree.column("#3" , width = 25 , anchor="center")
        self.products_tree.column("#4" , width = 80 , anchor="w")
        self.products_tree.column("#5" , width = 80 , anchor="w")
        self.products_tree.bind("<ButtonRelease-1>" , lambda event: LoadProducts.get_product(self , event))
        
        
        ProductsClass.prdoducts_dataframe(self)
        
        self.product_description_label = CTkLabel(self.sales_content_frame , textvariable = self.description , fg_color = 'Lightblue4' , corner_radius = 3)
        self.product_description_label.grid(row = 2 , column = 0 , sticky = W+E)
        
        self.product_description_frame = CTkScrollableFrame(self.sales_content_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.product_description_frame.grid(row = 3 , column =  0, sticky = 'nswe', padx = 3 , pady = 3)
        self.product_description_frame.grid_columnconfigure(0 , weight = 1)
        
        self.sales_order_frame = CTkFrame(self.sales_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_frame.grid(row = 1 , column = 1 , sticky = 'nswe', rowspan = 3 , padx = 3 , pady = 3)
        #   self.sales_order_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_order_frame.grid_rowconfigure(1 , weight = 1)
        
        self.order_label = CTkLabel(self.sales_order_frame , text = 'Pedido' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.order_label.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.sales_oreder_view = CTkScrollableFrame(self.sales_order_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' , width = 450)
        self.sales_oreder_view.grid(row = 1 , column = 0 , sticky = 'nswe', padx = 5 , pady = 5)
        
        self.sales_order_dashboard = CTkFrame(self.sales_order_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_dashboard.grid(row = 2 , column = 0 , sticky = 'nswe', padx = 5)
        
        self.sales_order_dashboard.grid_columnconfigure(0 , weight = 1)
        self.sales_order_dashboard.grid_columnconfigure(1 , weight = 1)
        self.sales_order_dashboard.grid_columnconfigure(2 , weight = 1)
        
        self.delete_button = CTkButton(self.sales_order_dashboard , text = 'Eliminar' , corner_radius = 2 , fg_color = '#f4f4f4' , height = 15 , text_color = 'gray' , border_width = 1 , border_color = "gray")
        self.delete_button.grid(row = 0 , column = 0 , sticky = W+E , padx = 5 , pady = 5)
        
        self.refresh_button = CTkButton(self.sales_order_dashboard , text = 'Button' , corner_radius = 2 , fg_color = '#f4f4f4' , height = 15 , text_color = 'gray' , border_width = 1 , border_color = "gray")
        self.refresh_button.grid(row = 0 , column = 1 , sticky = W+E , padx = 5 , pady = 5)
        
        self.delete_button = CTkButton(self.sales_order_dashboard , text = 'Terminar' , corner_radius = 2 , fg_color = '#f4f4f4' , height = 15 , text_color = 'gray' , border_width = 1 , border_color = "gray")
        self.delete_button.grid(row = 0 , column = 2 , sticky = W+E , padx = 5 , pady = 5)
        
        self.sales_order_info = CTkFrame(self.sales_order_dashboard , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_info.grid(row = 1 , column = 0 , columnspan = 3 , sticky = 'nswe', padx = 5 , pady = 5)
        
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
        self.aditional_order_info.grid(row = 2 , column = 0 , columnspan = 3 ,  sticky = W+E , padx = 10 , pady = 10)
        
        self.delivery_date_frame = CTkFrame(self.sales_order_dashboard , fg_color = "lightgray", height = 30)
        self.delivery_date_frame.grid(row = 3 , column = 0 , columnspan = 3 ,  sticky = W+E , padx = 10 , pady = 10)
        
        self.delivery_date_label = CTkLabel(self.delivery_date_frame , text = "Fecha de Entrega: " , anchor = 'w' , text_color = 'gray')
        self.delivery_date_label.grid(row = 0 , column = 0  ,  sticky = W+E , padx = 5 , pady = 5)
                
        self.delivery_date = CTkLabel(self.delivery_date_frame , text = "Martes 15 de Junio" , anchor = 'w' , text_color = 'gray')
        self.delivery_date.grid(row = 0 , column = 1  ,  sticky = W+E , padx = 5 , pady = 5)
                
        
        
 
        
        
        
        
        

    

    
        