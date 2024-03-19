
import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3


class Main:
    def __init__(self, root):
        self.ventana_principal = root
        self.ventana_principal.title("MyCRM")
        self.ventana_principal.resizable(1,1)
        
        
        self.info = ttk.Treeview(columns = 4)
        self.info.grid(row =0 , column = 0)
        
        self.info["columns"] = ("ultimo_contacto" , "ultima_venta", "Cantidad" , "Porcentaje")
        self.info.heading("#0" , text = "Cliente")
        self.info.heading("#1" , text  ="Último Contacto")
        self.info.heading("#2" , text = "Ultima Venta")
        self.info.heading("#3" , text = "Cantidad")
        self.info.heading("#4" , text = "Porcentaje")
        
        # FRAME EMPRESA
        
        self.frame_empresa = ttk.LabelFrame(self.ventana_principal , text = "Información Empresa")
        self.frame_empresa.grid(row =0 , column = 1)
        
        self.label_nombre_empreasa = ttk.Label(self.frame_empresa, text = "Empresa")
        self.label_nombre_empreasa.grid(row =0 , column = 0 , sticky=W)
        
        self.entry_nombre_empresa = ttk.Entry(self.frame_empresa)
        self.entry_nombre_empresa.insert(0 , "Gusanitos,S.A") # Es lo mismo que placeholder
        self.entry_nombre_empresa.grid(row = 1 , column= 0 , columnspan=2 , sticky = W+E)
        
        self.label_actividad_empresa = ttk.Label(self.frame_empresa , text = "Actividad")
        self.label_actividad_empresa.grid(row = 2 , column = 0 , sticky=W)
        
        self.entry_actividad_empresa = ttk.Entry(self.frame_empresa)
        self.entry_actividad_empresa.insert(0, "Arquitectura e Ingeniería")
        self.entry_actividad_empresa.grid(row = 3 , column = 0) 
        
        self.label_empleados_empresa = ttk.Label(self.frame_empresa , text = "Número de Empleados")
        self.label_empleados_empresa.grid(row = 2 , column = 1 , sticky = W)
        
        self.entry_empleados_empresa = ttk.Entry(self.frame_empresa)
        self.entry_empleados_empresa.insert(0,"50-100")
        self.entry_empleados_empresa.grid(row = 3 , column = 1)
        
        self.label_web_empresa = ttk.Label(self.frame_empresa , text = "Web")
        self.label_web_empresa.grid(row = 4 , column = 0 , sticky = W)
        
        self.entry_web_empresa = ttk.Entry(self.frame_empresa)
        self.entry_web_empresa.insert(0,"www.google.com")
        self.entry_web_empresa.grid(row = 5 , column = 0)
        
        self.label_mail_empresa = ttk.Label(self.frame_empresa , text = "Mail")
        self.label_mail_empresa.grid(row = 4 , column = 1 , sticky = W)
        
        self.entry_mail_empresa = ttk.Entry(self.frame_empresa)
        self.entry_mail_empresa.insert(0,"provwork2015@gmail.com")
        self.entry_mail_empresa.grid(row = 5 , column = 1)
        
        self.label_telefono_empresa = ttk.Label(self.frame_empresa , text = "Teléfono")
        self.label_telefono_empresa.grid(row = 6 , column = 0 , sticky = W)
        
        self.entry_telefono_empresa = ttk.Entry(self.frame_empresa)
        self.entry_telefono_empresa.insert(0,"965125477")
        self.entry_telefono_empresa.grid(row = 7 , column = 0)
        
        self.label_telefono_dos = ttk.Label(self.frame_empresa , text = "Otro Teléfono")
        self.label_telefono_dos.grid(row = 6 , column = 1 ,sticky = W)
        
        self.entry_telefono_dos = ttk.Entry(self.frame_empresa)
        self.entry_telefono_dos.insert(0,"965126874")
        self.entry_telefono_dos.grid(row = 7 , column = 1)
        
        
        #FRAME CONTACTO
        
        self.frame_contacto = ttk.LabelFrame(self.ventana_principal , text = "Persona de Contacto")
        self.frame_contacto.grid(row = 1 , column = 1)
        
        self.label_nombre_contacto = ttk.Label(self.frame_contacto , text = "Persona de Contacto")
        self.label_nombre_contacto.grid(row =0 , column = 0 , sticky = W)
        
        self.entry_nombre_contacto = ttk.Entry(self.frame_contacto)
        self.entry_nombre_contacto.insert(0 , "Pepito")
        self.entry_nombre_contacto.grid(row = 1 , column = 0)
        
        self.label_apellido_contacto = ttk.Label(self.frame_contacto , text = "Apellido")
        self.label_apellido_contacto.grid(row = 0 , column = 1)
        
        self.entry_apellido_contacto = ttk.Entry(self.frame_contacto)
        self.entry_apellido_contacto.insert(0, "Palotes")
        self.entry_apellido_contacto.grid(row = 1 , column = 1)
        
        



if __name__ == "__main__":
    
    root = Tk()
    app = Main(root)
    root.mainloop()
    
