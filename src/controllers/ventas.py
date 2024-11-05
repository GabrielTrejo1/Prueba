from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from models.conexion import Conexion
from config import base_path

class Ventas():
  def __init__(self):
    self.ventas = uic.loadUi(f"{base_path}/src/gui/ventas.ui")
    self.ventas.show()
    self.db = Conexion()
    self.initGui()

  def initGui(self):
    # Preparar algunos campos de la GUI
    self.ventas.txtIDCliente.setVisible(False)
    self.ventas.txtIDVehiculo.setVisible(False)
    self.ventas.dtpFechaRegistro.setDate(QDate.currentDate())
    self.ventas.dtpFechaHasta.setDate(QDate.currentDate())
    
    # Poblar tablas
    self.cargar_ventas()
    self.cargar_clientes()
    self.cargar_vehiculos()
    
    # Conectar funciones
    self.ventas.txtBuscarCliente.textChanged.connect(self.cargar_clientes)
    self.ventas.txtBuscarVehiculo.textChanged.connect(self.cargar_vehiculos)
    self.ventas.txtBuscarVenta.textChanged.connect(self.cargar_ventas)
    
    self.ventas.tblClientes.cellDoubleClicked.connect(self.seleccionar_cliente)
    self.ventas.tblVehiculos.cellDoubleClicked.connect(self.seleccionar_vehiculo)
    self.ventas.btnGuardar.clicked.connect(self.guardar_venta)
    
    self.ventas.dtpFechaDesde.dateChanged.connect(self.cargar_ventas)
    self.ventas.dtpFechaHasta.dateChanged.connect(self.cargar_ventas)
    self.ventas.checkFecha.clicked.connect(self.cargar_ventas)
    
  def cargar_ventas(self):
    if self.ventas.checkFecha.isChecked():
      desde = self.ventas.dtpFechaDesde.date().toString("yyyy-MM-dd")
      hasta = self.ventas.dtpFechaHasta.date().toString("yyyy-MM-dd")
      busqueda = self.ventas.txtBuscarVenta.text().strip().lower()
      query = "SELECT Vent.ID, C.nombre, Vent.precio_final, Vent.fecha_venta, Vehi.marca, Vehi.modelo, Vehi.dominio FROM VENTAS AS Vent INNER JOIN CLIENTES AS C ON Vent.id_cliente = C.ID INNER JOIN VEHICULOS AS Vehi ON Vent.id_vehiculo = Vehi.ID WHERE (LOWER(C.nombre) LIKE ? OR LOWER(C.nombre) LIKE ? OR LOWER(Vehi.marca) LIKE ? OR LOWER(Vehi.modelo) LIKE ? OR LOWER(Vehi.dominio) LIKE ?) AND fecha_venta BETWEEN ? AND ? ORDER BY Vent.ID DESC"
      values = (f"{busqueda}%", f"% {busqueda}%", f"{busqueda}%", f"{busqueda}%", f"{busqueda}%", desde, hasta)
      datos_ventas = self.db.execute_query_fetchall(query,values)
    else:
      busqueda = self.ventas.txtBuscarVenta.text().strip().lower()
      query = "SELECT Vent.ID, C.nombre, Vent.precio_final, Vent.fecha_venta, Vehi.marca, Vehi.modelo, Vehi.dominio FROM VENTAS AS Vent INNER JOIN CLIENTES AS C ON Vent.id_cliente = C.ID INNER JOIN VEHICULOS AS Vehi ON Vent.id_vehiculo = Vehi.ID WHERE LOWER(C.nombre) LIKE ? OR LOWER(C.nombre) LIKE ? OR LOWER(Vehi.marca) LIKE ? OR LOWER(Vehi.modelo) LIKE ? OR LOWER(Vehi.dominio) LIKE ? ORDER BY Vent.ID DESC"
      values = (f"{busqueda}%", f"% {busqueda}%", f"{busqueda}%", f"{busqueda}%", f"{busqueda}%")
      datos_ventas = self.db.execute_query_fetchall(query,values)

    # Limpiar la tabla antes de cargar nuevos datos
    self.ventas.tblVentas.setRowCount(0)
    self.ventas.tblVentas.setRowCount(len(datos_ventas))
    fila = 0
    for item in datos_ventas:
      self.ventas.tblVentas.setItem(fila,0,QTableWidgetItem(str(item[0])))
      self.ventas.tblVentas.setItem(fila,1,QTableWidgetItem(str(item[1])))
      self.ventas.tblVentas.setItem(fila,2,QTableWidgetItem(f"{str(item[4])} {str(item[5])} ({str(item[6])})")) # Marca Modelo (Patente)
      self.ventas.tblVentas.setItem(fila,3,QTableWidgetItem(str(item[2])))
      self.ventas.tblVentas.setItem(fila,4,QTableWidgetItem(str(item[3])))
      fila +=1
    self.ventas.tblVentas.resizeColumnsToContents()
  
  def cargar_clientes(self):
    busqueda = self.ventas.txtBuscarCliente.text().strip().lower()
    query = "SELECT ID, nombre, dni FROM Clientes WHERE LOWER(nombre) LIKE ? OR LOWER(nombre) LIKE ? ORDER BY id DESC"
    values = (f"{busqueda}%", f"% {busqueda}%") # Nombre - Apellido
    datos_clientes = self.db.execute_query_fetchall(query,values)

    # Limpiar la tabla antes de cargar nuevos datos
    self.ventas.tblClientes.setRowCount(0)
    self.ventas.tblClientes.setRowCount(len(datos_clientes))
    for fila, item in enumerate(datos_clientes):
      for columna, valor in enumerate(item):
        self.ventas.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
    self.ventas.tblClientes.resizeColumnsToContents()
        
  def cargar_vehiculos(self):
    busqueda = self.ventas.txtBuscarVehiculo.text().strip().lower()
    query = "SELECT ID, marca, modelo, color, dominio FROM Vehiculos WHERE (LOWER(marca) LIKE ? OR LOWER(modelo) LIKE ? OR LOWER(dominio) LIKE ?) AND disponible = 1 ORDER BY id DESC"
    values = (f"%{busqueda}%", f"%{busqueda}%", f"%{busqueda}%")
    datos_vehiculos = self.db.execute_query_fetchall(query,values)

    # Limpiar la tabla antes de cargar nuevos datos
    self.ventas.tblVehiculos.setRowCount(0)
    self.ventas.tblVehiculos.setRowCount(len(datos_vehiculos))
    for fila, item in enumerate(datos_vehiculos):
      for columna, valor in enumerate(item):
        self.ventas.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
    self.ventas.tblVehiculos.resizeColumnsToContents()

  def seleccionar_cliente(self):
    row = self.ventas.tblClientes.currentRow()
    self.ventas.txtIDCliente.setText(self.ventas.tblClientes.item(row, 0).text())
    self.ventas.txtNombreCliente.setText(self.ventas.tblClientes.item(row, 1).text())
    self.ventas.txtDNICliente.setText(self.ventas.tblClientes.item(row, 2).text())

  def seleccionar_vehiculo(self):
    row = self.ventas.tblVehiculos.currentRow()
    self.ventas.txtPatente.setText(self.ventas.tblVehiculos.item(row, 4).text())
    self.ventas.txtMarca.setText(self.ventas.tblVehiculos.item(row, 1).text())
    self.ventas.txtModelo.setText(self.ventas.tblVehiculos.item(row, 2).text())
    self.ventas.txtColor.setText(self.ventas.tblVehiculos.item(row, 3).text())
    self.ventas.txtIDVehiculo.setText(self.ventas.tblVehiculos.item(row, 0).text())
    
  def guardar_venta(self):
    datosValidos = self.validarDatos()
    if datosValidos:
      query = "INSERT INTO Ventas (id_cliente, id_vehiculo, fecha_venta, precio_final, metodo_pago, id_tipo_financiamiento) VALUES(?,?,?,?,'tarjeta',NULL)"
      values = (self.ventas.txtIDCliente.text(),
                self.ventas.txtIDVehiculo.text(),
                self.ventas.dtpFechaRegistro.date().toString("yyyy-MM-dd"),
                self.ventas.txtPrecio.text(),
                # metodo_pago,
                # id_tipo_financiamiento
                )
      
      self.db.execute_query(query, values)
      # Modificar disponibilidad del vehículo
      query_update = "UPDATE Vehiculos SET disponible = 0 WHERE ID = ?"
      values = (self.ventas.txtIDVehiculo.text())
      self.db.execute_query(query_update, values)
      self.cargar_vehiculos()

      QMessageBox.information(self.ventas,"Venta Agregada","Venta agregada con éxito.")
      self.cargar_ventas()
      # Limpiar campos después de guardar una venta
      self.ventas.txtIDCliente.clear()
      self.ventas.txtNombreCliente.clear()
      self.ventas.txtDNICliente.clear()
      self.ventas.txtIDVehiculo.clear()
      self.ventas.txtPatente.clear()
      self.ventas.txtMarca.clear()
      self.ventas.txtModelo.clear()
      self.ventas.txtColor.clear()
      self.ventas.txtPrecio.clear()
      
  def validarDatos(self):
    id_cliente = self.ventas.txtIDCliente.text()
    id_vehiculo = self.ventas.txtIDVehiculo.text()
    precio = self.ventas.txtPrecio.text()
    if id_cliente == "":
      QMessageBox.warning(self.ventas, "Error", "Por favor, selecciona un cliente.")
      return False
    if id_vehiculo == "":
      QMessageBox.warning(self.ventas, "Error", "Por favor, selecciona un vehículo.")
      return False
    if precio == "":
      QMessageBox.warning(self.ventas, "Error", "Por favor, ingresa el precio.")
      return False
    if int(precio) <= 0:
      QMessageBox.warning(self.ventas, "Error", "El precio debe ser mayor a cero.")
      return False
    return True
