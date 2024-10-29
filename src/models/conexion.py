import pyodbc

class Conexion:
    def __init__(self, db_path):
        self.db_path = db_path
        self.con = None
    
    def conectar(self):
        if not self.con:
            self.con = pyodbc.connect(self.db_path)
    
    def close(self):
        if self.con:
            self.con.close()
            self.con = None

    def execute_query_fetchall(self, query, params=()):
        try:
            self.conectar()
            cursor = self.con.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return []
        finally:
            cursor.close()

    def execute_query(self, query, params=()):
        try:
            self.conectar()
            cursor = self.con.cursor()
            cursor.execute(query, params)
            self.con.commit()
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
        finally:
            cursor.close()