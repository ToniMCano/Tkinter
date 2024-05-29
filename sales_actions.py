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



class OrderFunctions:
    
    def show_products(self , selected = 'reference'): 
        
        self.products_tree.tag_configure("odd", background="snow2" )
        self.products_tree.tag_configure("even", background="white")
        self.products_tree.tag_configure("font_red", foreground="red")
        self.products_tree.tag_configure("font_green", foreground="green")
        self.products_tree.tag_configure("font_orange", foreground="Darkorange3")
        
        try:
            clean = self.products_tree.get_children()
            
            for x in clean: 
                self.products_tree.delete(x)
                        
        except Exception as e:
            print("[show_products]: (Clean): " , e)

        if selected == 'reference':
            products = db.session.query(Products).order_by(Products.reference).all()
            
        elif selected =="name":
            products = db.session.query(Products).order_by(Products.product_name).all()
            
        elif selected =="stock":
            products = db.session.query(Products).order_by(Products.units).all()
            
        elif selected =="category":
            products = db.session.query(Products).order_by(Products.category).all()
            
        elif selected =="subcategory":
            products = db.session.query(Products).order_by(Products.subcategory).all()
            
        elif selected =="price":
            products = db.session.query(Products).order_by(Products.price).all()
        
        for i , product in enumerate(products):
            font = ""
            
            if product.units == 0:
                font = 'font_red'
                
            elif product.units < 25:
                
                font = "font_orange"
                
            elif product.discount > 0:
                font = "font_green"
                
            self.products_tree.insert("" , 0 , text = product.reference , values = (product.product_name , product.price , product.units , product.category , product.subcategory) , tags=(font))

        try:
            client = db.session.get(Client , self.company_id.get())
            
            if client is not None:
                self.order_header.set(f'[{client.id_client}] {client.name}')
                                
            else:
                self.order_header.set('Pedido')
            
        except Exception as e:
            print(f'[show_products] (order_header): {e}')
            
        
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
    
    
    def get_product(self , place , e):

        try:
            reference = LoadInfo.get_item(self , "products" , self.products_tree , e)
            print(reference)
            product = db.session.query(Products).filter(Products.reference == reference).first()
            
            OrderFunctions.load_product(self , product)
            
            if place == "order":
                OrderFunctions.add_product(self , product)                
            
        except Exception as e:
            print(f'[get_product]: {e}')
        
    
    def load_product(self , product):
       
        try:
            self.header_description.set(f"[{product.reference}] {product.product_name}")
            
            self.product_description.delete(1.0 , 'end')
            self.product_description.insert('end' , product.description)
           
            self.expiration.set(MyCalendar.format_date_to_show(f'{product.expiration} 08:00')[0:-6])
        
        except Exception as e:
            print(f"[load_product]: {e}")
        
        
    def add_product(self , product):
        
        if self.product_units_entry.get().isdigit():      
            row_import = round(int(self.product_units_entry.get()) * product.price , 2)
            
            try:
                if product.discount != 0:
                    row_import = row_import - (row_import * int(product.discount) / 100)
                    
                self.order_tree.insert('' , 0 , text = product.reference , values = (product.product_name , product.price , self.product_units_entry.get() , f"{product.discount} %" , row_import))
                
                self.product_description.delete(1.0 , 'end')
                self.product_description.insert('end' , product.description)
                
                OrderFunctions.calculate_import(self)
                
            except Exception as e:
                print(f"[add_product]: {e}")
                
                mb.showerror("Añadir Producto" , f"Error: {e}.")
                
        else:
            mb.showwarning("Unidades" , "Las unidades deben ser un número entero.")
            
            
    def calculate_import(self , e = ""):
        
        order = self.order_tree.get_children()
        total = []
        
        try:
            for item in order:
                row_import = float(self.order_tree.item(item , 'values')[-1])

                total.append(row_import)
                                    
            self.order_import.set(round(sum(total) , 2))
            
            if self.discount.get():
                with_discount =  sum(total) - (sum(total) * int(self.discount.get()) / 100)
                
                total_order_import = with_discount + with_discount * 8 / 100
                
            else:
                total_order_import = sum(total) + (sum(total) * 8 / 100)
                
            self.total_order_import.set(round(total_order_import , 2))
        
        except Exception as e:
            print(f"[calculate_import]: {e}")
        
        
        
    def delete_product(self):
        
        try:
            item = self.order_tree.focus()
            
            self.order_tree.delete(item)
            
            OrderFunctions.get_product(self , "products" , e)
            
            OrderFunctions.calculate_import(self , e = "")
        
        except Exception as e:
            print(f"[delete_product]: {e}")
        
        
    def send_order(self): 
  
        id_order = db.session.query(Orders).order_by(Orders.id_order.desc()).first()
        buyer = db.session.get(Client , self.company_id.get())
        buyer = buyer.contact_person
        print(self.modify_order_id , id_order )
        print((id_order is not None) ,( not self.modify_order_id[0]))
        try:
            if id_order is not None and not self.modify_order_id[0]:
                id_order = id_order.id_order + 1
                            
            elif id_order is None and not self.modify_order_id[0]:    
                id_order = 1 
                
            else:
                id_order = self.modify_order_id[1]
                ModifyDeleteOrder.delete_order(self , id_order , "" , "" , True)
                
            order = self.order_tree.get_children()
            print(f"ORDER ID: {id_order}")  
            for x in order:#         id_order , product_reference ,                product_units ,                        order_client_id ,                 seller_id ,         buyer_id ,            order_date ,                total_import                         , order_notes):
                
                order_entry = Orders(id_order ,self.order_tree.item(x , 'text') , self.order_tree.item(x , 'values')[2] , self.company_id.get() , self.active_employee_id.get() , buyer,  str(datetime.now())[0:16] , self.order_tree.item(x , 'values')[4] , self.oreder_notes.get(1.0, "end") , self.discount.get() )
                
                db.session.add(order_entry)
                db.session.commit()
                
                id_order_to_update = db.session.query(Orders).filter(Orders.id_order == id_order).order_by(Orders.null_id.desc()).first()
                
                Stock.update_stock_send(self , id_order_to_update , "send")
                
            db.session.close()
            
            OrderFunctions.clean_order(self)
            
            self.modify_order_id = [False , None]

        except Exception as e:
            print(f"[send_order]: {e}")
    
    
    def clean_order(self):
        
        clean = self.order_tree.get_children()
        
        for x in clean:
            self.order_tree.delete(x)
        
        self.discount.set("")
        self.total_order_import.set("")
        self.order_import.set("")
    
    
    def sales_historical(self):
        
        window = Toplevel()  
        window.configure(bg = "#f4f4f4")
        window.geometry("800x300")
        window.resizable(0,0)
        window.title(f"Historial de Ventas")
        window.grid_columnconfigure(0 , weight = 1)
        window.grid_rowconfigure(0 , weight = 1)
        
        client = db.session.get(Client , self.company_id.get())
 
        self.historial_frame = CTkFrame(window , fg_color = 'transparent')
        self.historial_frame.grid(row = 0 , column = 0 , padx = 10 , pady = 10 , sticky = "nswe")
        self.historial_frame.grid_columnconfigure(0 , weight = 1)
        #self.historial_frame.grid_rowconfigure(1 , weight = 1)
        
        self.historial_header = CTkFrame(self.historial_frame , border_width = 1 , border_color = 'gray' , fg_color = 'transparent' , height = 40)
        self.historial_header.grid(row = 0 , column = 0 ,  sticky = W+E , padx = 3 , pady = 3)
        self.historial_header.grid_columnconfigure(0 , weight = 1)
        self.historial_header.grid_columnconfigure(1 , weight = 1)
        self.historial_header.grid_columnconfigure(2 , weight = 1)
        self.historial_header.grid_columnconfigure(3 , weight = 1)
        self.historial_header.grid_columnconfigure(4 , weight = 1)
        
        self.reference_view_header = CTkLabel(self.historial_header , text = f"Referencia" , text_color = 'gray')
        self.reference_view_header.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.units_view_header = CTkLabel(self.historial_header , text = "Total Productos", text_color = 'gray')
        self.units_view_header.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W)
        
        self.price_view_header = CTkLabel(self.historial_header , text ="Importe" , text_color = 'gray')
        self.price_view_header.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W)
        
        self.date_view_header = CTkLabel(self.historial_header , text = "Fecha" , text_color = 'gray')
        self.date_view_header.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = W)
        
        self.date_view_header = CTkLabel(self.historial_header , text = f"Hasta: {MyCalendar.format_date_to_show(str(datetime.now())[:16])}" , width = 100 , fg_color = 'Lightblue4' , corner_radius = 4 , text_color = "white")
        self.date_view_header.grid(row = 0 , column = 4 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.historial_content = CTkScrollableFrame(self.historial_frame , border_width = 1 , border_color = 'gray' , fg_color = 'transparent' , scrollbar_fg_color = 'transparent' )
        self.historial_content.grid(row = 1 , column = 0 ,  sticky = W+E , padx = 3 , pady = 3)
        self.historial_content.grid_columnconfigure(0 , weight = 1)
        
        Pops.center_window(self , window)
        
        window.lift()
        
        OrderFunctions.group_orders(self , window)
        
        
    def group_orders(self , historical_window):
        
        orders = db.session.query(Orders).filter(Orders.order_client_id == self.company_id.get()).all()
        
        orders_id = []
        
        for order in orders:          # Obtenemos un único id por pedido
            
            if order.id_order not in orders_id:
                orders_id.append(order.id_order)

        for i, single_id in enumerate(orders_id):  # Obtenemos todos los productos del pedido con ese id
            single_order = db.session.query(Orders).filter(Orders.id_order == single_id).all()
            
            products = []
            imports = []
            
            self.orders_view = CTkFrame(self.historial_content , fg_color = 'lightgray' , corner_radius = 4)
            self.orders_view.grid(row = i , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            self.orders_view.grid_columnconfigure(0 , weight = 1)
            self.orders_view.grid_columnconfigure(1 , weight = 1)
            self.orders_view.grid_columnconfigure(2 , weight = 1)
            self.orders_view.grid_columnconfigure(3 , weight = 1)
            self.orders_view.grid_columnconfigure(4 , weight = 1)
            
            
            for order_view in single_order:   # Recorremos los productos y ...
                products.append(order_view.product_units)
                imports.append(order_view.total_import)
    
            self.reference_view = CTkLabel(self.orders_view , text = f"Pedido ID[{orders_id[i]}]" , text_color = 'gray')
            self.reference_view.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.units_view = CTkLabel(self.orders_view , text = str(sum(products)) , text_color = 'gray')
            self.units_view.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.price_view = CTkLabel(self.orders_view , text ="{:.2f} €".format((sum(imports))) , text_color = 'gray' , anchor = "e")
            self.price_view.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.date_view = CTkLabel(self.orders_view , text = MyCalendar.format_date_to_show(order_view.order_date) , text_color = 'gray')
            self.date_view.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.date_view = CTkButton(self.orders_view , text = "Ver Pedido" , width = 80 , fg_color = 'Lightblue4' , corner_radius = 4 , command = lambda order_id_to_show = orders_id[i]: OrderFunctions.view_single_order(self , order_id_to_show , historical_window))
            self.date_view.grid(row = 0 , column = 4 , padx = 5 , pady = 5 , sticky = E)
            
            
    def view_single_order(self , order_id , historical_window):
        
        window = Toplevel()  
        window.configure(bg = "#f4f4f4")
        window.grid_columnconfigure(0 , weight = 1)
        
        order = db.session.query(Orders).filter(Orders.id_order == order_id).all()
        client = db.session.get(Client , order[0].order_client_id)
        contact_person = db.session.get(ContactPerson , order[0].buyer_id)
        window.title(f"Pedido: ref.{order[0].id_order}")
        
        imports = []
        
        self.client_info_frame= CTkFrame(window , fg_color = 'transparent')
        self.client_info_frame.grid(row = 0 , column = 0 , padx = 5 , pady = 10 , sticky = W+E)
        self.client_info_frame.grid_columnconfigure(0 , weight = 1)
        self.client_info_frame.grid_columnconfigure(1 , weight = 1)
        self.client_info_frame.grid_columnconfigure(2 , weight = 1)
        self.client_info_frame.grid_columnconfigure(3 , weight = 1)
        
        self.client_info= CTkLabel(self.client_info_frame, text = f'   Referencia: {order[0].id_order}   ' , text_color = 'white' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.client_info.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = W)
        
        self.order_client_name = CTkLabel(self.client_info_frame , text = f'   Cliente:    {client.name}         ' , text_color = 'white' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.order_client_name.grid(row = 1 , column = 1 ,  pady = 5 , sticky = W+E)
        
        self.client_employee = CTkLabel(self.client_info_frame , text = f'Persona que realiza el pedido:    {contact_person.contact_name} {contact_person.contact_surname}   ' , text_color = 'white' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.client_employee.grid(row = 1 , column = 2 , pady = 5 , sticky = W+E)
        
        self.order_date_top= CTkLabel(self.client_info_frame, text = f'   Fecha del Pedido: {MyCalendar.format_date_to_show(order[0].order_date)}   ' , text_color = 'white' , fg_color = 'Lightblue4' , corner_radius = 3)
        self.order_date_top.grid(row = 1 , column = 3 , padx = 5 , pady = 5 , sticky = E)
        
        
        self.window_header= CTkFrame(window , fg_color = 'Lightblue4' , corner_radius = 3)
        self.window_header.grid(row = 1 , column = 0 , padx = 10 , pady = 5 , sticky = W+E)
        self.window_header.grid_columnconfigure(0 , weight = 2)
        self.window_header.grid_columnconfigure(1 , weight = 5)
        self.window_header.grid_columnconfigure(2 , weight = 2)
        self.window_header.grid_columnconfigure(3 , weight = 2)
        self.window_header.grid_columnconfigure(4 , weight = 2)
        self.window_header.grid_columnconfigure(5 , weight = 2)
        
        self.reference_view_label= CTkLabel(self.window_header, text = 'Referencia' , text_color = 'white' , font = ("", 12, "bold"))
        self.reference_view_label.grid(row = 1 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.product_name_view_label = CTkLabel(self.window_header , text = 'Nombre' , text_color = 'white' , font = ("", 12, "bold"))
        self.product_name_view_label.grid(row = 1 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.price_view_label= CTkLabel(self.window_header, text = 'Precio' , text_color = 'white' , font = ("", 12, "bold"))
        self.price_view_label.grid(row = 1 , column = 2 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.units_view_label = CTkLabel(self.window_header , text = 'Unidades', text_color = 'white' , font = ("", 12, "bold"))
        self.units_view_label.grid(row = 1 , column = 3 , padx = 5 , pady = 5 , sticky = W+E)
        
        self.product_discount_label = CTkLabel(self.window_header , text = 'Descuento' , text_color = 'white' , font = ("", 12, "bold"))
        self.product_discount_label.grid(row = 1 , column = 4 , padx = 5 , pady = 5 , sticky = W+E)
    
        self.products_total_import_label = CTkLabel(self.window_header , text = 'Importe' , text_color = 'white' , font = ("", 12, "bold"))
        self.products_total_import_label.grid(row = 1 , column = 5 , padx = 5 , pady = 5 , sticky = W+E)

        self.margin = CTkLabel(self.window_header , text = '' , text_color = 'white' , width = 10 , font = ("", 12, "bold")) 
        self.margin.grid(row = 1 , column = 6 , padx = 5 , pady = 5 )
        
        self.order_view_frame = CTkScrollableFrame(window , fg_color = 'transparent')
        self.order_view_frame.grid(row = 2 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        self.order_view_frame.grid_columnconfigure(0 , weight = 1)
        
        for i, product in enumerate(order):          # Obtenemos los productos del pedido
            imports.append(product.total_import)
            
            self.product_view_frame = CTkFrame(self.order_view_frame , fg_color = 'transparent')
            self.product_view_frame.grid(row = i , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            self.product_view_frame.grid_columnconfigure(0 , weight = 2)
            self.product_view_frame.grid_columnconfigure(1 , weight = 1)
            self.product_view_frame.grid_columnconfigure(2 , weight = 2)
            self.product_view_frame.grid_columnconfigure(3 , weight = 2)
            self.product_view_frame.grid_columnconfigure(4 , weight = 2)
            self.product_view_frame.grid_columnconfigure(5 , weight = 2)
        
            product_info = db.session.get(Products , product.product_reference)
            
            self.reference_view = CTkLabel(self.product_view_frame  , text = f'{product_info.reference}' , text_color = 'gray')
            self.reference_view.grid(row = 0 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.product_name_view = CTkLabel(self.product_view_frame , text = f'{product_info.product_name}' , text_color = 'gray', width = 150)
            self.product_name_view.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W+E)
            
            self.price_view = CTkLabel(self.product_view_frame , text = f'{product_info.price}' , text_color = 'gray')
            self.price_view.grid(row = 0 , column = 2 , padx = 5 , pady = 5 )
            
            self.units_view = CTkLabel(self.product_view_frame  , text = f'{product.product_units}' , text_color = 'gray')
            self.units_view.grid(row = 0 , column = 3 , padx = 5 , pady = 5 )
            
            self.product_discount = CTkLabel(self.product_view_frame , text = f'{product_info.discount}' , text_color = 'gray')
            self.product_discount.grid(row = 0 , column = 4 , padx = 5 , pady = 5 )
        
            self.products_total_import = CTkLabel(self.product_view_frame  , text = f'{product.total_import}' , text_color = 'gray')
            self.products_total_import.grid(row = 0 , column = 5 , padx = 5 , pady = 5 , sticky = W+E)
            
            #self.delete_product_button = CTkButton(self.product_view_frame , width = 20 , text = 'x' , fg_color = 'red' , corner_radius = 4 , text_color = 'white' , command = lambda reference = self.reference_view.get() , row = i: ModifyDeleteOrder.delete_product(self , reference , window , historical_window , order[0].id_order))
            #self.delete_product_button.grid(row = 0 , column = 6 , padx = 5 , pady = 5)
            
            
            
        self.order_footer = CTkFrame(window , fg_color = 'transparent')
        self.order_footer .grid(row = 3 , column = 0 , padx = 5 , pady = 5 , sticky = W+E)
        self.order_footer.grid_columnconfigure(2 , weight = 1)
        
        
        self.delete_order_button = CTkButton(self.order_footer , text = "Eliminar Pedido" , fg_color = 'Lightblue4', text_color = 'white' , corner_radius = 3 , command = lambda: ModifyDeleteOrder.delete_order(self, order[0].id_order ,  window , historical_window))
        self.delete_order_button.grid(row = 0 , column = 1 , padx = 5 , pady = 5 , sticky = W)
        
        self.modify_order_button = CTkButton(self.order_footer , text = "Modificar Pedido" , fg_color = 'Lightblue4', text_color = 'white' , corner_radius = 3, command = lambda: ModifyDeleteOrder.modify_order(self, order[0].id_order ,  window , historical_window))
        self.modify_order_button.grid(row = 0 , column = 2 , padx = 5 , pady = 5 , sticky = W)
            
        self.order_total_import = CTkLabel(self.order_footer , text = f'   Iporte Total: {(sum(imports)):.2f} €    Descuento en pedido:   {0 if order[0].order_discount is None else order[0].order_discount } %   ' , fg_color = 'Lightblue4', text_color = 'white' , corner_radius = 3)
        self.order_total_import.grid(row = 0 , column = 3 , padx = 5 , pady = 5 , sticky = E)
        
        
        Pops.center_window(self, window)
        window.lift()
        
        
        
class ModifyDeleteOrder:
    
    
    def modify_order(self , order_id , single_order_window , historical_window): # order =[order[0].id_order , self.reference_view , self.units_view , self.product_discount]
        
        self.sales_root_from_modify()
        
        order = db.session.query(Orders).filter(Orders.id_order == order_id).all()
        
        try:
            for row in order:
                product = db.session.get(Products , row.product_reference)
                
                row_import = round(int(row.product_units) * product.price , 2)
                
                if int(product.discount) > 0:
                    row_import - ModifyDeleteOrder.percentage(row_import , product.discount)
                # Cargamos los producto en el nuevo pedido que tendrá el mismo id.
                self.order_tree.insert('' , 0 , text = product.reference , values = (product.product_name , product.price , row.product_units , f"{product.discount} %" , row_import))
                
            self.modify_order_id = [True , order_id]  # Pasamos el mismo id de pedido.
            
            single_order_window.destroy() # 
            historical_window.destroy()
        
        except Exception as e:
            print(f"[modify_order]: {e}")
            
            mb.showerror("Modificar Pedido" , f"\n{e}\n")
            

    def delete_order(self , order_id_to , single_order_window , historical_window , old = False):
        
        try:
            products = db.session.query(Orders).filter(Orders.id_order == order_id_to).all()
            
            for product in products:                
                Stock.update_stock_send(self , product , "delete")
                
                db.session.delete(product)
                db.session.commit()
            db.session.close()
            
            if not old:
                historical_window.destroy()
                single_order_window.destroy()
                
                OrderFunctions.sales_historical(self)
            
        except Exception as e:
            print(f"[delete_order]: {e}")
            
            mb.showerror("Elimniar Pedido" , f"\n{e}\n")
        
        
    def delete_product(self , reference , window , historical_window , order_id_to_show):
        
        try:
            product = db.session.query(Orders).filter(and_(Orders.id_order == order_id_to_show , Orders.product_reference == reference)).first()
                                                    
            db.session.delete(product)
            
            Update.save_close()
            
            window.destroy()
            
            OrderFunctions.view_single_order(self , order_id_to_show , historical_window)
        
        except Exception as e:
            print(f"[delete_product]: {e}")
            
            mb.showerror("Elimniar Producto" , f"\n{e}\n")
        
        
            
            
    def percentage(number , percentage):
        
        try:
            result = round((number * percentage) / 100 , 2)
            
            return result
        
        except Exception as e:
            print(f"[percentage]: {e}")
    
    
    def focus_product_list(self , e):
        
        order_products = self.order_tree.get_children()
        
        try:
            for order_product in order_products:
                if order_product == self.order_tree.focus():
                    reference = self.order_tree.item(order_product  , 'text') 
                    
            products = self.products_tree.get_children()
            
            for product in products:
                if self.products_tree.item(product , 'text') == reference:
                    self.products_tree.selection_set(product)
        
        except UnboundLocalError:
            pass
        
        except Exception as e:
            print(f"[focus_product_list]: {e}")
            
            mb.showerror("Error" , f"\n{e}\n")
                
                
class Stock:
    
    def update_stock_send(self , product , actions):
                       
        try:
            product_to_update = db.session.get(Products , product.product_reference)
            
            if actions == "send" and   product_to_update.units > product.product_units:
                product_to_update.units -= product.product_units
            
            else:
                product_to_update.units += product.product_units
            
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            
            print(f"[update_stock]: {e}")
            
            mb.showerror("Actualizar Stock" , f"\n{e}\n")
            
                
                
  
                