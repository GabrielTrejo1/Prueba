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
    self.ventas.dtpFechaRegistro.setDate(QDate.currentDate())
    self.cargar_ventas()
    self.cargar_clientes()
    self.cargar_vehiculos()
    # self.ventas.btnGuardar.clicked.connect(self.nuevo_algo)
      
    self.ventas.txtBuscarCliente.textChanged.connect(self.buscar_cliente)
    self.ventas.txtBuscarVehiculo.textChanged.connect(self.buscar_vehiculo)
    # self.ventas.txtBuscarVenta.textChanged.connect(self.buscar_venta)

  # función para llenar la tabla de Ventas
  def cargar_ventas(self): 
    try:
      query = "SELECT V.ID, C.nombre, V.precio_final, V.fecha_venta FROM VENTAS AS V INNER JOIN CLIENTES AS C ON V.id_cliente = C.ID"
      datos_ventas = self.db.execute_query_fetchall(query)
      
      self.ventas.tblVentas.setRowCount(len(datos_ventas))
      
      fila = 0
      for item in datos_ventas:
        self.ventas.tblVentas.setItem(fila,0,QTableWidgetItem(str(item[0])))
        self.ventas.tblVentas.setItem(fila,1,QTableWidgetItem(str(item[1])))
        self.ventas.tblVentas.setItem(fila,2,QTableWidgetItem("Nada por ahora"))
        self.ventas.tblVentas.setItem(fila,3,QTableWidgetItem(str(item[2])))
        self.ventas.tblVentas.setItem(fila,4,QTableWidgetItem(str(item[3])))
        fila +=1
      self.ventas.tblVentas.resizeColumnsToContents()
    except Exception as e:
      print("Error al cargar las ventas: ", e)

  # función para llenar la tabla de Clientes
  def cargar_clientes(self):
    try:
      query = "SELECT id, nombre, dni FROM CLIENTES"
      datos_clientes = self.db.execute_query_fetchall(query)
      self.ventas.tblClientes.setRowCount(len(datos_clientes))
      for fila, item in enumerate(datos_clientes):
        for columna, valor in enumerate(item):
          self.ventas.tblClientes.setItem(fila, columna, QTableWidgetItem(str(valor)))
      self.ventas.tblClientes.resizeColumnsToContents()
    except Exception as e:
      print("Error al cargar los clientes: ", e)
      
  # función para llenar la tabla de Vehículos
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
        query = "SELECT ID, nombre, dni FROM Clientes WHERE LOWER(nombre) LIKE ? OR LOWER(nombre) LIKE ?"
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
      query = "SELECT ID, marca, modelo, dominio FROM Vehiculos WHERE marca LIKE ? OR modelo LIKE ? OR dominio LIKE ?"
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
    
  # def buscar_venta(self):
  #       try:
  #           marca = self.ventas.txtBuscarVenta.text().strip().lower()
  #           query = "SELECT * FROM Ventas WHERE Nombre LIKE ?"
  #           values = (f"{marca}%", f"{modelo}%")
  #           datos_vehiculos = self.db.execute_query_fetchall(query,values)

  #             # Limpiar la tabla antes de cargar nuevos datos
  #           self.vehiculo.tblVehiculos.setRowCount(0)

  #           self.vehiculo.tblVehiculos.setRowCount(len(datos_vehiculos))
  #           for fila, item in enumerate(datos_vehiculos):
  #               for columna, valor in enumerate(item):
  #                   self.vehiculo.tblVehiculos.setItem(fila, columna, QTableWidgetItem(str(valor)))
  #       except Exception as e:
  #           QMessageBox.critical(self.vehiculo, "Error", f"No se pudo buscar el vehiculo: {e}")

  # def nuevo_cliente(self):
  #   try:
  #     cursor = self.db.cursor()
      
  #     nombre = self.cliente.txtNombre.text()
  #     correo = self.cliente.txtCorreo.text()
  #     telefono = self.cliente.txtTelefono.text()
  #     direccion = self.cliente.txtDireccion.text()
  #     fechaRegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")
  #     valid = self.valid()
  #     if valid == True:
  #       query = "INSERT INTO Clientes (nombre, correo, telefono, direccion, fecha_registro) VALUES(?,?,?,?,?)"
  #       values = (nombre,correo,telefono,direccion,fechaRegistro)
        
  #       cursor.execute(query,values)
  #       cursor.commit()
  #       QMessageBox.information(self.cliente,"Cliente Agregado","Cliente agregado con éxito.")
  #       self.limpiar_tabla() # self.ventas.tblVentas.setRowCount(0)
  #       self.cargar_ventas()
  #   except Exception as e:
  #     QMessageBox.critical(self.cliente,"Error al agregar cliente",f"No se pudo agregar el cliente: {e}")
  #     print("No se pudo insertar el cliente:", e)
  #   finally:
  #       cursor.close()
          
  # def eliminar_cliente(self): #Para eliminar un cliente se debe seleccionar una fila y luego pulsar el boton Eliminar.
  #   selected_row = self.cliente.tblVentas.currentRow()

  #   if selected_row < 0:  # Verificar si no hay fila seleccionada
  #     QMessageBox.warning(self.cliente, "Advertencia", "Por favor, seleccione un cliente para eliminar.")
  #     return

  #   # Confirmar eliminación
  #   confirm = QMessageBox.question(self.cliente, "Confirmar Eliminación", "¿Está seguro de que desea eliminar este cliente?", QMessageBox.Yes | QMessageBox.No)

  #   if confirm == QMessageBox.Yes:
  #     try:
  #       # Eliminar la fila seleccionada
  #       #print(selected_row)
  #       id_cliente=self.cliente.tblVentas.item(selected_row,0)
  #       cursor = self.db.cursor()
  #       query = "DELETE FROM Clientes WHERE ID = ?"
  #       values = int(id_cliente.text())
  #       cursor.execute(query,values)
  #       cursor.commit()
  #       self.cliente.tblVentas.removeRow(selected_row)
  #       QMessageBox.information(self.cliente, "Éxito", "Cliente eliminado exitosamente.")
  #     except Exception as e:
  #       print("Error al eliminar el cliente: ",e)
  #       QMessageBox.information(self.cliente, "Error", "No se pudo eliminar el cliente.")
  #     finally:
  #       cursor.close()
  
  # def buscar_cliente(self):
  #   try:
  #     nombre = self.cliente.txtBuscar.text().strip().lower()
  #     # Añadir comodines para coincidencias parciales
  #     query = "SELECT * FROM Clientes WHERE LOWER(nombre) LIKE ?"
  #     values = (f"%{nombre}%",)
  #     cursor = self.db.cursor()
  #     res = cursor.execute(query, values)
  #     datos_clientes = res.fetchall()

  #     # Limpiar la tabla antes de cargar nuevos datos
  #     self.cliente.tblVentas.setRowCount(0)

  #     # Llenar la tabla con los nuevos resultados
  #     self.cliente.tblVentas.setRowCount(len(datos_clientes))
  #     for fila, item in enumerate(datos_clientes):
  #       for columna, valor in enumerate(item):
  #         self.cliente.tblVentas.setItem(fila, columna, QTableWidgetItem(str(valor)))
  #   except Exception as e:
  #     QMessageBox.critical(self.cliente, "Error", f"No se pudo buscar el cliente: {e}")
          
  # def valid(self): #Valida que almenos un campo contenga texto.
  #   nombre = self.cliente.txtNombre.text()
  #   correo = self.cliente.txtCorreo.text()
  #   telefono = self.cliente.txtTelefono.text()
  #   direccion = self.cliente.txtDireccion.text()
  #   if (nombre+correo+telefono+direccion) == "":
  #     QMessageBox.warning(self.cliente, "Error", "Llene almenos un campo para agregar el cliente")
  #     return False
  #   return True
      
  # def actualizar_cliente(self):
  #   pass
  
  # def filtrar_fecha(self):
  #   pass
