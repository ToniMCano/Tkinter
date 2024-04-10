import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
import webbrowser
from models import Employee , Client , Contact , ContactPerson
import db
import openpyxl
from sqlalchemy import and_ , or_   


 
class Actions:
    
    def login(window):
            
            login = Toplevel()
            login.title("Login")
            #login.geometry("300x200")
            
            login.grid_columnconfigure(0 , weight = 1)
            #login.grid_rowconfigure(0 , weight = 1)
            
            frame = ttk.Labelframe(login , text = "Login")
            frame.grid(row = 0 , column = 0 , padx = 10 , pady = 5 , sticky = "we")
            frame.grid_columnconfigure(1, weight = 1)        
            
            employee_alias = ttk.Label(frame, text = "Employee: ")
            employee_alias.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = "w")
            
            employee_alias_entry = ttk.Entry(frame)
            employee_alias_entry.grid(row = 0 , column = 1 , padx = 5 , pady = 10 , sticky = W+E)
            
            employee_password = ttk.Label(frame, text = "Password: ")
            employee_password.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = "w")
            
            employee_password_entry = ttk.Entry(frame)
            employee_password_entry.grid(row =1 , column = 1 , padx = 5 , pady = 10 , sticky = W+E)
            
            log_button = ttk.Button(login , text = "Login")
            log_button.grid(row = 1 , column = 0 , padx = 10 , pady = 10)
            
            window.center_window(login)