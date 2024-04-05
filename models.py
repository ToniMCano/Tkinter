import db
from db import Base

from sqlalchemy import String, Boolean, Integer, ForeingKey
from sqlalchemy.orm import sessionmaker , relationship # Comprobar si es necesaria.






class Employee(Base):
    
    __table_name__ = "employee"
    __table_args__ = {"sqlite_autoincrement" : True}
    
    id_employee = Column(Integer , primary_key = True)
    employee_name = Column(String , nullable = False)
    employee_surname = Column(String , nullable = False)
    employee_mail = Column(Integer , nullable = False)
    employee_job_title = Column(String , nullable = False)
    password = Column(String , nullable = False)
    permissions = Column(Integer , nullable = False)
    
    def __init__(self, employee_name = "Pool" , employee_surname = "Terminada" , employee_mail = "company.mail@test.com" , employee_job_title = "None" , password = "******" , permisions = 0):
        
        self.employee_name = employee_name
        self.employee_surname = employee_surname
        self.employee_mail = employee_mail
        self.employee_job_title = employee_job_title
        self.password = password
        self.permissions = permisions
        
    def __str__(self):
        
        return f"Se ha añadido el empleado:\nNombre: {self.employee_name}\nApellido: {self.employee_surname}\nMail: {self.employee_mail}\nCargo: {self.employee_job_title}\nPermisos: {self.permissions}"


class Client(Base):                                                      # Definimos la columnas
    
    __table_name__ = "client"
    __table_args__ = {"sqlite_autoincrement" : True}
    
    id_client = Column(Integer , primary_key = True)
    name = Column(String , nullable = False , unique = True)
    nif = Column(String , unique = True)
    adress = Column(String , nullable = False)
    web = Column(String)
    mail = Column(String , nullable = False)
    phone = Column(Integer , nullable = False)
    phone2 = Column(Integer)
    activity = Column(String , nullable = False)
    contact_person = Column(Integer , ForeingKey("contact_person.id_person")) # Referencia al id de la persona de contacto en la tabla Contact Person
    employee_id = Column(Integer , ForeingKey("employee.id_employee"))
    state = Column(String , nullable = False)
    
    def __init__(self , name , nif , adress , web , mail , phone , phone2 , activity , contact_person , employee_id , state): # Creamos el constructor para capturar los valores de cada 
                                                                                                                              # columna el id se autogenera, por eso no lo incluimos
        
        self.name = name
        self.nif = nif
        self.adress = adress
        self.web = web
        self.mail = mail
        self.phone = phone
        self.phone2 = phone2
        self.activity = activity
        self.contact_person = contact_person
        self.employee_id = employee_id
        self.state = state
        
    
    def __str__(self):
        return f"Se ha creado el Cliente:\nNombre: {self.name}\nN.I.F: {self.nif}\nDirección: {self.adress}\nWeb: {self.web}\nMail: {self.mail}\nTeléfono: {self.phone}\nOtro Teléfono: {self.phone2}\nActividad: {self.activity}\nPresona de contacto: {self.contact_person}\nEstado: {self.name}\nEmpleado al cargo: {self.employee_id}"
    
    
    class ContactPerson(Base):
        
        __table_name__ = "contact_person"
        __table_args__ = {"sqlite_autoincrement" : True}
        
        id_person = Column(Integer , primary_key = True)
        contact_name = Column(String , nullable = False)
        contact_surname = Column(String , nullable = False)
        contact_job_title = Column(String , nullable = False)
        contact_phone = Column(Integer , nullable = False)
        contact_mail = Column(String , nullable = False)
        
        
        
        def __init__(self , )
        
        