from PyQt5 import uic
from PyQt5.QtWidgets import QDesktopWidget
from controllers.cliente import Clientes
from controllers.vehiculo import Vehiculos
from controllers.ventas import Ventas
from controllers.estadoVehiculos import EstadoVehiculos
from config import base_path

class Inicio():
    def __init__(self):
        self.inicio = uic.loadUi(f"{base_path}/src/gui/inicio.ui")
        self.center()
        self.inicio.show()
        self.initGui()

    def initGui(self):
        self.inicio.btnClientes.clicked.connect(self.abrirClientes)
        self.inicio.btnVehiculos.clicked.connect(self.abrirVehiculos)
        self.inicio.btnVentas.clicked.connect(self.abrirVentas)
        self.inicio.btnEstadoVehiculo.clicked.connect(self.abrirEstadoVehiculos)
        
    def center(self):
        qr = self.inicio.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.inicio.move(qr.topLeft())

    def abrirVehiculos(self):
        self.vehiculos = Vehiculos()

    def abrirClientes(self):
        self.clientes = Clientes()
    
    def abrirVentas(self):
        self.ventas = Ventas()

    def abrirEstadoVehiculos(self):
        self.estadovehiculos = EstadoVehiculos()