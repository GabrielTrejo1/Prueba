from PyQt5 import uic
from controllers.cliente import Clientes
from models.conexion import Conexion
from PyQt5.QtCore import QDate

class Inicio():
    def __init__(self):
        self.inicio = uic.loadUi("gui/inicio.ui")
        self.inicio.show()

        self.initGui()

    def initGui(self):
        self.inicio.btnClientes.clicked.connect(lambda: self.abrirClientes())

    def abrirClientes(self):
        self.clientes = uic.loadUi("gui/cliente.ui")
        self.clientes.show()
