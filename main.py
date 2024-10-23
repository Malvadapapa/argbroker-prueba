import traceback
from src.controller.broker_controller import ControladorBroker
from src.DAO.inversor_dao import InversorDAO
from src.DAO.accion_dao import AccionDAO
from src.DAO.portafolio_dao import PortafolioDAO
from src.DAO.transaccion_dao import TransaccionDAO
from src.utils.mysql_connector import MySQLConnector
from src.model.accion import Accion

class MenuConsola:
    def __init__(self, controlador):
        self.controlador = controlador
        self.inversor_actual = None

    def mostrar_menu_principal(self):
        while True:
            print("\n--- Menu Principal ---")
            print("1. Iniciar sesion")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opcion: ")
            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                self.registrarse()
            elif opcion == "3":
                break
            else:
                print("Opcion no valida")

    def iniciar_sesion(self):
        email = input("Ingrese su email: ")
        contrasena = input("Ingrese su contrasena: ")
        try:
            inversor = self.controlador.login.autenticar(email, contrasena)
            if inversor:
                self.inversor_actual = inversor
                print(f"Bienvenido, {inversor.nombre}!")
                self.mostrar_menu_inversor()
            else:
                print("Credenciales incorrectas o cuenta bloqueada.")
        except Exception as e:
            print(f"Error during login: {e}")
            traceback.print_exc()

    def mostrar_menu_inversor(self):
        while True:
            print("\n--- Menu Inversor ---")
            print("1. Ver saldo")
            print("2. Ver portafolio")
            print("3. Ver cotizaciones")
            print("4. Comprar acciones")
            print("5. Vender acciones")
            print("6. Cerrar sesion")
            opcion = input("Seleccione una opcion: ")
            if opcion == "1":
                self.ver_saldo()
            elif opcion == "2":
                self.ver_portafolio()
            elif opcion == "3":
                self.ver_cotizaciones()
            elif opcion == "4":
                self.comprar_acciones()
            elif opcion == "5":
                self.vender_acciones()
            elif opcion == "6":
                break
            else:
                print("Opcion no valida")

    def ver_saldo(self):
        print(f"Su saldo actual es: ${self.inversor_actual.saldo_cuenta:.2f}")

    def ver_portafolio(self):
        portafolio = self.controlador.ver_portafolio(self.inversor_actual.id_inversor)
        if portafolio:
            for accion in portafolio:
                print(f"{accion.simbolo}: {accion.cantidad} acciones")
        else:
            print("No tiene acciones en su portafolio.")

    def ver_cotizaciones(self):
        try:
            cotizaciones = self.controlador.ver_cotizaciones()
            if cotizaciones:
                for simbolo, precio in cotizaciones.items():
                    print(f"{simbolo}: ${precio:.2f}")
            else:
                print("No se encontraron cotizaciones.")
        except Exception as e:
            print(f"Error fetching cotizaciones: {e}")
            traceback.print_exc()

    def comprar_acciones(self):
        id_accion = int(input("Ingrese el ID de la accion que desea comprar: "))
        cantidad = int(input("Ingrese la cantidad de acciones que desea comprar: "))
        precio = float(input("Ingrese el precio de la accion: "))
        if self.controlador.realizar_compra(self.inversor_actual.id_inversor, id_accion, cantidad, precio):
            print("Compra realizada con exito.")
        else:
            print("No se pudo realizar la compra. Verifique su saldo y los datos ingresados.")

    def vender_acciones(self):
        id_accion = int(input("Ingrese el ID de la accion que desea vender: "))
        cantidad = int(input("Ingrese la cantidad de acciones que desea vender: "))
        precio = float(input("Ingrese el precio de la accion: "))
        if self.controlador.realizar_venta(self.inversor_actual.id_inversor, id_accion, cantidad, precio):
            print("Venta realizada con exito.")
        else:
            print("No se pudo realizar la venta. Verifique su portafolio y los datos ingresados.")

    def registrarse(self):
        nombre = input("Ingrese su nombre: ")
        apellido = input("Ingrese su apellido: ")
        cuil = input("Ingrese su CUIL: ")
        email = input("Ingrese su email: ")
        contrasena = input("Ingrese su contrasena: ")
        saldo_cuenta = float(input("Ingrese su saldo inicial (opcional, presione Enter para omitir): ") or 0.00)
        direccion = input("Ingrese su direccion (opcional, presione Enter para omitir): ") or None
        telefono = input("Ingrese su telefono (opcional, presione Enter para omitir): ") or None
        perfil_inversor = input("Ingrese su perfil de inversor (opcional, presione Enter para omitir): ") or None
        nuevo_inversor = self.controlador.registrar_inversor(nombre, apellido, cuil, email, contrasena, saldo_cuenta, direccion, telefono, perfil_inversor)
        if nuevo_inversor:
            print(f"Registro exitoso. Bienvenido, {nuevo_inversor.nombre}!")
        else:
            print("No se pudo realizar el registro. Verifique los datos ingresados.")

if __name__ == "__main__":
    # MySQL connection details
    host = "127.0.0.1"
    database = "arg_broker_bdd"
    user = "root"
    password = "redcros62"

    # Create MySQL connector
    mysql_connector = MySQLConnector(host, database, user, password)
    mysql_connector.connect()

    # Create DAOs with MySQL connector
    inversor_dao = InversorDAO(mysql_connector)
    accion_dao = AccionDAO(mysql_connector)
    portafolio_dao = PortafolioDAO(mysql_connector)
    transaccion_dao = TransaccionDAO(mysql_connector)

    # Create controller
    controlador = ControladorBroker(inversor_dao, accion_dao, portafolio_dao, transaccion_dao)

    # Create and run menu
    menu = MenuConsola(controlador)
    try:
        menu.mostrar_menu_principal()
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        traceback.print_exc()
        print("El programa se cerrara.")
    finally:
        mysql_connector.disconnect()