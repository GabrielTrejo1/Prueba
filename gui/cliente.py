from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from src.conexion import Conexion

class Clientes():
    def __init__(self):
        self.cliente = uic.loadUi("gui\cliente.ui")
        self.cliente.show()
        self.db = Conexion().conectar()
        self.cursor = self.db.cursor()

        self.cargar_datos_cliente()
        
    def cargar_datos_cliente(self):
        query="SELECT * FROM Clientes"
        res = self.cursor.execute(query)
        datos_clientes= res.fetchall()
        self.cliente.tblClientes.setRowCount(len(datos_clientes))
        fila = 0
        for item in datos_clientes:
            self.cliente.tblClientes.setItem(fila,0,QTableWidgetItem(str(item[0])))
            self.cliente.tblClientes.setItem(fila,1,QTableWidgetItem(str(item[1])))
            self.cliente.tblClientes.setItem(fila,2,QTableWidgetItem(str(item[2])))
            self.cliente.tblClientes.setItem(fila,3,QTableWidgetItem(str(item[3])))
            self.cliente.tblClientes.setItem(fila,4,QTableWidgetItem(str(item[4])))
            self.cliente.tblClientes.setItem(fila,5,QTableWidgetItem(str(item[5])))
            fila +=1
            
    def valid(self):
        pass
    
    def nuevo_cliente(self):
        pass
    
        
        