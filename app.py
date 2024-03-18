from tkinter import ttk
from tkinter import *
import sqlite3

#########
class Main:   # El objeto que creamos en esta clase es la ventana principal del programa.   
    
    db = "database/ejercicio.db"
    
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App de Gestión") # Cambia el título de la ventana.
        self.ventana.resizable(1,1) # Habilita la redimensión , para que no se redimensione (0,0).
        self.ventana.wm_iconbitmap("recursos/eye_icon.ico")   # Ruta hacia el icono que queremos mostrar.
        
        frame = LabelFrame(self.ventana , text = "Registrar un Nuevo Producto") 
        frame.grid(column = 0, row = 0, columnspan = 3 , pady = 20)    # Le indicamos donde empieza (column = 0, row = 0) cuanto ocupa (columnspan = 3) y un margen en y (pady = 20)
        
        # Label Nombre
        
        self.etiqueta_nombre = Label(frame , text = "Nombre: ")  # Se asocia a "frame" y el texto que debe incluir
        self.etiqueta_nombre.grid(row = 1 , column = 0)          # Se posiciona en el grid
        
        #Entry Nombre
        
        self.nombre = Entry(frame)    # Lo asociamos al "frame", indicando que es del tipo entrada de texto (Entry) 
        self.nombre.focus()           # El foco aquí
        self.nombre.grid(row = 1 , column = 1)   # Ubicación
        
        # Label Precio
        
        self.etiqueta_precio = Label(frame , text = "Precio: ")
        self.etiqueta_precio.grid(row = 2 , column = 0) 
        
        # Entry de Precio
        self.precio = Entry(frame)  
        self.precio.grid(row = 2, column = 1)
        
        # Mensaje
        
        self.mensaje = Label(text = "" , fg = "red") # No lo asociamos a un Frame, solo le damos ubicación con .grid - "fg" es para el color del texto
        self.mensaje.grid(row = 3 , columnspan = 2 , sticky = W+E)   # self.mensaje.grid(sticky = W+E)   Esto lo ubicaría en el mismo sitio que hemos indicado, debe ser por no estar asociado a un Frame.
                                                                     # Con sticky le indicamos que se expanda,  en este acos de oeste a este (W+E)
        # Botón     
        
        self.boton_anadir = ttk.Button(frame , text = "Añadir Producto" , command = self.add_producto) # Se asocia al "frame" , se añade un texto "Añadir Producto"
        self.boton_anadir.grid(row = 3  , columnspan = 3 , sticky=W+E )                                # command está preparado para recibir una función y no requiere incluir ().
        
        # Crear estilos
        
        style = ttk.Style()
        style.configure("mystyle.Treeview" , highlightthickness = 0 , bd = 0, font = ("Calibri" , 11)) # Modificar la fuente de la tabla
        style.configure("mystyle.Treeview.Heading" , font = ("Calibri" , 13 , 'bold'))   # Modificar la fuente de las cabeceras
        style.layout("mystyle.Treeview" , [("mystyle.Treeview.treearea", {'sticky' : 'nswe'})]) # Eliminar los bordes
        
        # Crear Tabla y aplicar los estilos
        
        self.tabla = ttk.Treeview(height = 20 , columns = 2, style = "mystyle.Treeview")  # Le damos altura, número de columnas y el estlo se debe de llamar así "mystyle.Treeview"
        self.tabla.grid(row = 4 , column = 0)                                             # Si se quieren crear más stilos lo que se modifica es "esto.Treeview"
        self.tabla.heading("#0" , text = "Nombre" , anchor = CENTER)
        self.tabla.heading("#1" , text = "Precio" , anchor = CENTER)
        #self.tabla.heading("#2" , text = "ID" , anchor = CENTER)
        
        #self.frame_botones = Frame(self.ventana , bg = "red")
        #self.frame_botones.grid(row = 5 , column = 0 , sticky= W+E )
        # Botón Eliminar
        self.boton_eliminar = ttk.Button(text = "Eliminar" , command = self.eliminar_producto)
        self.boton_eliminar.grid(row = 5 , column = 0 , sticky = W+E)
        
        # Botón Editar
        self.boton_editar = ttk.Button( text = "Editar" , command = self.editar_producto)
        self.boton_editar.grid(row = 5 , column = 1 )

        
        self.get_productos()
     ######   
        
    def db_consulta(self , consulta, parametros = ()):   # hay que pasar una tupla como valor por defecto porque sqlite siempre espera un valor aquí
        with sqlite3.connect(self.db) as conexion:
            cursor = conexion.cursor()
            resultado = cursor.execute(consulta, parametros)
            conexion.commit()
        return resultado
    
    
    def get_productos(self):
                                    #########
        vista = self.tabla.get_children()      # vaciamos la tabla y la devolemos actualizada con los nuevos productos.
        for producto in vista:
            self.tabla.delete(producto)
            
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        
        for x in registros:   #############     
            self.tabla.insert("" , 0 ,text = str(x[1]) , values = (str(x[2]))) # En Tkinter si quieres insertar elementos al principio de la tabla se hace con 0 si quieres que se incluya al final con
                                                                # "end" en lugar de "" (o en lugar de 0, comprobar) van siempore, 0 es el índice donde se va a insertar empenzando por el principio ("") en este caso.
                                                                # La primera columna de la DB siempre va en "text" y el resto en "values", si quieres todas las columnas x[1:].
    def validar_nombre(self):  #####
        return len(self.nombre.get()) !=0   # Con .get recibimos la información de los cajones de texto. Retornará True o False
       
       
    def validar_precio(self):
        return len(self.precio.get()) != 0

    
    
    def add_producto(self):
        if self.validar_precio() and self.validar_nombre():
            values = (self.nombre.get() , self.precio.get())   # Se podría pasar la consulta directamente MUY IMPORTANTE incluir las comillas simples ('') en las variables.
            query = f"INSERT INTO producto VALUES (NULL,?,?)"  #self.db_consulta(f"INSERT INTO producto (nombre,precio) VALUES('{self.nombre.get()}' , '{self.precio.get()}')")
            self.db_consulta(query , values)     
            self.mensaje["text"] = f"Producto {self.nombre.get()} creado con éxito"    # Para reenplazar el valor de text se hace como si fuera un diccionario self.mensaje["text"]   
            self.mensaje["fg"] = "green"                                                                       
            self.nombre.delete(0,END)  ##### Esto vaciará el campo desde el principio hasta el final.
            self.precio.delete(0,END)
            
        elif self.validar_nombre() and self.validar_precio() == False:
            self.mensaje["fg"] = "red" 
            self.mensaje["text"] = "El Precio es obligatorio"
            
        elif self.validar_nombre() == False and self.validar_precio():
            self.mensaje["fg"] = "red" 
            self.mensaje["text"] = "El Nombre es obligatorio"
            
        else:
            self.mensaje["fg"] = "red" 
            self.mensaje["text"] = "Es obligatorio introducir un nombre un precio."
            
            
        self.get_productos()
        
        
    def eliminar_producto(self):
        producto = self.tabla.item(self.tabla.selection())  # Obtenemos el valor del elemento que esté seleccionado.
        if producto["text"]:
            self.db_consulta(f"DELETE FROM producto WHERE nombre = '{producto["text"]}'")
            self.mensaje["text"] = f'Se ha eliminado {producto["text"]} con éxito'
            self.mensaje["fg"] = 'green'
            
        else:
            self.mensaje["text"] = f'No has seleccionado ningún producto'
            self.mensaje["fg"] = 'red'
            
        self.get_productos()
    
    def editar_producto(self):
        producto = self.tabla.item(self.tabla.selection())
        self.ventana_editar = Toplevel()     # Crea una nueva ventana.    
        self.ventana_editar.title(f"Editar {producto['text']}")
        self.ventana_editar.resizable(0,0)
        self.ventana_editar.wm_iconbitmap("recursos/eye_icon.ico") 
        
        label_editar_nombre = Label(self.ventana_editar , text = "Editar Nombre: ")
        label_editar_nombre.grid(row = 0 , column = 0, pady = 10) 
        
        entry_editar_nombre = Entry(self.ventana_editar)
        entry_editar_nombre.grid(row = 0 , column = 1, pady = 10 , padx = 20) 
        
        label_editar_precio = Label(self.ventana_editar , text = "Editar Precio: ")
        label_editar_precio.grid(row = 1 , column = 0 , pady = 10 )
        
        entry_editar_precio = Entry(self.ventana_editar)
        entry_editar_precio.grid(row = 1 , column = 1, pady = 10 , padx = 20)
        
           
if __name__ == "__main__":
    ########
    root = Tk()
    app = Main(root)   # Creamos un objeto de la clase Producto 
    root.mainloop()
    #########
   