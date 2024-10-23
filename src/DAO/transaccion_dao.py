from src.model.transaccion import Transaccion

class TransaccionDAO:
    def __init__(self, mysql_connector):
        self.connector = mysql_connector

    def crear(self, transaccion):
        query = """INSERT INTO transaccion (id_inversor, id_accion, tipo, fecha, precio, cantidad, comision)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (transaccion.id_inversor, transaccion.id_accion, transaccion.tipo, transaccion.fecha,
                  transaccion.precio, transaccion.cantidad, transaccion.comision)
        cursor = self.connector.execute_query(query, params)
        if cursor:
            transaccion.id_transaccion = cursor.lastrowid
            return transaccion
        return None

    def obtener(self, id_transaccion):
        query = "SELECT * FROM transaccion WHERE id_transaccion = %s"
        result = self.connector.fetch_one(query, (id_transaccion,))
        if result:
            return Transaccion(*result)
        return None

    def actualizar(self, transaccion):
        query = """UPDATE transaccion SET id_inversor = %s, id_accion = %s, tipo = %s, fecha = %s,
                   precio = %s, cantidad = %s, comision = %s WHERE id_transaccion = %s"""
        params = (transaccion.id_inversor, transaccion.id_accion, transaccion.tipo, transaccion.fecha,
                  transaccion.precio, transaccion.cantidad, transaccion.comision, transaccion.id_transaccion)
        self.connector.execute_query(query, params)

    def eliminar(self, id_transaccion):
        query = "DELETE FROM transaccion WHERE id_transaccion = %s"
        self.connector.execute_query(query, (id_transaccion,))

    def obtener_por_inversor(self, id_inversor):
        query = "SELECT * FROM transaccion WHERE id_inversor = %s"
        results = self.connector.fetch_all(query, (id_inversor,))
        return [Transaccion(*result) for result in results]