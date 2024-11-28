from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from models.conexion import Conexion
from config import base_path

class EstadoVehiculos():
    def __init__(self):
        self.estadoVehiculos = uic.loadUi(f"{base_path}/src/gui/estado_vehiculo2.ui")
        self.estadoVehiculos.show()
        self.db = Conexion()
        self.initGui()
        self.estadoVehiculos.dtpFechaService.setDate(QDate.currentDate())

    def initGui(self):
        self.cargar_datos_vehiculos()
        self.cargar_datos_estado()
        self.estadoVehiculos.tblVehiculos.cellDoubleClicked.connect(self.seleccionar_vehiculo)
        self.estadoVehiculos.tblEstVehiculos.cellDoubleClicked.connect(self.seleccionar_est_vehiculo)
        self.estadoVehiculos.btnEditarEstado.clicked.connect(self.editar_estado)
        self.estadoVehiculos.btnGuardar.clicked.connect(self.guardar_estado)
        self.estadoVehiculos.txtID.setVisible(False)

        self.estadoVehiculos.tblVehiculos.setColumnHidden(0, True)
        self.estadoVehiculos.tblEstVehiculos.setColumnHidden(1, True)
        self.estadoVehiculos.tblEstVehiculos.setColumnHidden(2, True)

    def cargar_datos_vehiculos(self):
        query = "select ID, dominio, marca, modelo, color from VEHICULOS"
        datos_vehiculos = self.db.execute_query_fetchall(query)

        self.estadoVehiculos.tblVehiculos.setRowCount(len(datos_vehiculos))
        for fila, item in enumerate(datos_vehiculos):
            for columna, valor in enumerate(item):
                self.estadoVehiculos.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))

    def cargar_datos_estado(self):
        query = ("select V.dominio, EV.id, EV.id_vehiculos, EV.estado_general, EV.deudas, EV.papeles, EV.kilometraje, EV.fecha_estado from VEHICULOS as V "
                 "join ESTADOS_VEHICULOS as EV on V.ID = EV.id_vehiculos")
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

        self.estadoVehiculos.btnEditarEstado.setEnabled(True)

    def seleccionar_est_vehiculo(self):
        row = self.estadoVehiculos.tblEstVehiculos.currentRow()
        self.estadoVehiculos.txtEstadoGral.setText(self.estadoVehiculos.tblEstVehiculos.item(row, 3).text())
        self.estadoVehiculos.txtKilometraje.setText(self.estadoVehiculos.tblEstVehiculos.item(row, 6).text())

        # Deudas
        if self.estadoVehiculos.tblEstVehiculos.item(row, 4).text() == 'No':
            self.estadoVehiculos.cmbDeuda.setCurrentIndex(0)
        else:
            self.estadoVehiculos.cmbDeuda.setCurrentIndex(1)

        # Papeles
        if self.estadoVehiculos.tblEstVehiculos.item(row, 5).text() == 'Si':
            self.estadoVehiculos.cmbPapeles.setCurrentIndex(0)
        else:
            self.estadoVehiculos.cmbPapeles.setCurrentIndex(1)

    def editar_estado(self):
        self.estadoVehiculos.tblEstVehiculos.setEnabled(True)
        self.estadoVehiculos.txtEstadoGral.setEnabled(True)
        self.estadoVehiculos.cmbDeuda.setEnabled(True)
        self.estadoVehiculos.cmbPapeles.setEnabled(True)
        self.estadoVehiculos.txtKilometraje.setEnabled(True)
        self.estadoVehiculos.dtpFechaService.setEnabled(True)
        self.estadoVehiculos.btnGuardar.setEnabled(True)

    def guardar_estado(self):
        query = (
            f"select id_vehiculos from ESTADOS_VEHICULOS where id_vehiculos = {self.estadoVehiculos.txtID.text()}"
        )
        resquery = self.db.execute_query_fetchall(query)

        id_vehiculos = int(self.estadoVehiculos.txtID.text())
        estado_general = self.estadoVehiculos.txtEstadoGral.text()
        deudas = self.estadoVehiculos.cmbDeuda.currentText()
        papeles = self.estadoVehiculos.cmbPapeles.currentText()
        kilometraje = int(self.estadoVehiculos.txtKilometraje.text())
        fecha_estado = self.estadoVehiculos.dtpFechaService.date().toString("yyyy-MM-dd")

        if resquery == []:
            # INSERT
            query = ("INSERT INTO ESTADOS_VEHICULOS (id_vehiculos, estado_general, deudas, papeles, kilometraje, fecha_estado)"
                     " VALUES(?,?,?,?,?,?)")
            values = (id_vehiculos, estado_general, deudas, papeles, kilometraje, fecha_estado)

            self.db.execute_query(query, values)
            self.cargar_datos_estado()
        else:
            estado_general = self.estadoVehiculos.txtEstadoGral.text()
            deudas = self.estadoVehiculos.cmbDeuda.currentText()
            papeles = self.estadoVehiculos.cmbPapeles.currentText()
            kilometraje = self.estadoVehiculos.txtKilometraje.text()
            fecha_estado = self.estadoVehiculos.dtpFechaService.date().toString("yyyy-MM-dd")
            id_vehiculos = int(self.estadoVehiculos.txtID.text())

            query = (
                "UPDATE ESTADOS_VEHICULOS SET estado_general = ?, deudas = ?, papeles = ?, kilometraje = ?, fecha_estado = ?"
                " WHERE id_vehiculos = ?"
            )
            values = (estado_general, deudas, papeles, kilometraje, fecha_estado, id_vehiculos)

            self.db.execute_query(query, values)
            self.cargar_datos_estado()