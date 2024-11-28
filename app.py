from PyQt5.QtWidgets import QApplication
from src.controllers.inicio import Inicio
from src.controllers.cliente import Clientes
from src.controllers.ventas import Ventas
from src.controllers.vehiculo import Vehiculos
from src.controllers.boleto import Boleto


class App():
    def __init__(self):
        self.App = QApplication([])
        self.inicio = Inicio()
        self.App.exec()