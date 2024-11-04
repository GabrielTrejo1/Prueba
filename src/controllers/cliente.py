from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from PyQt5.QtCore import QDate
from models.conexion import Conexion
from config import base_path

class Clientes():
    def __init__(self):
        self.cliente = uic.loadUi(f"{base_path}/src/gui/cliente.ui")
        self.cliente.show()
        self.db = Conexion()
        self.insert_update = False  #False = Insert , True = Update
        self.id_cliente = "" #Esta variable va a almacenar el ID del cliente que queremos modificar
        self.initGui()
        
    def initGui(self): #Func. de inicio(lo que esta en esta funcion se va a ejecutar al iniciar el programa)
        self.cargar_datos_cliente()
        self.cliente.dtpFechaHasta.setDate(QDate.currentDate())
        self.cliente.dtpFechaRegistro.setDate(QDate.currentDate())
        self.cliente.btnGuardar.clicked.connect(self.guardar_cliente)
        self.cliente.btnEliminar.clicked.connect(self.eliminar_cliente)
        self.cliente.txtBuscar.textChanged.connect(self.cargar_datos_cliente)
        self.cliente.dtpFechaDesde.dateChanged.connect(self.cargar_datos_cliente)
        self.cliente.dtpFechaHasta.dateChanged.connect(self.cargar_datos_cliente)
        self.cliente.checkFecha.clicked.connect(self.cargar_datos_cliente)
        self.cliente.btnModificar.clicked.connect(self.llenar_txtBox)
        self.cliente.btnCancelar.clicked.connect(self.cancelar_modificar)
        self.cliente.lblModificar.setVisible(False)
        # self.cliente.stateChanged.connect(self.cargar_datos_cliente)

    def cargar_datos_cliente(self):
        try:
            if self.cliente.checkFecha.isChecked():
                desde = self.cliente.dtpFechaDesde.date().toString("yyyy-MM-dd")
                hasta = self.cliente.dtpFechaHasta.date().toString("yyyy-MM-dd")
                buscar = self.cliente.txtBuscar.text().lower()
                buscar = self.cliente.txtBuscar.text().lower()
                query = "SELECT ID, nombre, DNI, correo, telefono, direccion, fecha_registro FROM Clientes WHERE (LOWER(nombre) LIKE ? OR LOWER(nombre) LIKE ? OR LOWER(DNI) LIKE ?) AND fecha_registro BETWEEN ? AND ? ORDER BY ID DESC"
                values = (f"{buscar}%",f"% {buscar}%", f"%{buscar}%", desde, hasta)
                datos_clientes = self.db.execute_query_fetchall(query,values)
            else:
                buscar = self.cliente.txtBuscar.text().lower()
                query = "SELECT ID, nombre, DNI, correo, telefono, direccion, fecha_registro FROM Clientes WHERE LOWER(nombre) LIKE ? OR LOWER(nombre) LIKE ? OR LOWER(DNI) LIKE ? ORDER BY ID DESC"
                values = (f"{buscar}%",f"% {buscar}%", f"%{buscar}%")
                datos_clientes = self.db.execute_query_fetchall(query,values)
            
            # Llenar la tabla con los nuevos resultados
            self.cliente.tblClientes.setRowCount(len(datos_clientes))
            for fila, item in enumerate(datos_clientes):
                for columna, valor in enumerate(item):
                    self.cliente.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
            self.cliente.tblClientes.resizeColumnsToContents() #Ajustar las columnas al tamaño del mayor elemento.
            self.cliente.tblClientes.verticalHeader().setVisible(False) #Ocultar indices de las filas.
        except Exception as e:
            QMessageBox.critical(self.cliente, "Error", f"No se pudo buscar el cliente: {e}")
            
    def nuevo_cliente(self):
        confirm = QMessageBox.question(self.cliente, "Agregar Nuevo Cliente", "¿Está seguro de que desea agregar este cliente?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            nombre = self.cliente.txtNombre.text()
            dni = self.cliente.txtDNI.text()
            correo = self.cliente.txtCorreo.text()
            telefono = self.cliente.txtTelefono.text()
            direccion = self.cliente.txtDireccion.text()
            fechaRegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")
            valid = self.valid()
            if valid:
                query = "INSERT INTO Clientes (nombre, DNI, correo, telefono, direccion, fecha_registro, estado) VALUES(?,?,?,?,?,?,1)"
                values = (nombre,dni,correo,telefono,direccion,fechaRegistro)
                
                self.db.execute_query(query, values)
                QMessageBox.information(self.cliente,"Cliente Agregado","Cliente agregado con éxito.")
                self.cargar_datos_cliente()
                self.cliente.txtNombre.clear()
                self.cliente.txtDNI.clear()
                self.cliente.txtCorreo.clear()
                self.cliente.txtTelefono.clear()
                self.cliente.txtDireccion.clear()
                self.cliente.dtpFechaRegistro.setDate(QDate.currentDate())
    
    def eliminar_cliente(self): #Para eliminar un cliente se debe seleccionar una fila y luego pulsar el boton Eliminar.
        selected_row = self.cliente.tblClientes.currentRow()

        if selected_row < 0:  # Verificar si no hay fila seleccionada
            QMessageBox.warning(self.cliente, "Advertencia", "Por favor, seleccione un cliente para eliminar.")
            return
        # Confirmar eliminación
        confirm = QMessageBox.question(self.cliente, "Confirmar Eliminación", "¿Está seguro de que desea eliminar este cliente?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
                # Eliminar la fila seleccionada
            try:
                id_cliente=self.cliente.tblClientes.item(selected_row,0)
                query = "DELETE FROM Clientes WHERE ID = ?"
                values = int(id_cliente.text())
                self.db.execute_query(query,values)
                self.cliente.tblClientes.removeRow(selected_row)
                QMessageBox.information(self.cliente, "Éxito", "Cliente eliminado exitosamente.")
            except Exception as e:
                print("Error al eliminar el cliente: ",e)
                QMessageBox.information(self.cliente, "Error", "No se pudo eliminar el cliente.")
    
    def llenar_txtBox(self): 
        selected_row = self.cliente.tblClientes.currentRow()
        if selected_row < 0:  # Verificar si no hay fila seleccionada
            QMessageBox.warning(self.cliente, "Advertencia", "Por favor, seleccione un cliente para modificar.")
            return
        # Confirmar modificación
        confirm = QMessageBox.question(self.cliente, "Confirmar Modificación", "¿Está seguro de que desea modifiar el cliente seleccionado?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.insert_update = True #Cambio el estado para que al apretar el boton Guadar, se genere un Update
            self.cliente.btnModificar.setEnabled(False)
            self.cliente.dtpFechaRegistro.setEnabled(False)
            self.id_cliente = self.cliente.tblClientes.item(selected_row,0).text() #Guardo el ID del Cliente que quiero Modificar
            self.cliente.txtNombre.setText(self.cliente.tblClientes.item(selected_row,1).text())
            self.cliente.txtDNI.setText(self.cliente.tblClientes.item(selected_row,2).text())
            self.cliente.txtCorreo.setText(self.cliente.tblClientes.item(selected_row,3).text())
            self.cliente.txtTelefono.setText(self.cliente.tblClientes.item(selected_row,4).text())
            self.cliente.txtDireccion.setText(self.cliente.tblClientes.item(selected_row,5).text())
            fecha_registro = self.cliente.tblClientes.item(selected_row,6).text().split('-')
            self.cliente.dtpFechaRegistro.setDate(QDate(int(fecha_registro[0]),int(fecha_registro[1]),int(fecha_registro[2])))
            self.cliente.lblModificar.setVisible(True)
            
    def guardar_cliente(self):
        if self.insert_update == False:
            self.nuevo_cliente()
        elif self.insert_update == True:
            self.modificar_cliente()

    
    def modificar_cliente(self):
        try:
            nombre = self.cliente.txtNombre.text()
            dni = self.cliente.txtDNI.text()
            correo = self.cliente.txtCorreo.text()
            telefono = self.cliente.txtTelefono.text()
            direccion = self.cliente.txtDireccion.text()
            fechaRegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")
            valid = self.valid()
            if valid == True:
                query = "UPDATE Clientes SET nombre = ?,DNI = ?, correo = ?, telefono = ?, direccion = ?, fecha_registro = ? WHERE ID = ?"
                values = (nombre,dni,correo,telefono,direccion,fechaRegistro, self.id_cliente)
                
                self.db.execute_query(query,values)
                QMessageBox.information(self.cliente,"Cliente Modificado","Cliente modificado con éxito.")
                self.cargar_datos_cliente()
                self.cliente.txtNombre.clear()
                self.cliente.txtDNI.clear()
                self.cliente.txtCorreo.clear()
                self.cliente.txtTelefono.clear()
                self.cliente.txtDireccion.clear()
                self.cliente.dtpFechaRegistro.setDate(QDate.currentDate())
                self.insert_update = False
                self.id_cliente = ""
                self.cliente.btnModificar.setEnabled(True)
                self.cliente.dtpFechaRegistro.setEnabled(True)
                self.cliente.lblModificar.setVisible(False)
        except Exception as e:
            QMessageBox.critical(self.cliente,"Error al modificar cliente",f"No se pudo modificar el cliente: {e}")
            print("No se pudo modificar el cliente:", e)
    
    def cancelar_modificar(self):
        self.insert_update = False
        self.cliente.btnModificar.setEnabled(True)
        self.cliente.dtpFechaRegistro.setEnabled(True)
        self.cliente.lblModificar.setVisible(False)
        self.cliente.dtpFechaRegistro.setDate(QDate.currentDate())

            
    def valid(self): #Valida que almenos un campo contenga texto.
        nombre = self.cliente.txtNombre.text()
        dni = self.cliente.txtDNI.text()
        correo = self.cliente.txtCorreo.text()
        telefono = self.cliente.txtTelefono.text()
        direccion = self.cliente.txtDireccion.text()
        if (nombre+correo+telefono+direccion+dni) == "":
            QMessageBox.warning(self.cliente, "Error", "Llene almenos un campo para agregar el cliente")
            return False
        if not dni.isdigit():
            QMessageBox.warning(self.cliente, "Error", "El DNI solo puede contener números")
            return False
        return True