import db
from db import Base
from sqlalchemy import String, Boolean, Integer, ForeignKey, Column
from sqlalchemy.orm import sessionmaker , relationship # Comprobar si es necesaria.


class Employee(Base):
    
    __tablename__ = "employee"
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
    
    __tablename__ = "client"
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
    contact_person = Column(Integer , ForeignKey("contact_person.id_person")) # Referencia al id de la persona de contacto en la tabla Contact Person
    employee_id = Column(Integer , ForeignKey("employee.id_employee"))
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
    
    __tablename__ = "contact_person"
    __table_args__ = {"sqlite_autoincrement" : True}
    
    id_person = Column(Integer , primary_key = True)
    contact_name = Column(String , nullable = False)
    contact_surname = Column(String , nullable = False)
    contact_job_title = Column(String , nullable = False)
    contact_phone = Column(Integer , nullable = False)
    contact_mobile = Column(Integer)
    contact_mail = Column(String , nullable = False)
    client_id = Column(Integer , ForeignKey("client.id_client"))
    notes = Column(String)
    
    
    def __init__(self , contact_name , contact_surname , contact_job_title, contact_phone , contact_mobile , contact_mail ,client_id , notes = ""):
        
        self.contact_name = contact_name
        self.contact_surname = contact_surname
        self.contact_job_title = contact_job_title
        self.contact_phone = contact_phone
        self.contact_mobile = contact_mobile
        self.contact_mail = contact_mail
        self.client_id = client_id
        self.notes = notes
    
        
    def __str__(self):
        return f"Se ha creado el Contacto:\nNombre: {self.contact_name}\nApellido: {self.contact_surname}\nCargo: {self.contact_job_title}\nTeléfono: {self.contact_phone}\nMóvil: {self.contact_mobile}\nMail: {self.contact_mail}"

    
class Contact(Base):
    
    __tablename__ = "contact"
    __table_args__ = {"sqlite_autoincrement" : True}
    
    id_contact = Column(Integer , primary_key = True)
    company_state = Column(String , nullable = False)
    last_contact = Column(String)
    log = Column(String , nullable = False)
    client_id = Column(Integer , ForeignKey("client.id_client"))
    contact_state = Column(String , nullable = False)
    contact_counter = Column(Integer , nullable = False)
    contact_employee_id = Column(Integer , ForeignKey('employee.id_employee'))
    contact_person_id = Column(Integer , ForeignKey('contact_person.id_person'))

def __init__(self , last_contact , log , client_id , contact_state , contact_counter , contact_employee_id , contact_person_id , company_state = 'pool'):
    self.company_state = company_state
    self.last_contact = last_contact
    self.log = log
    self.client_id = client_id
    self.contact_state = contact_state
    self.contact_counter = contact_counter
    self.contact_employee_id = contact_employee_id
    self.contact_person_id = contact_person_id