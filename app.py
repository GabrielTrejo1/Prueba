from PyQt5.QtWidgets import QApplication
from gui.cliente import Clientes
from gui.ventas import Ventas

class App():
    def __init__(self):
        self.App = QApplication([])
        # self.cliente = Clientes()
        self.ventas = Ventas()
        self.App.exec()