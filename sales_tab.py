# REVISAR
# toggle_view

from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs
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
        self.sales_frame.grid_columnconfigure(1 , weight = 3)
        self.sales_frame.grid_rowconfigure(1 , weight = 1)
        
        self.description = StringVar() 
        self.description.set('Descripción Producto') # Será el nombre del producto seleccionado
        
                       
        self.sales_header = CTkFrame(self.sales_frame , fg_color = 'transparent' , height = 50 , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_header.grid(row = 0 , column = 0 , columnspan = 2 , sticky = W+E, padx = 3 , pady = 3)
        
        self.sales_content_frame = CTkScrollableFrame(self.sales_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.sales_content_frame.grid(row = 1 , column = 0 , sticky = 'nswe', padx = 3 , pady = 3)
        
        self.sales_order_frame = CTkFrame(self.sales_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_frame.grid(row = 1 , column = 1 , sticky = 'nswe', rowspan = 3 , padx = 3 , pady = 3)
        self.sales_order_frame.grid_columnconfigure(0 , weight = 1)
        self.sales_order_frame.grid_rowconfigure(1 , weight = 1)
        
        self.order_label = CTkLabel(self.sales_order_frame , text = 'Pedido' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.order_label.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.sales_oreder_view = CTkScrollableFrame(self.sales_order_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.sales_oreder_view.grid(row = 1 , column = 0 , sticky = 'nswe', padx = 5 , pady = 5)
        
        self.sales_order_dashboard = CTkFrame(self.sales_order_frame , fg_color = 'transparent' , corner_radius = 3 , border_width = 1 , border_color = 'lightgray')
        self.sales_order_dashboard.grid(row = 2 , column = 0 , sticky = 'nswe', padx = 5)
        
        self.product_description_label = CTkLabel(self.sales_frame , textvariable = self.description , fg_color = 'Lightblue4' , corner_radius = 3)
        self.product_description_label.grid(row = 2 , column = 0 , sticky = W+E)
        
        self.product_description_frame = CTkScrollableFrame(self.sales_frame , corner_radius = 3 , border_width = 1 , border_color = 'lightgray' , fg_color = 'transparent' )
        self.product_description_frame.grid(row = 3 , column =  0, sticky = 'nswe', padx = 3 , pady = 3)
        self.product_description_frame.grid_columnconfigure(0 , weight = 1)
        
        
        
        
        

    

    
        