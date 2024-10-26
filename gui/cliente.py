from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from PyQt5.QtCore import QDate
from src.conexion import Conexion

class Clientes():
    def __init__(self):
        self.cliente = uic.loadUi("gui\cliente.ui")
        self.cliente.show()
        self.db = Conexion().conectar()
        self.cursor = self.db.cursor()

        self.initGui()
        

    def initGui(self):
        query="SELECT day(GETDATE()),month(GETDATE()),year(GETDATE())"
        res = self.cursor.execute(query)
        fecha_hoy= res.fetchall()
        self.cliente.dtpFechaRegistro.setDate(QDate(fecha_hoy[0][2],fecha_hoy[0][1],fecha_hoy[0][0]))
        self.cargar_datos_cliente()
        self.cliente.btnGuardar.clicked.connect(self.nuevo_cliente)
        
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
        try:
            nombre = self.cliente.txtNombre.text()
            correo = self.cliente.txtCorreo.text()
            telefono = self.cliente.txtTelefono.text()
            direccion = self.cliente.txtDireccion.text()
            fechaRegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")
            
            query = "INSERT INTO Clientes (nombre, correo, telefono, direccion, fecha_registro) VALUES(?,?,?,?,?)"
            values = (nombre,correo,telefono,direccion,fechaRegistro)
            self.cursor.execute(query,values)
            self.cursor.commit()
            print("Se creo un nuevo cliente")
        except Exception as e:
            print("No se pudo insertar el cliente:", e)
        finally:
            self.cursor.close()

        