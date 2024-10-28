from PyQt5.QtWidgets import QApplication
from gui.cliente import Clientes
from gui.vehiculo import Vehiculos
class App():
    def __init__(self):
        self.App = QApplication([])
        self.cliente = Clientes()
        self.vehiculo = Vehiculos()
        self.App.exec()