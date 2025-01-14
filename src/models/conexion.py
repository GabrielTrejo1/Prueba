import pyodbc

class Conexion:
  def __init__(self):
    self.con = None
  
  def conectar(self):
    if not self.con:
      self.con = pyodbc.connect("DSN=db_agencia")
  
  def close(self):
    if self.con:
      self.con.close()
      self.con = None

  def execute_query_fetchall(self, query, values=()):
    try:
      self.conectar()
      cursor = self.con.cursor()
      cursor.execute(query, values)
      return cursor.fetchall()
    except pyodbc.Error as e:
      print(f"Error ejecutando la consulta: {e}")
      return []
    finally:
      cursor.close()

  def execute_query(self, query, values=()):
    try:
      self.conectar()
      cursor = self.con.cursor()
      cursor.execute(query, values)
      self.con.commit()
    except pyodbc.Error as e:
      print(f"Error ejecutando la consulta: {e}")
    finally:
      cursor.close()
