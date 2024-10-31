from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from models.conexion import Conexion

class Ventas():
    def __init__(self):
        self.venta = uic.loadUi("C:/Users/equipo/PycharmProjects/Trabajo-UTN/src/gui/ventas.ui")
        self.venta.show()
        self.db = Conexion('DRIVER={SQL Server};SERVER=DESKTOP-PM1QNE7\SQLEXPRESS;DATABASE=AGENCIA_AC;Trusted_Connection=Yes;')
        
    def initGui(self):
        pass
    
    def cargar_clientes(self):
        #Llenar la tabla tblClientes con los datos de la BD
        pass
    
    def cargar_vehiculos(self):
        #Llenar la tabla tblVehiculos con los datos de la BD
        pass
    
    def cargar_ventas(self):
        #Llenar la tabla tblVentas con los datos de la BD
        pass
    
    def buscar_ventas(self):
        #Buscar ventas igual que en clientes
        pass
    
    def buscar_clientes(self):
        #Buscar cliente igual que en clientes
        pass
    
    def buscar_vehiculos(self):
        #Buscar vehiculos igual que en clientes
        pass
    
    def valid(self):
        #Comprobar que se alla seleccionado un cliente y un vehiculo
        #Comprobar que el precio de venta no sea menor a 0
        # ? Comprobar que el vehiculo no este vendido
        pass
    
    def generar_venta(self):
        #QMessageBox para confirmar la creación de la venta
        #Insert de la venta
        pass
    