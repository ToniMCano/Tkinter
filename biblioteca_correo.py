from tkinter import ttk
from tkinter import *
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Test:
    
 
    def enviar_correo(destinario, asunto, mensaje):
        #Obtener datos del formulario enviado

        destinatario = ['destinatario']
        asunto = ['asunto']
        mensaje = "Esto es una prueba"  # Mensaje de correo electrónico

    #Si hubiera un campo en el formulario para el mensaje sería

        mensaje = ['mensaje']

        #Configurar servidor SMTP

        smtp_server = 'smtp.example.com'
        puerto = 587  # Puerto SMTP (generalmente 587 para TLS)
        remitente = 'tu_correo@example.com'
        password = 'tu_contraseña'

        #Crear mensaje de correo electrónico

        for mail in destinatario:
            
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = mail
            msg['Subject'] = asunto

            #Adjuntar mensaje al cuerpo del correo

            msg.attach(MIMEText(mensaje, 'plain'))  # Texto sin formato se pueden establecer de otro tipo como html por ejemplo.


            #Iniciar conexión con el servidor SMTP

            with smtplib.SMTP(smtp_server, puerto) as server:
                server.starttls()  # Iniciar conexión TLS
                server.login(remitente, password)  # Autenticarse en el servidor SMTP
                server.send_message(msg) # Enviar correo electrónico

        return 'mensaje: Correo enviado correctamente'
        
        
        
Test.enviar_correo(['destinario'], 'asunto', 'mensaje')