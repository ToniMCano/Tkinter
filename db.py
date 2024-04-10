from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import create_engine
import os

try:
    if os.name == "nt":
        engine = create_engine("sqlite:///database\\crm.db")
                
    else:
        engine = create_engine("sqlite:///database/crm.db")
    
    Session = sessionmaker(bind = engine)
        
    session = Session()
    
    Base = declarative_base()
    
    
except Exception as e:
    print(f"Ha ocurrido un error al conectarse a la Base de Datos:\n{e}")
    
    
    