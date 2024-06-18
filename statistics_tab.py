

from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs  
from statistics_actions import StatisticsActions , Graphics , StatisticsDataFrame
import tkinter as tk
from tkinter import ttk , filedialog
from tkinter import *
from tkcalendar import Calendar
from sqlalchemy import and_ , or_ , func ,asc , desc
from datetime import datetime , timedelta
from tkinter import messagebox as mb 
from customtkinter import *
import pandas as pd

generate_data_frame = [True]

class StatisticsTab:
    
    def statistics_root(self):
        
        self.header_one = StringVar()
        self.header_one.set("Header One")
        
        self.employee_company = StringVar() 
        self.employee_company.set("company")
        
        self.statistics_date_from = StringVar()
        self.statistics_date_from.set(datetime.now().strftime("%d %B %Y")) 

        self.statistics_date_to = StringVar()
        self.statistics_date_to.set(datetime.now().strftime("%d %B %Y")) 

        self.statisticts_type = StringVar()
        self.statisticts_type.set("product")

        self.statistics_product_number = StringVar()
        self.statistics_product_number.set(25)

        self.statistics_wich = StringVar()
        self.statistics_wich.set('best_seller')

        
        self.statistics_frame = CTkFrame(self.main_window , fg_color = 'transparent')
        
        Tabs.select_tab(self , 'statistics') 
        
        self.statistics_frame.grid(row = 2, column = 0 , rowspan = 2 , sticky = 'nswe')
        self.statistics_frame.grid_columnconfigure(0 ,weight = 1)
        self.statistics_frame.grid_rowconfigure(0 ,weight = 3)        
        
        self.graphics_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.graphics_frame.grid_columnconfigure(0, weight = 1)
        self.graphics_frame.grid_rowconfigure(0 ,weight = 2)
        self.graphics_frame.grid_rowconfigure(1 ,weight = 1)
        
        # GRAPHICS
        
        self.view_graphics_frame  = CTkFrame(self.graphics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.view_graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.view_graphics_frame.grid_columnconfigure(0 , weight = 1)
        self.view_graphics_frame.grid_rowconfigure(0 , weight = 1)
        
        # DATA
        
        self.frame_view_data = CTkFrame(self.graphics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.frame_view_data.grid(row = 1 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.frame_view_data.grid_columnconfigure(0, weight = 1)
        self.frame_view_data.grid_rowconfigure(1, weight = 1)
        
        self.view_data_frame = CTkFrame(self.frame_view_data , fg_color = 'transparent' , bg_color = 'transparent')
        self.view_data_frame.grid(row = 1 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.view_data_frame.grid_columnconfigure(0, weight = 1)
        self.view_data_frame.grid_rowconfigure(1, weight = 1)

        #DASHBOARD
        
        self.graphics_dashboard_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray' , width = 450)
        self.graphics_dashboard_frame.grid(row = 0 , column = 1 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.graphics_dashboard_frame.grid_columnconfigure(0, weight = 1)
        self.graphics_dashboard_frame.grid_propagate(False)
        self.graphics_dashboard_frame.grid_rowconfigure(4, weight = 1)
        
        self.header_one_label = CTkLabel(self.graphics_dashboard_frame , textvariable = self.header_one ,  fg_color = 'Lightblue4', text_color = 'white' , corner_radius = 3)
        self.header_one_label.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.statistics_employee = ttk.Combobox(self.graphics_dashboard_frame  ,state = "readonly", values =  LoadInfo.employees_list(True) , width= 10)
        self.statistics_employee.configure(background='lightblue')
        self.statistics_employee.grid(row = 1 , column = 0 , padx = 5 , pady = 10 , sticky = W+E)
        company = LoadInfo.employees_list(True).index("Company")
        self.statistics_employee.current(newindex = company)
        self.statistics_employee.bind("<<ComboboxSelected>>" , lambda e: Pops.change_employee(self ,  e))
        
        self.statistics_dates = CTkFrame(self.graphics_dashboard_frame , fg_color = 'transparent' , width = 50 , border_color = 'gray' , border_width = 1)
        self.statistics_dates.grid(row = 2 , column = 0 , padx = 5 , pady = 10 , sticky = W+E) 
        self.statistics_dates.grid_columnconfigure(0 , weight = 1)
        self.statistics_dates.grid_columnconfigure(1 , weight = 1)
          
        self.statistics_dates.calendar = Calendar(self.statistics_dates, selectedmode = "day" , date_pattern = "yyyy-mm-dd" , selectbackground = 'LightBlue4') # Para poder ordenarlo en la DB "YYYY-MM-DD"  
        self.statistics_dates.calendar.bind("<<CalendarSelected>>", lambda e: StatisticsActions.test_calendar(self , e))
        self.statistics_dates.calendar.bind("<Leave>", lambda e: StatisticsActions.forget_calendar(self , e))
        
        self.calendar_from_label = CTkLabel(self.statistics_dates , text = 'Desde:' , text_color = 'Lightblue4' , fg_color = 'transparent' , bg_color = 'transparent' , height = 10 , font = ("" , 12 , 'bold'))
        self.calendar_from_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5, sticky = W)

        self.calendar_from = CTkLabel(self.statistics_dates , textvariable = self.statistics_date_from, fg_color = 'white' , corner_radius = 4 , font = ("" , 12 , 'bold') , text_color = "gray")
        self.calendar_from.grid(row = 1 , column = 0 , padx = 5 ,pady = 5 , sticky = "we")
        self.calendar_from.bind("<Button-1>" , lambda e: StatisticsActions.show_calendar(self , "from" , e))
        
        self.calendar_to_label = CTkLabel(self.statistics_dates , text = 'Hasta:' , text_color = 'Lightblue4' , fg_color = 'transparent' , bg_color = 'transparent' , height = 10 , font = ("" , 12 , 'bold'))
        self.calendar_to_label.grid(row = 0 , column = 1 , padx = 5 , pady = 5, sticky = W)

        self.calendar_to = CTkLabel(self.statistics_dates , textvariable = self.statistics_date_to  , fg_color = 'white' , corner_radius = 4 , font = ("" , 12 , 'bold') , text_color = "gray")
        self.calendar_to.grid(row = 1 , column = 1 , padx = 5 ,pady = 5 , sticky = "we")
        self.calendar_to.bind("<Button-1>" , lambda e: StatisticsActions.show_calendar(self , "to" , e))
        
        self.date_all_frame = CTkFrame(self.statistics_dates , fg_color='lightgray' , corner_radius = 4)
        self.date_all_frame.grid(row = 3 , column = 0 , columnspan = 2 , padx = 5 , pady = 10 , sticky = W+E) 
        self.date_all_frame.grid_columnconfigure(0 , weight = 1)
        self.date_all_frame.grid_columnconfigure(1 , weight = 1)
        
        
        self.statistics_all_label = CTkLabel(self.date_all_frame , text = 'Todo' , bg_color='transparent' , width = 18 , font = ("" , 16 , 'bold') , text_color = 'Lightblue4')
        self.statistics_all_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = E) 
        
        self.statistics_dates_all = CTkCheckBox(self.date_all_frame , text = '' , bg_color='transparent' , width = 18)
        self.statistics_dates_all.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W) 
        
        self.statistics_number_views_frame = CTkFrame(self.graphics_dashboard_frame , fg_color='lightgray' , border_color = 'gray' , border_width = 1 , corner_radius = 4)
        self.statistics_number_views_frame.grid(row = 3 , column = 0 , columnspan = 2 , padx = 5 , pady = 5 , sticky = W+E) 
        self.statistics_number_views_frame.grid_columnconfigure(0 , weight = 1)
        
        self.statistics_number_views_label = CTkLabel(self.statistics_number_views_frame , text = 'Número de productos a mostrar' , bg_color='transparent' , width = 18 , font = ("" , 16 , 'bold') , text_color = 'Lightblue4')
        self.statistics_number_views_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E) 
        
        self.statistics_number_views = ttk.Combobox(self.statistics_number_views_frame , state = 'readonly' , values = [25 , 50 , 100 , 150 , 200 , "Todo"] )
        self.statistics_number_views.current(newindex = 0)
        self.statistics_number_views.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = W+E) 
        self.statistics_number_views.configure(background='lightblue')
        self.statistics_number_views.bind("<<ComboboxSelected>>" , lambda e: StatisticsDataFrame.statistics_dataframe(self , e))
        
        ## SELECTIONS
        
        self.statistics_types = CTkFrame(self.graphics_dashboard_frame , fg_color = 'transparent' , width = 50)
        self.statistics_types.grid(row = 4 , column = 0 , padx = 5 , pady = 10 , sticky = 'nswe') 
        self.statistics_types.grid_columnconfigure(0 , weight = 1)
        self.statistics_types.grid_rowconfigure(0 , weight = 1)
        self.statistics_types.grid_rowconfigure(1 , weight = 1)
        self.statistics_types.grid_rowconfigure(2 , weight = 1)
        self.statistics_types.grid_rowconfigure(3 , weight = 1)
        self.statistics_types.grid_rowconfigure(4 , weight = 1)
        self.statistics_types.grid_rowconfigure(5 , weight = 1)
        self.statistics_types.grid_rowconfigure(6 , weight = 1)
        self.statistics_types.grid_rowconfigure(7 , weight = 1)
        self.statistics_types.grid_rowconfigure(8 , weight = 1)
                                                    
        #self.statistics_types.grid_columnconfigure(1 , weight = 1)
        
        self.products = CTkButton(self.statistics_types , text = "Productos" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.products.grid(row = 0 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.price = CTkButton(self.statistics_types , text = "Precio" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.price.grid(row = 1 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.category = CTkButton(self.statistics_types , text = "Categoría" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.category.grid(row = 2 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.subcategory = CTkButton(self.statistics_types , text = "Subcategoría" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.subcategory.grid(row = 3 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.orders = CTkButton(self.statistics_types , text = "Pedidos" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.orders.grid(row = 4 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.orders_import = CTkButton(self.statistics_types , text = "Importe Pedido" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.orders_import.grid(row = 5 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.client = CTkButton(self.statistics_types , text = "Cliente" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.client.grid(row = 6 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.clients = CTkButton(self.statistics_types , text = "Clientes (Todos)" , fg_color = "Lightblue4" , text_color = 'white' , font = ("" , 16 , 'bold'))
        self.clients.grid(row = 7 , column = 0 , sticky =  'nswe' , padx = 1 , pady = 1)
        
        self.statistics_radiobuttons = CTkFrame(self.graphics_dashboard_frame)
        self.statistics_radiobuttons.grid(row = 5 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5) 
        self.statistics_radiobuttons.grid_columnconfigure(0 , weight = 1)
        self.statistics_radiobuttons.grid_columnconfigure(1 , weight = 1)
        self.statistics_radiobuttons.grid_columnconfigure(2 , weight = 1)

        self.more = CTkCheckBox(self.statistics_radiobuttons , text = 'Más Vendidos' , checkbox_height = 15 , checkbox_width = 15)
        self.more.grid(row = 0 , column = 1 , sticky =  W+E , pady = 10)

        self.less = CTkCheckBox(self.statistics_radiobuttons , text = 'Menos Vendidos' , checkbox_height = 15 , checkbox_width = 15)
        self.less.grid(row = 0 , column = 2 , sticky =  W+E , pady = 10)
        
        self.All = CTkCheckBox(self.statistics_radiobuttons , text = 'Todos' , checkbox_height = 15 , checkbox_width = 15)
        self.All.grid(row = 0 , column = 3 , sticky =  W+E , pady = 10)

        self.calculate_button = CTkButton(self.graphics_dashboard_frame , text = "Mostrar" , fg_color = "white" , corner_radius = 4 , border_color = 'Lightblue4' , border_width = 5 , text_color = 'Lightblue4' , font = ("" , 14 , 'bold') , height = 25 , command = lambda: Graphics.example(self))
        self.calculate_button.grid(row = 6 , column = 0 , pady = 10 , sticky =  W+E , padx = 50)
                
    
    
        
        
    
        
        

