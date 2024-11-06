from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from src.models.conexion import Conexion

class EstadoVehiculos():
    def __init__(self):
        self.estadoVehiculos = uic.loadUi("./gui/estado_vehiculo2.ui")
        self.estadoVehiculos.show()
        self.db = Conexion()
        self.initGui()
        self.estadoVehiculos.dtpFechaService.setDate(QDate.currentDate())

    def initGui(self):
        self.cargar_datos_vehiculos()
        self.cargar_datos_estado()
        self.estadoVehiculos.tblVehiculos.cellDoubleClicked.connect(self.seleccionar_vehiculo)
        self.estadoVehiculos.btnEditarEstado.clicked.connect(self.editar_estado)
        self.estadoVehiculos.btnGuardar.clicked.connect(self.guardar_estado)

    def cargar_datos_vehiculos(self):
        query = "select ID, dominio, marca, modelo, color from VEHICULOS"
        datos_vehiculos = self.db.execute_query_fetchall(query)

        self.estadoVehiculos.tblVehiculos.setRowCount(len(datos_vehiculos))
        for fila, item in enumerate(datos_vehiculos):
            for columna, valor in enumerate(item):
                self.estadoVehiculos.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def cargar_datos_estado(self):
        query = "SELECT * FROM ESTADOS_VEHICULOS"
        datos_estado = self.db.execute_query_fetchall(query)

        self.estadoVehiculos.tblEstVehiculos.setRowCount(len(datos_estado))
        for fila, item in enumerate(datos_estado):
            for columna, valor in enumerate(item):
                self.estadoVehiculos.tblEstVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def seleccionar_vehiculo(self):
        row = self.estadoVehiculos.tblVehiculos.currentRow()
        self.estadoVehiculos.txtID.setText(self.estadoVehiculos.tblVehiculos.item(row, 0).text())
        self.estadoVehiculos.txtDominio.setText(self.estadoVehiculos.tblVehiculos.item(row, 1).text())
        self.estadoVehiculos.txtMarca.setText(self.estadoVehiculos.tblVehiculos.item(row, 2).text())
        self.estadoVehiculos.txtModelo.setText(self.estadoVehiculos.tblVehiculos.item(row, 3).text())
        self.estadoVehiculos.txtColor.setText(self.estadoVehiculos.tblVehiculos.item(row, 4).text())

    def editar_estado(self):
        # VER ESTADO SIN ROW SELECCIONADA

        self.estadoVehiculos.txtEstadoGral.setEnabled(True)
        self.estadoVehiculos.cmbDeuda.setEnabled(True)
        self.estadoVehiculos.cmbPapeles.setEnabled(True)
        self.estadoVehiculos.txtKilometraje.setEnabled(True)
        self.estadoVehiculos.dtpFechaService.setEnabled(True)
        self.estadoVehiculos.btnGuardar.setEnabled(True)

        query = (
            f"select id_vehiculos from ESTADOS_VEHICULOS where id_vehiculos = {self.estadoVehiculos.txtID.text()}"
        )
        resquery = self.db.execute_query_fetchall(query)

        if resquery == []:
            # INSERT
            print("1")
        else:
            # CARGAR DATOS EN TXT BOX + UPDATE
            print("2")

    def guardar_estado(self):
        query = (
            f"select id_vehiculos from ESTADOS_VEHICULOS where id_vehiculos = {self.estadoVehiculos.txtID.text()}"
        )

        evomorales = self.db.execute_query_fetchall(query)

        # MOVER INSERT O UPDATE ACA

        print(evomorales[0][0])
        print(self.estadoVehiculos.txtID.text())

# TO-DO
# OCULTAR ID
# self.ventas.txtIDVehiculo.setVisible(False)
# EN INITGUI
#