from PyQt5.QtWidgets import QApplication
from controllers.cliente import Clientes
from controllers.inicio import Inicio
from controllers.vehiculo import Vehiculos
from controllers.ventas import Ventas


class App():
    def __init__(self):
        self.App = QApplication([])
        #self.cliente = Clientes()
        #self.vehiculo = Vehiculos()
        #self.venta = Ventas()
        self.inicio = Inicio()
        self.App.exec()