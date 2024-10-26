import pyodbc

class Conexion():
    def __init__(self):
        try:
            self.con = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-B2OVTGG;DATABASE=AGENCIA_AC;Trusted_Connection=Yes;')
        except Exception as e:
            print(e)
        
    def conectar(self):
        return self.con
        
'''try:
            connection = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-B2OVTGG;DATABASE=DB_Prueba;Trusted_Connection=Yes;')
            print("Conexión Exitosa.")
            cursor=connection.cursor()
            cursor.execute("Select * FROM Clientes;")
            row=cursor.fetchall()
            for i in row:
                print(f"{i}\n")  
        except Exception as e:
            print(e)'''
