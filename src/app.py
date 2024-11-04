from PyQt5.QtWidgets import QApplication
from controllers.inicio import Inicio


class App():
    def __init__(self):
        self.App = QApplication([])
        self.inicio = Inicio()
        self.App.exec()