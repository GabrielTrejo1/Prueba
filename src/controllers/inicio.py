from PyQt5 import uic
from controllers.cliente import Clientes
from controllers.estadoVehiculos import EstadoVehiculos
from controllers.vehiculo import Vehiculos
from controllers.ventas import Ventas
from config import base_path
#from controllers.estadoVehiculos import EstadoVehiculos

class Inicio():
    def __init__(self):
        self.inicio = uic.loadUi(f"{base_path}/src/gui/inicio.ui")
        self.inicio.show()

        self.initGui()

    def initGui(self):
        self.inicio.btnClientes.clicked.connect(self.abrirClientes)
        self.inicio.btnVehiculos.clicked.connect(self.abrirVehiculos)
        self.inicio.btnVentas.clicked.connect(self.abrirVentas)
        self.inicio.btnEstadoVehiculo.clicked.connect(self.abrirEstadoVehiculos)

    def abrirVehiculos(self):
        self.vehiculos = Vehiculos()

    def abrirClientes(self):
        self.clientes = Clientes()
    
    def abrirVentas(self):
        self.ventas = Ventas()
        
    def abrirEstadoVehiculos(self):
        self.estadovehiculos = EstadoVehiculos()