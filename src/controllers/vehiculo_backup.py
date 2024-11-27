from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from models.conexion import Conexion
from config import base_path

class Vehiculos():
    def __init__(self):
        self.vehiculo = uic.loadUi(f"{base_path}/src/gui/vehiculos.ui")
        self.vehiculo.show()
        self.db = Conexion()

        self.initGui()

    def initGui(self):
        self.vehiculo.btnAgregar.clicked.connect(self.nuevo_vehiculo)
        self.vehiculo.btnEliminar.clicked.connect(self.eliminar_vehiculo)

        # Conectar la señal textChanged del campo de texto
        self.vehiculo.txtBuscar.textChanged.connect(self.cargar_datos_vehiculos)
        self.cargar_datos_vehiculos()

    def cargar_datos_vehiculos(self):
        buscar = self.vehiculo.txtBuscar.text().strip().lower()
        query = "SELECT ID, dominio, marca, modelo, color, motor, carroceria, tipo_combustible, detalles FROM Vehiculos WHERE LOWER(marca) LIKE ? OR LOWER(modelo) LIKE ? OR LOWER(dominio) LIKE ? ORDER BY ID DESC"
        values = (f"{buscar}%", f"{buscar}%", f"{buscar}%")
        datos_vehiculos = self.db.execute_query_fetchall(query,values)

        self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
        for fila, item in enumerate(datos_vehiculos):
            for columna, valor in enumerate(item):
                self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
        # self.vehiculo.tblVehiculos.resizeColumnsToContents()
        self.vehiculo.tblVehiculos.setColumnWidth(0, 16)
        self.vehiculo.tblVehiculos.setColumnWidth(1, 64)
        self.vehiculo.tblVehiculos.setColumnWidth(5, 70)

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
                    "INSERT INTO Vehiculos (dominio, marca, modelo, motor, color, carroceria, tipo_combustible, detalles, disponible) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)"
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









