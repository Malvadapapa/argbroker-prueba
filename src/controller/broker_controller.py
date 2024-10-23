from src.model.inversor import Inversor
from src.model.accion import Accion
from src.model.portafolio import Portafolio
from src.model.transaccion import Transaccion
from src.utils.login import Login
from datetime import datetime
import random

class ControladorBroker:
    def __init__(self, inversor_dao, accion_dao, portafolio_dao, transaccion_dao):
        self.inversor_dao = inversor_dao
        self.accion_dao = accion_dao
        self.portafolio_dao = portafolio_dao
        self.transaccion_dao = transaccion_dao
        self.login = Login(inversor_dao)


    def registrar_inversor(self, nombre, apellido, cuil, email, contrasena, saldo_cuenta, direccion, telefono, perfil_inversor):
        nuevo_inversor = Inversor(None, nombre, apellido, cuil, email, contrasena, saldo_cuenta, direccion, telefono, perfil_inversor)
        id_inversor = self.inversor_dao.crear(nuevo_inversor)
        nuevo_inversor.id_inversor = id_inversor
        return nuevo_inversor

    def realizar_compra(self, id_inversor, id_accion, cantidad, precio):
        inversor = self.inversor_dao.obtener(id_inversor)
        accion = self.accion_dao.obtener(id_accion)
        if inversor and accion:
            monto_total = cantidad * precio
            if inversor.saldo_cuenta >= monto_total:
                inversor.actualizar_saldo(-monto_total)
                id_transaccion = self.transaccion_dao.obtener_numero_transacciones() + 1
                nueva_transaccion = Transaccion(id_transaccion, id_inversor, id_accion, "COMPRA", datetime.now(), precio, cantidad, 0)
                self.transaccion_dao.crear(nueva_transaccion)
                
                portafolio = next((p for p in self.portafolio_dao.obtener_por_inversor(id_inversor) if p.id_accion == id_accion), None)
                if portafolio:
                    portafolio.actualizar_cantidad(cantidad, precio)
                    self.portafolio_dao.actualizar(portafolio)
                else:
                    nuevo_portafolio = Portafolio(id_inversor, id_accion, cantidad, precio)
                    self.portafolio_dao.crear(nuevo_portafolio)
                return True
        return False

    def realizar_venta(self, id_inversor, id_accion, cantidad, precio):
        inversor = self.inversor_dao.obtener(id_inversor)
        accion = self.accion_dao.obtener(id_accion)
        if inversor and accion:
            portafolio = next((p for p in self.portafolio_dao.obtener_por_inversor(id_inversor) if p.id_accion == id_accion), None)
            if portafolio and portafolio.cantidad >= cantidad:
                monto_total = cantidad * precio
                inversor.actualizar_saldo(monto_total)
                id_transaccion = self.transaccion_dao.obtener_numero_transacciones() + 1
                nueva_transaccion = Transaccion(id_transaccion, id_inversor, id_accion, "VENTA", datetime.now(), precio, cantidad, 0)
                self.transaccion_dao.crear(nueva_transaccion)
                
                portafolio.actualizar_cantidad(-cantidad, precio)
                if portafolio.cantidad == 0:
                    self.portafolio_dao.eliminar(portafolio)
                else:
                    self.portafolio_dao.actualizar(portafolio)
                return True
        return False

    def ver_portafolio(self, id_inversor):
        return self.portafolio_dao.obtener_por_inversor(id_inversor)

    def ver_cotizaciones(self):
        return self.accion_dao.obtener_cotizaciones()