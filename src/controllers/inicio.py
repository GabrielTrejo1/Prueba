from PyQt5 import uic
from src.controllers.cliente import Clientes
from src.models.conexion import Conexion
from PyQt5.QtCore import QDate
from src.controllers.vehiculo import Vehiculos
from src.controllers.ventas import Ventas

class Inicio():
    def __init__(self):
        self.ventas = None
        self.vehiculos = None
        self.clientes = None
        self.inicio = uic.loadUi("C:/Users/equipo/PycharmProjects/Trabajo-UTN/src/gui/inicio_02.ui")
        self.inicio.show()

        self.initGui()

    def initGui(self):
        self.inicio.btnClientes.clicked.connect(self.abrirClientes)
        self.inicio.btnVehiculos.clicked.connect(self.abrirVehiculos)
        self.inicio.btnVentas.clicked.connect(self.abrirVentas)

    def abrirVehiculos(self):
        self.vehiculos = Vehiculos()

    def abrirClientes(self):
        self.clientes = Clientes()
    
    def abrirVentas(self):
        self.ventas = Ventas()