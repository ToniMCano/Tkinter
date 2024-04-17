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
from datetime import datetime
import locale
from tkinter import messagebox as mb
import os
locale.setlocale(locale.LC_ALL, '')


company_name , contact_name , contact_surname , contact_job = "UnaEmpresa" , "Pepito" , "Grillo" , "Mamporrero"

def show_new_company(company_name , contact_name , contact_surname , contact_job):
        
    show = Toplevel()
    show.title("Se ha creado una nueva Empresa") 
    show.resizable(0,0)

    
    frame = LabelFrame(show , text = "Nueva Empresa" , labelanchor = 'n')
    frame.grid(row = 0 , column =0 , columnspan = 2 , padx = 20 , pady = 10 , sticky = W+E)
    message = Label(frame ,  text= 
    f"""
    Empresa:
    {company_name}

    Persona de Contacto: 
    {contact_name} {contact_surname} 
    
    Cargo
    {contact_job}
    """ , justify = 'left')
    message.grid(row = 0 , column =0 , columnspan = 2 ,  sticky = W+E)
    
    show_button = ttk.Button(show , text = "Ver Empresa" , width = 20)
    show_button.grid(row = 1 , column = 0 , padx = 10 , pady = 10 , sticky = W+E)
    
    continue_button = ttk.Button(show , text = "Continuar" , width = 20)
    continue_button.grid(row = 1 , column = 1 , padx = 10 , pady = 10 , sticky = W+E)



root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

# Llamar a las funciones para mostrar las ventanas
show_new_company(company_name, contact_name, contact_surname, contact_job)

# Iniciar el bucle principal de tkinter
root.mainloop()