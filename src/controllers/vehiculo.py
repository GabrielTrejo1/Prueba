from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from src.models.conexion import Conexion

class Vehiculos():
    def __init__(self):
        self.vehiculo = uic.loadUi("C:/Users/equipo/PycharmProjects/Trabajo-UTN/src/gui/vehiculos.ui")
        self.vehiculo.show()
        self.db = Conexion()

        self.initGui()

    def initGui(self):
        query = "SELECT * FROM Vehiculos"
        datos_vehiculos = self.db.execute_query_fetchall(query)

        self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
        self.vehiculo.btnAgregar.clicked.connect(self.nuevo_vehiculo)
        self.vehiculo.btnEliminar.clicked.connect(self.eliminar_vehiculo)
        self.vehiculo.tblVehiculos.itemDoubleClicked.connect(self.seleccionar_vehiculo)

        # Conectar la señal textChanged del campo de texto
        self.vehiculo.txtMarca.textChanged.connect(self.buscar_vehiculo)
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
        warning = QMessageBox.question(self.vehiculo, "Agregar Nuevo Vehiculo",
                                       "¿Está seguro de que desea agregar este vehiculo?",
                                       QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            # Validar antes de continuar
            if self.validar():
                marca = self.vehiculo.txtMarcaAdd.text().strip()
                modelo = self.vehiculo.txtModeloAdd.text().strip()
                color = self.vehiculo.txtColor.text().strip()
                carroceria = self.vehiculo.txtCarroceria.text().strip()
                combustible = self.vehiculo.cmbCombustible.currentText().strip()
                motor = self.vehiculo.txtMotor.text().strip()
                detalles = self.vehiculo.txtDetalles.text().strip()
                dominio = self.vehiculo.txtPatente.text().strip()

                query = (
                    "INSERT INTO Vehiculos (dominio, marca, modelo, motor, color, carroceria, tipo_combustible, detalles) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                )
                values = (dominio, marca, modelo, motor, color, carroceria, combustible, detalles)

                self.db.execute_query(query, values)
                QMessageBox.information(self.vehiculo, "Información", "Se ha registrado el vehículo")
                self.cargar_datos_vehiculos()
                # Limpiar campos después de agregar
                self.vehiculo.txtMarcaAdd.clear()
                self.vehiculo.txtModeloAdd.clear()
                self.vehiculo.txtColor.clear()
                self.vehiculo.txtCarroceria.clear()
                self.vehiculo.cmbCombustible.setCurrentIndex(0)
                self.vehiculo.txtMotor.clear()
                self.vehiculo.txtDetalles.clear()
                self.vehiculo.txtPatente.clear()

    def buscar_vehiculo(self):
        try:
            marca = self.vehiculo.txtMarca.text().strip().lower()
            query = "SELECT * FROM Vehiculos WHERE LOWER(Marca) LIKE ? OR LOWER(Modelo) LIKE ?"
            values = (f"{marca}%", f"{marca}%")
            datos_vehiculos = self.db.execute_query_fetchall(query, values)

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
                self.db.execute_query(query, vehiculo_id)
                QMessageBox.information(self.vehiculo, "Éxito", "Vehiculo eliminado con éxito.")
                self.cargar_datos_vehiculos()
            else:
                QMessageBox.warning(self.vehiculo, "Advertencia", "Seleccione un vehiculo para eliminar.")
        except Exception as e:
            QMessageBox.critical(self.vehiculo, "Error", f"No se pudo eliminar el vehiculo: {e}")

    def validar(self):
        marca = self.vehiculo.txtMarcaAdd.text().strip()
        modelo = self.vehiculo.txtModeloAdd.text().strip()
        color = self.vehiculo.txtColor.text().strip()
        carroceria = self.vehiculo.txtCarroceria.text().strip()
        combustible = self.vehiculo.cmbCombustible.currentText().strip()
        motor = self.vehiculo.txtMotor.text().strip()
        detalles = self.vehiculo.txtDetalles.text().strip()
        dominio = self.vehiculo.txtPatente.text().strip()

        # Verificar que todos los campos necesarios estén completos
        if not all([marca, modelo, color, carroceria, combustible, motor, detalles, dominio]):
            QMessageBox.warning(self.vehiculo, "Error", "Todos los campos son obligatorios.SI no posee informacion coloque 0")
            return False

        return True

    def seleccionar_vehiculo(self, item):
            row = item.row()
            self.vehiculo.txtMarcaAdd.setText(self.vehiculo.tblVehiculos.item(row, 1).text())
            self.vehiculo.txtModeloAdd.setText(self.vehiculo.tblVehiculos.item(row, 2).text())
            self.vehiculo.txtColor.setText(self.vehiculo.tblVehiculos.item(row, 3).text())
            self.vehiculo.txtPatente.setText(self.vehiculo.tblVehiculos.item(row, 4).text())
            self.vehiculo.txtMotor.setText(self.vehiculo.tblVehiculos.item(row, 5).text())
            self.vehiculo.txtCarroceria.setText(self.vehiculo.tblVehiculos.item(row, 6).text())
            self.vehiculo.cmbCombustible.setCurrentText(self.vehiculo.tblVehiculos.item(row, 7).text())
            self.vehiculo.txtDetalles.setText(self.vehiculo.tblVehiculos.item(row, 8).text())


