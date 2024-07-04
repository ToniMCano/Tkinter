
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
        # Consulta optimizada para obtener todos los datos necesarios en una sola consulta
        query = db.session.query(
            Orders.id_order,
            Orders.product_reference,
            Orders.product_units,
            Orders.total_import,
            Products.product_name,
            Products.price,
            Products.category,
            Products.subcategory,
            Orders.order_date
        ).join(Products, Orders.product_reference == Products.reference)

        result = query.all()

        # Extracción de los datos de la consulta
        orders_id = [row.id_order for row in result]
        orders_product_reference = [row.product_reference for row in result]
        orders_product_name = [row.product_name for row in result]
        product_price = [row.price for row in result]
        orders_product_units = [row.product_units for row in result]
        orders_import = [row.total_import for row in result]
        product_catgory = [row.category for row in result]
        product_subcatgory = [row.subcategory for row in result]
        orders_date = [row.order_date for row in result]

        data = {
            'orders_id': orders_id,
            'orders_product_reference': orders_product_reference,
            'orders_product_name': orders_product_name,
            'product_price': product_price,
            'orders_product_units': orders_product_units,
            'orders_import': orders_import,
            'product_catgory': product_catgory,
            'product_subcatgory': product_subcatgory,
            'orders_date' : orders_date
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


    def product_dataframe(): # devuelve el número de 
        
        df = Test.statistics_dataframe()
        
        
        new_dataframe = df.groupby('orders_product_reference').agg({
            'orders_product_units': 'sum',
            'orders_id' : 'nunique',
            'orders_product_name' : 'unique',
            'product_price' : 'unique',
            'orders_import' : 'sum',
            #'product_catgory' : 'unique' ,
            #'product_subcatgory' : 'unique' ,
            
        })
        
        new_dataframe['average_units_per_order'] = new_dataframe['orders_product_units'] / new_dataframe['orders_id']
        new_dataframe['average_units_per_order'] = new_dataframe['orders_product_units'] / new_dataframe['orders_id']
        new = df.loc[df['orders_product_reference'] == 1007 , ['orders_date']].sort_values(by = "orders_date").reset_index(drop=True)
        print(new.loc[0])
        newnew =new.sort_values(by = 'orders_date' , ascending = False).reset_index()
        print(newnew.loc[0])
        #print(new_dataframe)
        #print(df.groupby('orders_product_reference')['orders_id'].count().head()) # devuelve el número de pedidos en los que se ha pedido cada producto.
        #print('-----------------')
        #print('-----------------')
        #print(df.groupby('orders_product_reference').agg({'orders_product_units': 'sum'  , 'orders_id': 'count' , 'orders_id': 'nunique'}).head()) # devuelve la cantidad de unidades que se ha vendido de ese producto.
        #print(f"-------{df['orders_import'].mean()}----------")
        print(new_dataframe.columns)
Test.product_dataframe()
