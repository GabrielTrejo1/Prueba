from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from src.conexion import Conexion


class Clientes():
    def __init__(self):
        self.cliente = uic.loadUi("gui\\cliente.ui")
        self.cliente.show()
        self.db = Conexion().conectar()
        self.cursor = self.db.cursor()

        self.initGui()

    def initGui(self):
        query = "SELECT day(GETDATE()), month(GETDATE()), year(GETDATE())"
        res = self.cursor.execute(query)
        fecha_hoy = res.fetchone()
        self.cliente.dtpFechaRegistro.setDate(QDate(fecha_hoy[2], fecha_hoy[1], fecha_hoy[0]))
        self.cargar_datos_cliente()

        self.cliente.btnGuardar.clicked.connect(self.nuevo_cliente)
        self.cliente.btnBuscar.clicked.connect(self.buscar_cliente)
        self.cliente.btnEliminar.clicked.connect(self.eliminar_cliente)

    def cargar_datos_cliente(self):
        query = "SELECT * FROM Clientes"
        res = self.cursor.execute(query)
        datos_clientes = res.fetchall()

        self.cliente.tblClientes.setRowCount(len(datos_clientes))
        for fila, item in enumerate(datos_clientes):
            for columna, valor in enumerate(item):
                self.cliente.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def nuevo_cliente(self):
        try:
            nombre = self.cliente.txtNombre.text()
            correo = self.cliente.txtCorreo.text()
            telefono = self.cliente.txtTelefono.text()
            direccion = self.cliente.txtDireccion.text()
            fecharegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")

            query = "INSERT INTO Clientes (nombre, correo, telefono, direccion, fecha_registro) VALUES(?,?,?,?,?)"
            values = (nombre, correo, telefono, direccion, fecharegistro)
            self.cursor.execute(query, values)
            self.db.commit()  # Cambia a self.db.commit()
            QMessageBox.information(self.cliente, "Éxito", "Cliente creado con éxito.")
            self.cargar_datos_cliente()  # Recargar datos
        except Exception as e:
            QMessageBox.critical(self.cliente, "Error", f"No se pudo insertar el cliente: {e}")

    def buscar_cliente(self):
        pass

    def eliminar_cliente(self):
        try:
            row = self.cliente.tblClientes.currentRow()
            if row >= 0:
                cliente_id = self.cliente.tblClientes.item(row,
                                                           0).text()  # Asumiendo que el ID del cliente está en la primera columna
                query = "DELETE FROM Clientes WHERE id_cliente = ?"
                self.cursor.execute(query, (cliente_id,))
                self.db.commit()
                QMessageBox.information(self.cliente, "Éxito", "Cliente eliminado con éxito.")
                self.cargar_datos_cliente()  # Recargar datos
            else:
                QMessageBox.warning(self.cliente, "Advertencia", "Seleccione un cliente para eliminar.")
        except Exception as e:
            QMessageBox.critical(self.cliente, "Error", f"No se pudo eliminar el cliente: {e}")

