
import openpyxl
from openpyxl import Workbook
import random
import sqlalchemy
from sqlalchemy import and_ , or_ , func ,asc , desc
import db
from models import Client , ContactPerson , Employee , Contact , Products , Orders
from datetime import datetime , timedelta
import os
from tkinter import messagebox as mb
import customtkinter
from actions import GetInfo,LoadInfo , MyCalendar
import pandas as pd
import threading
import time
from tkinter import * 
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np


class Test:   
        
    def statistics_dataframe():
            
            all_products = db.session.query(Products).all()
            all_orders = db.session.query(Orders).all()
        
            product_reference = list(product.reference for product in all_products)
            product_stock = list(product.units for product in all_products)
            
            
            
            orders_id = [order.id_order for order in all_orders]
            orders_product_reference = [order.product_reference for order in all_orders]
            orders_product_name = [db.session.get(Products , order.product_reference).product_name for order in all_orders]
            product_price = [db.session.get(Products , order.product_reference).price for order in all_orders] ###
            orders_product_units = [order.product_units for order in all_orders]
            orders_import = [order.total_import for order in all_orders]
            product_catgory = [db.session.get(Products , order.product_reference).category for order in all_orders]
            product_subcatgory = [db.session.get(Products , order.product_reference).subcategory for order in all_orders]
            
            
            data = {
                'orders_id' : orders_id ,
                'orders_product_reference' : orders_product_reference ,
                'orders_product_name' : orders_product_name ,
                'product_price' : product_price ,
                'orders_product_units' : orders_product_units ,
                'orders_import' : orders_import ,
                'product_catgory' : product_catgory ,
                'product_subcatgory' : product_subcatgory 
            }
            
            
            data_frame = pd.DataFrame(data)
            
            data_frame['total_products_solded'] = data_frame.groupby('orders_product_reference')['orders_product_units'].transform('sum')
            
            return data_frame
            
            

    def order_import_df():
        df = Test.statistics_dataframe()

        grouped_df = df.groupby('orders_id').agg({
            'orders_product_units': 'sum',  # Total de unidades de productos en la orden
            'orders_import': 'sum',  # Total del importe en la orden
            # Total de productos vendidos
            
        }).reset_index()

        for i, x in enumerate(range(5)):
            print('-----------------')
            print(grouped_df.iat[i , 0 ] , grouped_df.iat[i , 1 ] , round(grouped_df.iat[i , 2] , 2))
            print('-----------------')


    def product_units_df(): # devuelve el número de 
        
        df = Test.statistics_dataframe()
        print(df.head())
        for i, x in enumerate(range(5)):
            print('-----------------')
            print(df.groupby('orders_product_reference')['orders_id'].count()) # devuelve el número de pedidos en los que se ha pedido cada producto.
            print('-----------------')

            print('-----------------')
            print(df.groupby('orders_product_reference').agg({'orders_product_units': 'sum'  , 'orders_id': 'sum'})) # devuelve la cantidad de unidades que se ha vendido de ese producto.
            print('-----------------')

Test.product_units_df()