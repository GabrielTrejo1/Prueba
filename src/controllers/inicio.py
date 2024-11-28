from PyQt5 import uic
from PyQt5 import QtWidgets
from src.controllers.cliente import Clientes
from src.controllers.vehiculo import Vehiculos
from src.controllers.ventas import Ventas
from src.controllers.boleto import Boleto


class Inicio():
    def __init__(self):
        self.inicio = uic.loadUi("C:/Users/equipo/PycharmProjects/Trabajo-UTN/src/gui/inicio.ui")  # Cargar la interfaz
        self.ventas = None
        self.vehiculos = None
        self.clientes = None
        self.boleto = None
        self.initGui()

    def initGui(self):
        self.inicio.btnServicios.clicked.connect(self.abrirBoleto)
        self.inicio.btnClientes.clicked.connect(self.abrirClientes)
        self.inicio.btnVehiculos.clicked.connect(self.abrirVehiculos)
        self.inicio.btnVentas.clicked.connect(self.abrirVentas)

        self.inicio.show()


    def abrirBoleto(self): #Abrir venta de boletos
        self.boleto = Boleto()

    def abrirVehiculos(self):
        self.vehiculos = Vehiculos()

    def abrirClientes(self):
        self.clientes = Clientes()

    def abrirVentas(self):
        self.ventas = Ventas()