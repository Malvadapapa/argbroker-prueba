from src.model.portafolio import Portafolio

class PortafolioDAO:
    def __init__(self, mysql_connector):
        self.connector = mysql_connector

    def crear(self, portafolio):
        query = "INSERT INTO portafolio (id_inversor, id_accion, cantidad, precio_promedio_compra) VALUES (%s, %s, %s, %s)"
        params = (portafolio.id_inversor, portafolio.id_accion, portafolio.cantidad, portafolio.precio_promedio_compra)
        cursor = self.connector.execute_query(query, params)
        if cursor:
            portafolio.id_portafolio = cursor.lastrowid
            return portafolio
        return None

    def obtener(self, id_portafolio):
        query = "SELECT * FROM portafolio WHERE id_portafolio = %s"
        result = self.connector.fetch_one(query, (id_portafolio,))
        if result:
            return Portafolio(*result)
        return None

    def actualizar(self, portafolio):
        query = "UPDATE portafolio SET cantidad = %s, precio_promedio_compra = %s WHERE id_portafolio = %s"
        params = (portafolio.cantidad, portafolio.precio_promedio_compra, portafolio.id_portafolio)
        self.connector.execute_query(query, params)

    def eliminar(self, id_portafolio):
        query = "DELETE FROM portafolio WHERE id_portafolio = %s"
        self.connector.execute_query(query, (id_portafolio,))

    def obtener_por_inversor(self, id_inversor):
        query = "SELECT * FROM portafolio WHERE id_inversor = %s"
        results = self.connector.fetch_all(query, (id_inversor,))
        return [Portafolio(*result) for result in results]