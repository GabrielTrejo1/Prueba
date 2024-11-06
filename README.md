# Proyecto AC Automotores
## Estado del proyecto
    en desarrollo

## Descripción
Este es un proyecto para la gestion de automoviles en una agencia de vehiculos 

## Instalación
1. Clona el repositorio
2. Instala las dependencias
   ```bash
   pip install -r requirements.txt

   ```
3. Ejecuta el proyecto
   ```bash
   python src/controllers/main.py
   ```

## Autores
Gabriel trejo https://github.com/GabrielTrejo1
Alejandro Tonda https://github.com/aletondaX
Federico Mozzi https://github.com/FedericoMozzi
Marcos Cufre https://github.com/cucu2023

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Estructura del proyecto
```
├── README.md
├── requirements.txt
├── src
│   ├── controllers
│   │   ├── cliente.py
│   │   ├── inicio.py
│   │   ├── main.py
│   │   ├── vehiculo.py
│   │   └── ventas.py
│   ├── gui
│   │   ├── clientes.ui
│   │   ├── inicio.ui
│   │   ├── vehiculos.ui
│   │   └── ventas.ui
│   ├── models
│   │   ├── conexion.py
└── app.py
```
## Explicacion del codigo
### Controllers
Los controllers son los componentes que interactúan con la interfaz gráfica. 
En este proyecto, los controllers se encargan de manejar las interacciones del usuario con la aplicación. 
Cada controller tiene una clase que hereda de la clase `Controller` 
y tiene un método `initGui` que se encarga de inicializar la interfaz gráfica.

### Gui
La interfaz gráfica se encuentra en el directorio `src/gui`.
Cada archivo de interfaz gráfica se encuentra en un directorio separado.

## Tecnologías usadas
- Python3
- PyQt5
- SQL-SERVER
- PyODBC
- PYQT-DESIGNER

## Diagrama de base de datos
```
+----------------+     +---------------+     +--------------+     
|                |     |               |     |              |     
|  Cliente       |     |  Vehiculo     |     |  Venta       |     
|                |     |               |     |              |     
+----------------+     +---------------+     +--------------+    
|                |     |               |     |              |     
|   Nombre       |     |  Marca        |     |  Cliente     |     
|                |     |               |     |              |     
|    ...         |     |   ...         |     |   ...        |    
|                |     |               |     |              |     
+-------+--------+     +-------+-------+     +-------+------+     
        |                   |                   |                 
        |                   |                   |                   
        v                   v                   v                   
+-------+-------+     +-------+-------+     +-------+-------+     
|                |     |               |     |              |     
|  Cliente       |     |   Vehiculo    |     |    Venta     |     
|                |     |               |     |              |    
+-------+-------+      +---------------+     +--------------+     
        |                   |                     |                  
        |                   |                     |                  
        v                   v                     v                   
+-------+-------+     +-------+-------+      +-------+-------+    
|       ID       |     |       ID      |    |       ID      |   
|                |     |               |    |               |     
|    ClienteID   |     |  VehiculoID   |    |    VentaID    |     
|                |     |               |    |               |     
+-----------------+    +---------------+    +---------------+     
```

## Explicacion de clases

### Cliente
Representa a un cliente de la agencia de vehiculos. Contiene información como nombre
, apellido, dirección, telefono, correo electrónico y número de identificación.
esta clase se encarga de manejar las transacciones de la base de datos relacionadas con el cliente.
Ejemplo de transacciones:
- Agregar un cliente a la base de datos
- Eliminar un cliente de la base de datos
- Buscar un cliente en la base de datos
- Actualizar información de un cliente en la base de datos

### Vehiculo
Representa un vehículo que se encuentra en la agencia de vehiculos. 
Contiene información como marca, modelo, año, color, tipo de vehículo, número de identificación y fecha de venta.
esta clase se encarga de manejar las transacciones de la base de datos relacionadas con el vehículo.
Ejemplo de transacciones:
- Agregar un vehículo a la base de datos
- Eliminar un vehículo de la base de datos
- Buscar un vehículo en la base de datos
- Actualizar información de un vehículo en la base de datos

### Venta
Representa una venta realizada por un cliente. Contiene información como fecha 
de venta, precio, cantidad y número de identificación del cliente.
esta clase se encarga de manejar las transacciones de la base de datos relacionadas con la venta.
Ejemplo de transacciones:
- Agregar una venta a la base de datos
- Eliminar una venta de la base de datos
- Buscar una venta en la base de datos
- Actualizar información de una venta en la base de datos

### Conexion
Representa una conexión a la base de datos. Contiene información 
como el nombre de la base de datos, el usuario y la contraseña. 
Esta clase se encarga de establecer la conexión con la base de datos y de manejar las transacciones de la misma.
Ejemplo de transacciones:
- Conectarse a la base de datos
- Desconectarse de la base de datos
- Obtener la conexión actual

## documetación
pyqt5 https://wiki.python.org/moin/PyQt
pyodbc https://pypi.org/project/pyodbc/
