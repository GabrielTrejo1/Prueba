from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from models.conexion import Conexion

class Ventas():
  def __init__(self):
    self.ventas = uic.loadUi("src/gui/ventas.ui")
    self.ventas.show()
    self.db = Conexion()
    self.initGui()

  def initGui(self):
    self.ventas.txtIDCliente.setVisible(False)
    self.ventas.txtIDVehiculo.setVisible(False)
    
    self.ventas.dtpFechaRegistro.setDate(QDate.currentDate())
    self.cargar_ventas()
    self.cargar_clientes()
    self.cargar_vehiculos()
      
    self.ventas.txtBuscarCliente.textChanged.connect(self.buscar_cliente)
    self.ventas.txtBuscarVehiculo.textChanged.connect(self.buscar_vehiculo)
    self.ventas.txtBuscarVenta.textChanged.connect(self.buscar_venta)
    
    self.ventas.tblClientes.cellDoubleClicked.connect(self.seleccionar_cliente)
    self.ventas.tblVehiculos.cellDoubleClicked.connect(self.seleccionar_vehiculo)
    self.ventas.btnGuardar.clicked.connect(self.guardar_venta)
    
  # poblar la tabla de Ventas
  def cargar_ventas(self): 
    try:
      query = "SELECT Vent.ID, C.nombre, Vent.precio_final, Vent.fecha_venta, Vehi.marca, Vehi.modelo, Vehi.dominio FROM VENTAS AS Vent INNER JOIN CLIENTES AS C ON Vent.id_cliente = C.ID INNER JOIN VEHICULOS AS Vehi ON Vent.id_vehiculo = Vehi.ID ORDER BY Vent.ID DESC"
      datos_ventas = self.db.execute_query_fetchall(query)
      
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
    except Exception as e:
      print("Error al cargar las ventas: ", e)

  # poblar la tabla de Clientes
  def cargar_clientes(self):
    try:
      query = "SELECT id, nombre, dni FROM CLIENTES ORDER BY id DESC"
      datos_clientes = self.db.execute_query_fetchall(query)
      self.ventas.tblClientes.setRowCount(len(datos_clientes))
      for fila, item in enumerate(datos_clientes):
        for columna, valor in enumerate(item):
          self.ventas.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
      self.ventas.tblClientes.resizeColumnsToContents()
    except Exception as e:
      print("Error al cargar los clientes: ", e)
      
  # poblar la tabla de Vehículos
  def cargar_vehiculos(self):
    try:
      query = "SELECT ID, marca, modelo, color, dominio FROM VEHICULOS"
      datos_vehiculos = self.db.execute_query_fetchall(query)
      self.ventas.tblVehiculos.setRowCount(len(datos_vehiculos))
      for fila, item in enumerate(datos_vehiculos):
        for columna, valor in enumerate(item):
          self.ventas.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
      self.ventas.tblVehiculos.resizeColumnsToContents()
    except Exception as e:
      print("Error al cargar los vehículos: ", e)
  
  def buscar_cliente(self):
    try:
        cliente = self.ventas.txtBuscarCliente.text().strip().lower()
        query = "SELECT ID, nombre, dni FROM Clientes WHERE LOWER(nombre) LIKE ? OR LOWER(nombre) LIKE ? ORDER BY id DESC"
        values = (f"{cliente}%", f"% {cliente}%") # Esto es tremendo soy un capo
        datos_clientes = self.db.execute_query_fetchall(query,values)

        # Limpiar la tabla antes de cargar nuevos datos
        self.ventas.tblClientes.setRowCount(0)

        self.ventas.tblClientes.setRowCount(len(datos_clientes))
        for fila, item in enumerate(datos_clientes):
            for columna, valor in enumerate(item):
                self.ventas.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
    except Exception as e:
        QMessageBox.critical(self.ventas, "Error", f"No se pudo buscar el cliente: {e}")
        
  def buscar_vehiculo(self):
    try:
      txt_busq = self.ventas.txtBuscarVehiculo.text().strip().lower()
      query = "SELECT ID, marca, modelo, color, dominio FROM Vehiculos WHERE marca LIKE ? OR modelo LIKE ? OR dominio LIKE ?"
      values = (f"%{txt_busq}%", f"%{txt_busq}%", f"%{txt_busq}%")
      datos_vehiculos = self.db.execute_query_fetchall(query,values)

      # Limpiar la tabla antes de cargar nuevos datos
      self.ventas.tblVehiculos.setRowCount(0)

      self.ventas.tblVehiculos.setRowCount(len(datos_vehiculos))
      for fila, item in enumerate(datos_vehiculos):
          for columna, valor in enumerate(item):
              self.ventas.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
    except Exception as e:
        QMessageBox.critical(self.ventas, "Error", f"No se pudo buscar el vehículo: {e}")
    
  def buscar_venta(self):
    try:
      txt_busq = self.ventas.txtBuscarVenta.text().strip().lower()
      query = "SELECT Vent.ID, C.nombre, Vent.precio_final, Vent.fecha_venta, Vehi.marca, Vehi.modelo, Vehi.dominio FROM VENTAS AS Vent INNER JOIN CLIENTES AS C ON Vent.id_cliente = C.ID INNER JOIN VEHICULOS AS Vehi ON Vent.id_vehiculo = Vehi.ID WHERE LOWER(C.nombre) LIKE ? OR LOWER(C.nombre) LIKE ? OR LOWER(Vehi.marca) LIKE ? OR LOWER(Vehi.modelo) LIKE ? OR LOWER(Vehi.dominio) LIKE ? ORDER BY Vent.ID DESC"
      values = (f"{txt_busq}%", f"% {txt_busq}%", f"{txt_busq}%", f"{txt_busq}%", f"{txt_busq}%")
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
    except Exception as e:
      QMessageBox.critical(self.vehiculo, "Error", f"No se pudo buscar la venta: {e}")

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
    valid = self.valid()
    if valid:
      query = "INSERT INTO Ventas (id_cliente, id_vehiculo, fecha_venta, precio_final, metodo_pago, id_tipo_financiamiento) VALUES(?,?,?,?,'tarjeta',NULL)"
      values = (self.ventas.txtIDCliente.text(),
                self.ventas.txtIDVehiculo.text(),
                self.ventas.dtpFechaRegistro.date().toString("yyyy-MM-dd"),
                self.ventas.txtPrecio.text(),
                # metodo_pago,
                # id_tipo_financiamiento
                )
      
      self.db.execute_query(query, values)
      QMessageBox.information(self.ventas,"Venta Agregada","Venta agregada con éxito.")
      self.cargar_ventas()
      self.ventas.txtIDCliente.clear()
      self.ventas.txtNombreCliente.clear()
      self.ventas.txtDNICliente.clear()
      self.ventas.txtIDVehiculo.clear()
      self.ventas.txtPatente.clear()
      self.ventas.txtMarca.clear()
      self.ventas.txtModelo.clear()
      self.ventas.txtColor.clear()
      self.ventas.txtPrecio.clear()
      
  def valid(self): #Valida que almenos un campo contenga texto.
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