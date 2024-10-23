from src.model.inversor import Inversor

class InversorDAO:
    def __init__(self, mysql_connector):
        self.connector = mysql_connector

    def crear(self, inversor):
        try:
            query = """INSERT INTO inversor (nombre, apellido, cuil, email, contrasena, saldo_cuenta, direccion, telefono, perfil_inversor)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (inversor.nombre, inversor.apellido, inversor.cuil, inversor.email, inversor.contrasena,
                      inversor.saldo_cuenta, inversor.direccion, inversor.telefono, inversor.perfil_inversor)
            cursor = self.connector.execute_query(query, params)
            if cursor:
                inversor.id_inversor = cursor.lastrowid
                return inversor
        except Error as e:
            print(f"Error creating inversor: {e}")
            traceback.print_exc()
        return None

    def obtener(self, id_inversor):
        try:
            query = "SELECT * FROM inversor WHERE id_inversor = %s"
            result = self.connector.fetch_one(query, (id_inversor,))
            if result:
                return Inversor(*result)
        except Error as e:
            print(f"Error fetching inversor by id: {e}")
            traceback.print_exc()
        return None

    def actualizar(self, inversor):
        try:
            query = """UPDATE inversor SET nombre = %s, apellido = %s, cuil = %s, email = %s, contrasena = %s,
                       saldo_cuenta = %s, direccion = %s, telefono = %s, perfil_inversor = %s, intentos_fallidos = %s,
                       bloqueado = %s WHERE id_inversor = %s"""
            params = (inversor.nombre, inversor.apellido, inversor.cuil, inversor.email, inversor.contrasena,
                      inversor.saldo_cuenta, inversor.direccion, inversor.telefono, inversor.perfil_inversor,
                      inversor.intentos_fallidos, inversor.bloqueado, inversor.id_inversor)
            self.connector.execute_query(query, params)
        except Error as e:
            print(f"Error updating inversor: {e}")
            traceback.print_exc()

    def eliminar(self, id_inversor):
        try:
            query = "DELETE FROM inversor WHERE id_inversor = %s"
            self.connector.execute_query(query, (id_inversor,))
        except Error as e:
            print(f"Error deleting inversor: {e}")
            traceback.print_exc()

    def obtener_por_email(self, email):
        try:
            query = "SELECT * FROM inversor WHERE email = %s"
            result = self.connector.fetch_one(query, (email,))
            if result:
                return Inversor(*result)
        except Error as e:
            print(f"Error fetching inversor by email: {e}")
            traceback.print_exc()
        return None