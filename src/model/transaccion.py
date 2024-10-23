class Transaccion:
    def __init__(self, id_transaccion, id_inversor, id_accion, tipo, fecha, precio, cantidad, comision):
        self.id_transaccion = id_transaccion
        self.id_inversor = id_inversor
        self.id_accion = id_accion
        self.tipo = tipo
        self.fecha = fecha
        self.precio = precio
        self.cantidad = cantidad
        self.comision = comision

    def obtener_monto_total(self):
        return self.precio * self.cantidad + self.comision