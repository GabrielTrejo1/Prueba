from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from models.conexion import Conexion
from config import base_path

class Vehiculos():
    def __init__(self):
        self.vehiculo = uic.loadUi(f"{base_path}/src/gui/vehiculos.ui")
        self.vehiculo.show()
        self.db = Conexion()
        self.id = None

        self.initGui()

    def initGui(self):
        self.cargar_datos_vehiculos()
        self.vehiculo.btnAgregar.clicked.connect(self.nuevo_vehiculo)
        self.vehiculo.btnEliminar.clicked.connect(self.eliminar_vehiculo)

        # Conectar la señal textChanged del campo de texto
        self.vehiculo.txtBuscar.textChanged.connect(self.cargar_datos_vehiculos)
        self.vehiculo.btnModificar.clicked.connect(self.modificar_vehiculo)

        # Conectar el doble clic para seleccionar un vehículo
        self.vehiculo.tblVehiculos.cellDoubleClicked.connect(self.seleccionar_vehiculo)

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
                self.limpiar_campos()

    def cargar_datos_vehiculos(self):
        try:
            buscar = self.vehiculo.txtBuscar.text().strip().lower()
            query = "SELECT ID, dominio, marca, modelo, color, motor, carroceria, detalles FROM Vehiculos WHERE marca LIKE ? OR modelo LIKE ? OR dominio LIKE ?"
            values = (f"{buscar}%", f"{buscar}%", f"{buscar}%")
            datos_vehiculos = self.db.execute_query_fetchall(query,values)

            # Limpiar la tabla antes de cargar nuevos datos
            self.vehiculo.tblVehiculos.setRowCount(0)
            self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
            for fila, item in enumerate(datos_vehiculos):
                for columna, valor in enumerate(item):
                    self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
        except Exception as e:
            QMessageBox.critical(self.vehiculo, "Error", f"No se pudo buscar el vehículo: {e}")

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
        # if not all([marca, modelo, color, carroceria, combustible, motor, detalles, dominio]):
        #     QMessageBox.warning(self.vehiculo, "Error", "Todos los campos son obligatorios. Si no posee informacion coloque 0")
        #     return False
        print("JAJAJAJA")

        return True

    def seleccionar_vehiculo(self):
        row = self.vehiculo.tblVehiculos.currentRow()
        self.id = self.vehiculo.tblVehiculos.item(row, 0).text()  # Guardar el ID del vehículo seleccionado
        self.vehiculo.txtMarcaAdd.setText(self.vehiculo.tblVehiculos.item(row, 1).text())
        self.vehiculo.txtModeloAdd.setText(self.vehiculo.tblVehiculos.item(row, 2).text())
        self.vehiculo.txtColor.setText(self.vehiculo.tblVehiculos.item(row, 3).text())
        self.vehiculo.txtPatente.setText(self.vehiculo.tblVehiculos.item(row, 4).text())
        if self.vehiculo.tblVehiculos.item(row, 5) != None:
          self.vehiculo.txtMotor.setText(self.vehiculo.tblVehiculos.item(row, 5).text())
        if self.vehiculo.tblVehiculos.item(row, 6) != None:
          self.vehiculo.txtCarroceria.setText(self.vehiculo.tblVehiculos.item(row, 6).text())
        if self.vehiculo.tblVehiculos.item(row, 7) != None:
          self.vehiculo.cmbCombustible.setCurrentText(self.vehiculo.tblVehiculos.item(row, 7).text())
        if self.vehiculo.tblVehiculos.item(row, 8) != None:
          self.vehiculo.txtDetalles.setText(self.vehiculo.tblVehiculos.item(row, 8).text())

    def limpiar_campos(self):
        self.vehiculo.txtMarcaAdd.clear()
        self.vehiculo.txtModeloAdd.clear()
        self.vehiculo.txtColor.clear()
        self.vehiculo.txtCarroceria.clear()
        self.vehiculo.cmbCombustible.setCurrentIndex(0)
        self.vehiculo.txtMotor.clear()
        self.vehiculo.txtDetalles.clear()
        self.vehiculo.txtPatente.clear()
        self.id = None

    def modificar_vehiculo(self):
        if self.id is not None:  # Verificar que un vehículo ha sido seleccionado
            warning = QMessageBox.question(self.vehiculo, "Modificar Vehículo",
                                       "¿Está seguro de que desea modificar este vehículo?",
                                       QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                try:
                    marca = self.vehiculo.txtMarcaAdd.text().strip()
                    modelo = self.vehiculo.txtModeloAdd.text().strip()
                    color = self.vehiculo.txtColor.text().strip()
                    dominio = self.vehiculo.txtPatente.text().strip()
                    motor = self.vehiculo.txtMotor.text().strip()
                    carroceria = self.vehiculo.txtCarroceria.text().strip()
                    combustible = self.vehiculo.cmbCombustible.currentText().strip()
                    detalles = self.vehiculo.txtDetalles.text().strip()

                    valid = self.validar()
                    if valid:
                        query = (
                            "UPDATE Vehiculos SET dominio = ?, marca = ?, modelo = ?, color = ?, motor = ?, "
                            "carroceria = ?, tipo_combustible = ?, detalles = ? WHERE id = ?"
                        )
                        values = (dominio, marca, modelo, color, motor, carroceria, combustible, detalles, self.id)
                        self.db.execute_query(query, values)
                        QMessageBox.information(self.vehiculo, "Éxito", "Se modificó el vehículo satisfactoriamente.")
                        self.cargar_datos_vehiculos()
                        self.limpiar_campos()  # Limpiar campos después de modificar
                except Exception as e:
                    QMessageBox.critical(self.vehiculo, "Error",
                                     f"Ha ocurrido un error al intentar modificar el vehículo: {e}")
        else:
            QMessageBox.warning(self.vehiculo, "Advertencia", "Seleccione un vehículo para modificar.")