from actions import LoadInfo , GetInfo , MyCalendar , Pops , Alerts , AddInfo , Logs , Update , Tabs
import tkinter as tk
from tkinter import ttk , filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
from models import Employee , Client , Contact , ContactPerson , Products
import db
import openpyxl
from sqlalchemy import and_ , or_ , func ,asc , desc
from datetime import datetime , timedelta
from tkinter import messagebox as mb
from sqlalchemy.exc import IntegrityError , SQLAlchemyError 
from customtkinter import *
import pandas as pd



class ProductsClass:
    
    def prdoducts_dataframe(self): 
        
        self.products_tree.tag_configure("odd", background="snow2" )
        self.products_tree.tag_configure("even", background="white")
        self.products_tree.tag_configure("font_red", foreground="red")
        self.products_tree.tag_configure("font_green", foreground="green")
        
        try:
            clean = self.products_tree.get_children()
            
            for x in clean: 
                self.products_tree.delete(x)
                        
        except Exception as e:
            print("[prdoducts_dataframe]: (Clean): " , e)

        products = db.session.query(Products).order_by(Products.category).all()
        
        for i , product in enumerate(products):
            font = ""
            
            if product.units == 0:
                font = 'font_red'
                
            self.products_tree.insert("" , 0 , text = product.reference , values = (product.product_name , product.price , product.units , product.category , product.subcategory) , tags=(font))

        
    def row_colors(self, clients , ordenado , date , bgcolor , contacts , dot):
        for i , client in enumerate(clients):

            if ordenado.at[i, 'next'] <= str(date)[:11] + "23:59":               
                
                if int(ordenado.at[i, "days"]) >= 60:
                    font = "font_red"
                    
                else:
                    font = ""
                
                if bgcolor % 2 == 0:
                    color= "odd"
                
                else:
                    color= "even"
                #print(ordenado.at[i, 'pop'])
                if ordenado.at[i, 'pop'] == True:
                    next_contact = f"{MyCalendar.format_date_to_show(ordenado.at[i, 'next'])} {dot}"
                
                else:
                    next_contact = f"{MyCalendar.format_date_to_show(ordenado.at[i, 'next'])}"
                    
                if len(str(ordenado.at[i, 'cp'])) == 4:
                    postal_code = f"0{ordenado.at[i, 'cp']}"
                    
                else:
                    postal_code = ordenado.at[i, 'cp']
                    
                self.infoproducts_tree.insert("" , 0 , text = ordenado.at[i, 'state'] , values = (str(ordenado.at[i, 'days']).lstrip("0") , ordenado.at[i, 'name'] , MyCalendar.format_date_to_show(ordenado.at[i, 'last'])  , next_contact , postal_code) , tags=(color, font) )
                
                contacts += 1
                bgcolor += 1
                
        return contacts
    
    
class LoadProducts:
    
    def get_product(self , e):
        
        reference , name = LoadInfo.get_item(self , "products" , self.products_tree , e)
        self.description.set(f"[{reference}] {name}")
        
        
        