import pyodbc

class Conexion():
    def __init__(self):
        try:
            self.con = pyodbc.connect('DRIVER={SQL Server};SERVER=Ale-Notebook\SQLEXPRESS;DATABASE=AGENCIA_AC;Trusted_Connection=Yes;')
        except Exception as e:
            print(e)
        
    def conectar(self):
        return self.con
