from PyQt5.QtWidgets import QApplication
from gui.cliente import Clientes
from gui.vehiculo import Vehiculos
from gui.inicio import Inicio
class App():
   def __init__(self):
       self.App = QApplication([])
       self.inicio = Inicio()  # Solo la ventana de inicio
       self.App.exec()

