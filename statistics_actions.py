

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