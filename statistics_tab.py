

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
        
        try:
            self.sales_frame.grid_forget()
            
        except AttributeError as e:
            pass
        
        except Exception as e:
            print(f"[statistics_root]: {e}")
            
        
        LoadInfo.toggle_tabs(self , 'statistics') 
        
        self.statistics_frame = CTkFrame(self.main_window , fg_color = 'transparent')
        self.statistics_frame.grid(row = 2, column = 0, columnspan = 6 , rowspan = 2 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.statistics_frame.grid_columnconfigure(0 ,weight = 4)
        self.statistics_frame.grid_columnconfigure(1 ,weight = 1)
        self.statistics_frame.grid_rowconfigure(0 ,weight = 1)        
        
        self.graphics_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        self.graphics_frame.grid_columnconfigure(0, weight = 1)
        self.graphics_frame.grid_rowconfigure(0 ,weight = 1)
        
        self.view_graphics_frame  = CTkFrame(self.graphics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.view_graphics_frame.grid(row = 0 , column = 0 , sticky = 'nswe' , padx = 5 , pady = 5)
        
        self.view_data_frame = CTkScrollableFrame(self.graphics_frame)
        self.view_data_frame.grid(row = 1 , column = 0 , sticky = W+E)
        
        self.graphics_dashboard_frame  = CTkFrame(self.statistics_frame , fg_color = 'transparent' , border_width = 1 , border_color = 'gray')
        self.graphics_dashboard_frame.grid(row = 0 , column = 1 , sticky = 'nswe' , padx = 5 , pady = 5)
        
        