

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


class StatisticsTab:
    
    def statistics_root(self):
        
        self.header_one = StringVar()
        self.header_one.set("Header One")
        
        self.statistics_frame = CTkFrame(self.main_window , fg_color = 'transparent')
        
        Tabs.select_tab(self , 'statistics') 
        
        self.statistics_frame.grid(row = 2, column = 0 , rowspan = 2 , sticky = 'nswe')
        self.statistics_frame.grid_columnconfigure(0 ,weight = 1)
        #self.statistics_frame.grid_columnconfigure(1 ,weight = 1)
        self.statistics_frame.grid_rowconfigure(0 ,weight = 1)        
        
        self.graphics_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.graphics_frame.grid_columnconfigure(0, weight = 1)
        self.graphics_frame.grid_rowconfigure(0 ,weight = 1)
        
        self.view_graphics_frame  = CTkFrame(self.graphics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.view_graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        
        self.view_data_frame = CTkScrollableFrame(self.graphics_frame , fg_color = 'transparent')
        self.view_data_frame.grid(row = 1 , column = 0 , sticky = W+E)
        
        self.graphics_dashboard_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.graphics_dashboard_frame.grid(row = 0 , column = 1 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.graphics_dashboard_frame.grid_columnconfigure(0, weight = 1)
        
        self.header_one_label = CTkLabel(self.graphics_dashboard_frame , textvariable = self.header_one ,  fg_color = 'Lightblue4' ,corner_radius = 3)
        self.header_one_label.grid(row = 0 , column = 0 , sticky = W+E)
        
        self.employee = ttk.Combobox(self.graphics_dashboard_frame  ,state = "readonly", values =  LoadInfo.employees_list(True) , width= 10)
        self.employee.configure(background='lightblue')
        self.employee.grid(row = 1 , column = 0 , padx = 5 , pady = 10 , sticky = W+E)
        self.employee.bind("<<ComboboxSelected>>" , lambda e: Pops.change_employee(self ,  e))
        
        self.statistics_dates = CTkFrame(self.graphics_dashboard_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray' , width = 50)
        self.statistics_dates.grid(row = 2 , column = 0 , padx = 5 , pady = 10 , sticky = W+E) 
        
        self.statistics_calendar = CTkFrame(self.statistics_dates  , fg_color = 'red' , border_width = 1 , border_color = 'gray' , width = 50)
        self.statistics_calendar.grid(row = 2 , column = 0 , columnspan = 2 , padx = 5 , pady = 10 , sticky = W+E) 
          
        self.statistics_calendar.calendar = Calendar(self.graphics_dashboard_frame, selectedmode = "day" , date_pattern = "yyyy-mm-dd" , selectbackground = 'LightBlue4') # Para poder ordenarlo en la DB "YYYY-MM-DD"  
        self.statistics_calendar.calendar.bind("<<CalendarSelected>>", lambda e: StatisticsTab.test_calendar(self , e))
        self.statistics_calendar.calendar.bind("<Leave>", lambda e: StatisticsTab.forget_calendar(self , e))
        
        
        self.calendar_from_label = CTkLabel(self.statistics_dates , text = 'Desde:' , text_color = 'Lightblue4' , fg_color = 'transparent' , bg_color = 'transparent' , height = 10)
        self.calendar_from_label.grid(row = 0 , column = 0 , padx = 5 , pady = 5, sticky = W)

        self.calendar_from = ttk.Entry(self.statistics_dates)
        self.calendar_from.grid(row = 1 , column = 0 , padx = 5 ,pady = 5)
        self.calendar_from.insert(0 , datetime.now().strftime("%d %B %Y"))
        self.calendar_from.config(state = "disabled")
        self.calendar_from.bind("<Button-1>" , lambda e: StatisticsTab.show_calendar(self , self.calendar_from , e))
        
        self.calendar_to_label = CTkLabel(self.statistics_dates , text = 'Hasta:' , text_color = 'Lightblue4' , fg_color = 'transparent' , bg_color = 'transparent' , height = 10)
        self.calendar_to_label.grid(row = 0 , column = 1 , padx = 5 , pady = 5, sticky = W)

        self.calendar_to = ttk.Entry(self.statistics_dates)
        self.calendar_to.grid(row = 1 , column = 1 , padx = 5 ,pady = 5)
        self.calendar_to.insert(0 , datetime.now().strftime("%d %B %Y"))
        self.calendar_to.config(state = "disabled")
        self.calendar_to.bind("<Button-1>" , lambda e: StatisticsTab.show_calendar(self , self.calendar_to , e))
        
        
        
    def show_calendar(self, place , e):
        
        if place == "from":
            self.calendar_from.focus_set()
            self.statistics_calendar.calendar.place(x = 0 , y = 0)    
            
        else:
            self.calendar_to.focus_set()
            self.statistics_calendar.calendar.place(x = 0 , y = 150)  
            
        
    def forget_calendar(self , e):

        self.statistics_calendar.calendar.place_forget()
        
        
    def test_calendar(self , e):
        
        date = self.statistics_calendar.calendar.get_date() 
        
        StatisticsTab.forget_calendar(self , e)
        
        print(date)
        
        
               