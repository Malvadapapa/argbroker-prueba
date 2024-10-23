from src.model.accion import Accion

class AccionDAO:
    def __init__(self, mysql_connector):
        self.connector = mysql_connector

    def crear(self, accion):
        query = "INSERT INTO accion (nombre_empresa, simbolo_empresa) VALUES (%s, %s)"
        params = (accion.nombre_empresa, accion.simbolo_empresa)
        cursor = self.connector.execute_query(query, params)
        if cursor:
            accion.id_accion = cursor.lastrowid
            return accion
        return None

    def obtener(self, id_accion):
        query = "SELECT * FROM accion WHERE id_accion = %s"
        result = self.connector.fetch_one(query, (id_accion,))
        if result:
            return Accion(*result)
        return None

    def actualizar(self, accion):
        query = "UPDATE accion SET nombre_empresa = %s, simbolo_empresa = %s WHERE id_accion = %s"
        params = (accion.nombre_empresa, accion.simbolo_empresa, accion.id_accion)
        self.connector.execute_query(query, params)

    def eliminar(self, id_accion):
        query = "DELETE FROM accion WHERE id_accion = %s"
        self.connector.execute_query(query, (id_accion,))

    def obtener_todas(self):
        query = "SELECT * FROM accion"
        results = self.connector.fetch_all(query)
        return [Accion(*result) for result in results]

    def obtener_cotizaciones(self):
        query = """
        SELECT a.simbolo_empresa, c.ultimo_operado 
        FROM accion a
        JOIN cotizacion_diaria c ON a.id_accion = c.id_accion
        WHERE c.fecha = (SELECT MAX(fecha) FROM cotizacion_diaria WHERE id_accion = a.id_accion)
        """
        results = self.connector.fetch_all(query)
        if not results:
            print("No se encontraron cotizaciones.")
            return {}
        cotizaciones = {simbolo: precio for simbolo, precio in results}
        return cotizaciones