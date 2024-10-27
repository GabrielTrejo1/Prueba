from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem
from PyQt5.QtCore import QDate
from src.conexion import Conexion

class Ventas():
    def __init__(self):
        self.ventas = uic.loadUi("gui\\ventas.ui")
        self.ventas.show()
        self.db = Conexion().conectar()

        self.initGui()
        
    def initGui(self): #Func. de inicio(lo que esta en esta funcion se va a ejecutar al iniciar el programa)
        try:
            query="SELECT day(GETDATE()),month(GETDATE()),year(GETDATE())" #Establecer fecha actual al dtpFechaRegistro
            cursor= self.db.cursor()
            res = cursor.execute(query)
            fecha_hoy= res.fetchall()
            self.ventas.dtpFechaRegistro.setDate(QDate(fecha_hoy[0][2],fecha_hoy[0][1],fecha_hoy[0][0]))
            
            self.cargar_ventas()
            self.cargar_clientes()
            
            # self.ventas.btnGuardar.clicked.connect(self.nuevo_cliente)
            # self.ventas.btnEliminar.clicked.connect(self.eliminar_cliente)
            # self.ventas.btnBuscar.clicked.connect(self.buscar_cliente)
            # self.ventas.txtBuscar.textChanged.connect(self.buscar_cliente)
        except Exception as e:
            print("Error de conexion: ",e)
        finally:
            cursor.close()
       
    def cargar_ventas(self): #Func. para llenar la tabla de Clientes.
            try:
                query = "SELECT V.ID, C.nombre FROM VENTAS AS V INNER JOIN CLIENTES AS C ON V.id_cliente = C.ID"
                cursor = self.db.cursor()
                res = cursor.execute(query)
                datos_ventas = res.fetchall()
                
                self.ventas.tblVentas.setRowCount(len(datos_ventas))
                
                fila = 0
                for item in datos_ventas:
                    self.ventas.tblVentas.setItem(fila,0,QTableWidgetItem(str(item[0])))
                    self.ventas.tblVentas.setItem(fila,1,QTableWidgetItem(str(item[1])))
                    # self.ventas.tblVentas.setItem(fila,2,QTableWidgetItem(str(item[2])))
                    # self.ventas.tblVentas.setItem(fila,3,QTableWidgetItem(str(item[3])))
                    # self.ventas.tblVentas.setItem(fila,4,QTableWidgetItem(str(item[4])))
                    # self.ventas.tblVentas.setItem(fila,5,QTableWidgetItem(str(item[5])))
                    fila +=1
            except Exception as e:
                print("Erros al cargar los clientes: ", e)
            finally:
                cursor.close()
    
    # Función para llenar la lista de clientes          
    def cargar_clientes(self):
      query = "SELECT nombre FROM CLIENTES" # solo consultar nombre
      cursor = self.db.cursor()
      res = cursor.execute(query)
      lista_ordenada = []
      for row in cursor.fetchall():
        lista_ordenada.append(row[0]) # por cada registro, solo agregar el campo nombre
      cursor.close()
      lista_ordenada.sort() # ordenar la lista de nombres
      print(lista_ordenada)
      self.ventas.comboClientes.addItems(lista_ordenada) # agregar la lista al comboBox
    
    def limpiar_tabla(self):
        self.ventas.tblVentas.setRowCount(0)
    
    # def nuevo_cliente(self):
    #     try:
    #         cursor = self.db.cursor()
            
    #         nombre = self.cliente.txtNombre.text()
    #         correo = self.cliente.txtCorreo.text()
    #         telefono = self.cliente.txtTelefono.text()
    #         direccion = self.cliente.txtDireccion.text()
    #         fechaRegistro = self.cliente.dtpFechaRegistro.date().toString("yyyy-MM-dd")
    #         valid = self.valid()
    #         if valid == True:
    #             query = "INSERT INTO Clientes (nombre, correo, telefono, direccion, fecha_registro) VALUES(?,?,?,?,?)"
    #             values = (nombre,correo,telefono,direccion,fechaRegistro)
                
    #             cursor.execute(query,values)
    #             cursor.commit()
    #             QMessageBox.information(self.cliente,"Cliente Agregado","Cliente agregado con éxito.")
    #             self.limpiar_tabla()
    #             self.cargar_ventas()
    #     except Exception as e:
    #         QMessageBox.critical(self.cliente,"Error al agregar cliente",f"No se pudo agregar el cliente: {e}")
    #         print("No se pudo insertar el cliente:", e)
    #     finally:
    #         cursor.close()
            
    # def eliminar_cliente(self): #Para eliminar un cliente se debe seleccionar una fila y luego pulsar el boton Eliminar.
    #     selected_row = self.cliente.tblVentas.currentRow()

    #     if selected_row < 0:  # Verificar si no hay fila seleccionada
    #         QMessageBox.warning(self.cliente, "Advertencia", "Por favor, seleccione un cliente para eliminar.")
    #         return

    #     # Confirmar eliminación
    #     confirm = QMessageBox.question(self.cliente, "Confirmar Eliminación", "¿Está seguro de que desea eliminar este cliente?", QMessageBox.Yes | QMessageBox.No)

    #     if confirm == QMessageBox.Yes:
    #         try:
    #             # Eliminar la fila seleccionada
    #             #print(selected_row)
    #             id_cliente=self.cliente.tblVentas.item(selected_row,0)
    #             cursor = self.db.cursor()
    #             query = "DELETE FROM Clientes WHERE ID = ?"
    #             values = int(id_cliente.text())
    #             cursor.execute(query,values)
    #             cursor.commit()
    #             self.cliente.tblVentas.removeRow(selected_row)
    #             QMessageBox.information(self.cliente, "Éxito", "Cliente eliminado exitosamente.")
    #         except Exception as e:
    #             print("Error al eliminar el cliente: ",e)
    #             QMessageBox.information(self.cliente, "Error", "No se pudo eliminar el cliente.")
    #         finally:
    #             cursor.close()
    
    # def buscar_cliente(self):
    #     try:
    #         nombre = self.cliente.txtBuscar.text().strip().lower()
    #         # Añadir comodines para coincidencias parciales
    #         query = "SELECT * FROM Clientes WHERE LOWER(nombre) LIKE ?"
    #         values = (f"%{nombre}%",)
    #         cursor = self.db.cursor()
    #         res = cursor.execute(query, values)
    #         datos_clientes = res.fetchall()

    #         # Limpiar la tabla antes de cargar nuevos datos
    #         self.cliente.tblVentas.setRowCount(0)

    #         # Llenar la tabla con los nuevos resultados
    #         self.cliente.tblVentas.setRowCount(len(datos_clientes))
    #         for fila, item in enumerate(datos_clientes):
    #             for columna, valor in enumerate(item):
    #                 self.cliente.tblVentas.setItem(fila, columna, QTableWidgetItem(str(valor)))
    #     except Exception as e:
    #         QMessageBox.critical(self.cliente, "Error", f"No se pudo buscar el cliente: {e}")
            
    # def valid(self): #Valida que almenos un campo contenga texto.
    #     nombre = self.cliente.txtNombre.text()
    #     correo = self.cliente.txtCorreo.text()
    #     telefono = self.cliente.txtTelefono.text()
    #     direccion = self.cliente.txtDireccion.text()
    #     if (nombre+correo+telefono+direccion) == "":
    #         QMessageBox.warning(self.cliente, "Error", "Llene almenos un campo para agregar el cliente")
    #         return False
    #     return True
        
    # def actualizar_cliente(self):
    #     pass
    
    # def filtrar_fecha(self):
    #     pass
        
        