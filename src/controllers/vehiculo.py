from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from src.models.conexion import Conexion

class Vehiculos():
    def __init__(self):
        self.vehiculo = uic.loadUi("./gui/vehiculos.ui")
        self.vehiculo.show()
        self.db = Conexion()

        self.initGui()

    def initGui(self):
        query = "SELECT * FROM Vehiculos"
        datos_vehiculos = self.db.execute_query_fetchall(query)

        self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
        self.vehiculo.btnAgregar.clicked.connect(self.nuevo_vehiculo)
        self.vehiculo.btnEliminar.clicked.connect(self.eliminar_vehiculo)
        self.vehiculo.btnBuscar.clicked.connect(self.buscar_vehiculo)

        # Conectar la señal textChanged del campo de texto
        self.vehiculo.txtMarca.textChanged.connect(self.buscar_vehiculo)
        self.vehiculo.txtModelo.textChanged.connect(self.buscar_vehiculo)
        for fila, item in enumerate(datos_vehiculos):
            for columna, valor in enumerate(item):
                self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def cargar_datos_vehiculos(self):
        query = "SELECT * FROM Vehiculos"
        datos_vehiculos = self.db.execute_query_fetchall(query)

        self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
        for fila, item in enumerate(datos_vehiculos):
            for columna, valor in enumerate(item):
                self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def nuevo_vehiculo(self):
        try:
            marca = self.vehiculo.txtMarcaAdd.text()
            modelo = self.vehiculo.txtModeloAdd.text()
            color = self.vehiculo.txtColor.text()
            carroceria = self.vehiculo.txtCarroceria.text()
            combustible = self.vehiculo.cmbCombustible.currentText()
            motor = self.vehiculo.txtMotor.text()
            detalles = self.vehiculo.txtDetalles.text()
            dominio = self.vehiculo.txtPatente.text()

            query = ("INSERT INTO Vehiculos (dominio, marca, modelo, motor, color, carroceria, tipo_combustible, detalles)"
                     " VALUES(?,?,?,?,?,?,?,?)")
            values = (dominio, marca, modelo, motor, color, carroceria, combustible, detalles)
            self.db.execute_query(query,values)
            QMessageBox.information(self.vehiculo, "Información", "Se ha registrado el vehículo")
            self.cargar_datos_vehiculos()
        except Exception as e:
            QMessageBox.critical(self.vehiculo, "Error", str(e))

    def buscar_vehiculo(self):
        try:
            marca = self.vehiculo.txtMarca.text().strip().lower()
            modelo = self.vehiculo.txtModelo.text().strip().lower()
            query = "SELECT * FROM Vehiculos WHERE Marca LIKE ? AND Modelo LIKE ?"
            values = (f"{marca}%", f"{modelo}%")
            datos_vehiculos = self.db.execute_query_fetchall(query,values)

              # Limpiar la tabla antes de cargar nuevos datos
            self.vehiculo.tblVehiculos.setRowCount(0)

            self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
            for fila, item in enumerate(datos_vehiculos):
                for columna, valor in enumerate(item):
                    self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
        except Exception as e:
            QMessageBox.critical(self.vehiculo, "Error", f"No se pudo buscar el vehiculo: {e}")

    def eliminar_vehiculo(self):
        try:
            row = self.vehiculo.tblVehiculos.currentRow()
            if row >= 0:
                vehiculo_id = self.vehiculo.tblVehiculos.item(row, 0).text()
                query = "DELETE FROM Vehiculos WHERE ID = ?"
                self.db.execute_query(query,vehiculo_id)
                QMessageBox.information(self.vehiculo, "Éxito", "Vehiculo eliminado con éxito.")
                self.cargar_datos_vehiculos()
            else:
                QMessageBox.warning(self.vehiculo, "Advertencia", "Seleccione un vehiculo para eliminar.")
        except Exception as e:
            QMessageBox.critical(self.vehiculo, "Error", f"No se pudo eliminar el vehiculo: {e}")







