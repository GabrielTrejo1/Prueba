from PyQt5 import uic
from gui.cliente import Clientes
from src.conexion import Conexion
from PyQt5.QtCore import QDate

class Inicio():
    def __init__(self):
        self.vehiculos = None
        self.clientes = None
        self.inicio = uic.loadUi("gui/inicio.ui")
        self.inicio.show()

        self.initGui()

    def initGui(self):
        self.inicio.btnClientes.clicked.connect(lambda: self.abrirClientes())
        self.inicio.btnVehiculos.clicked.connect(lambda: self.abrirVehiculos())

    def abrirVehiculos(self):
        self.vehiculos = uic.loadUi("gui/vehiculos.ui")
        self.vehiculos.show()

    def abrirClientes(self):
        self.clientes = uic.loadUi("gui/cliente.ui")
        self.clientes.show()
