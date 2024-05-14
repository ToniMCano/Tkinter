
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
        
        self.frame_tree.grid_forget()
        self.frame_company.grid_forget() 
        self.contact_frame.grid_forget()
        self.company_contact_buttons.grid_forget()
        
        self.sales_frame.grid(row = 2, column = 0, columnspan = 6 , rowspan = 2 , sticky = 'nswe')
        
        self.otra = ttk.Frame(self.sales_frame)
        self.otra.pack(fill = BOTH , expand = True)
        
        
    
    
        


    

    
        