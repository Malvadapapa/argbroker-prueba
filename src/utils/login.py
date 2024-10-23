class Login:
    def __init__(self, inversor_dao):
        self.inversor_dao = inversor_dao

    def autenticar(self, email, contrasena):
        try:
            inversor = self.inversor_dao.obtener_por_email(email)
            if inversor and not inversor.bloqueado:
                if inversor.contrasena == contrasena:
                    inversor.intentos_fallidos = 0
                    self.inversor_dao.actualizar(inversor)
                    return inversor
                else:
                    inversor.incrementar_intentos_fallidos()
                    self.inversor_dao.actualizar(inversor)
        except Error as e:
            print(f"Error during authentication: {e}")
            traceback.print_exc()
        return None