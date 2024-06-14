
# Tkinter
Aplicación de Escritorio Utilizando Tkinter

## CRM Gestión de Clientes y Ventas.


### Descripción General del Proyecto
Se trata de una  herramienta diseñada para ayudar a las empresas a gestionar sus interacciones con los clientes y prospectos.
 Este sistema centraliza la información de los clientes, facilita la gestión de ventas y mejora la comunicación y el seguimiento de los contactos. 
La aplicación permite a los usuarios registrar y organizar datos de los clientes, así como registrar directamente las ventas.

### Objetivos y Alcalde del Proyecto.
1. Centralizar la información de los clientes en una única plataforma accesible.
2. Facilitar el seguimiento y la gestión de las oportunidades de ventas.
3. Tener un registro de las veces que se ha contactado con el cliente y cuál ha sido su respuesta.
4. Realizar la venta o tomar el pedido directamente desde la plataforma de seguimiento (CRM).

### Stack Tecnológico y Alternativas Evaluadas.

#### Stack Tecnológico:
Lenguaje de Programación: Python
Se ha optado por python por su flexibilidad y porque el proyecto trata de este.

**Interfaz de Usuario:** *Tkinter* y *CustomTkinter*

Se ha usado Tkinter por su integración (viene preinstalado) y su sencillez para agilizar la entrega de este proyecto. Se ha usado CustomTkinter para la mejora de la interfaz.

**Procesamiento de Imágenes:** *PIL (Pillow)*
Para poder manejar diferentes formatos de imagen ya que Tkinter solo soporta GIF y PPM/PGM de forma nativa.

**Gestión de Fechas:** *datetime*
Para ciertas funcionalidades que requerían trabajar con fechas.

**Calendario:** tkcalendar
Como complemento a datetime en las funcionalidades que implican fechas y manejo de tiempo.

**Navegación Web:** *webbrowser*
Para algunas funcionalidades que requerían de abrir páginas web o el gestor de correo electrónico.

**Manejo de Excel:** *openpyxl*
Para el manejo de ficheros excel, actualmente solo se necesita para cargar varias empresas, en futuras actualizaciones se usará para exportar datos.

**ORM y Base de Datos:** *SQLAlchemy*
ORM para facilitar la migración o implementación de otras bases de datos SQL.

**Manipulación de Datos:** *pandas*
Para crear un dataframe en un punto concreto de la aplicación que requería mostrar información de diversas fuentes.

**Concurrencia:** threading
Para programar que se revisen cambios en la base de datos de forma periódica.

**Sistema Operativo:** os
Para detectar en qué sistema operativo se está ejecutando la aplicación y evitar fallos de formato u otros.


## Alternativas Evaluadas:

### ORM y Base de Datos
Se evaluó la posibilidad de realizar el proyecto con SQLite3, MySQL o PostgreSQL directamente pero finalmente se optó por un ORM (sqlalchemy) por su mayor flexibilidad que facilitará el cambio a cualquiera de estas en un futuro.
La Base de Datos utilizada es SQLite3.

### Interfaz de Usuario:
Se consideraron PyQt5 o Kivi por su mayor versatilidad y flexibilidad en la apariencia y la estética pero finalmente fueron descartadas por diversas razones la principal la curva de aprendizaje y se optó por Tkinter dada su sencillez y que ya me encontraba familiarizado con ella.

### Modelo de Datos.
Se ha optado por una base de datos SQLite3 para agilizar  la entrega del proyecto.
En la tabla Orders se ha establecido la primary key como null_id dado que sin primary key no permite la creación de la tabla ya que los valores de esta no se pueden repetir y era necesario repetir el id del pedido con sus diferentes entradas por el diseño de la lógica de negocio.

## Esquema de BD.

![Example Image](https://drive.google.com/uc?id=1rEEtfySStxJ2YSyRcG-2uhtFrWnz8uOK)

