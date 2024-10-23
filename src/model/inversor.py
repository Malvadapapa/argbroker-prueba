class Inversor:
    def __init__(self, id_inversor, nombre, apellido, cuil, email, contrasena, saldo_cuenta, direccion, telefono, perfil_inversor, intentos_fallidos=0, bloqueado=False):
        self.id_inversor = id_inversor
        self.nombre = nombre
        self.apellido = apellido
        self.cuil = cuil
        self.email = email
        self.contrasena = contrasena
        self.saldo_cuenta = saldo_cuenta
        self.direccion = direccion
        self.telefono = telefono
        self.perfil_inversor = perfil_inversor
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado = bloqueado

    def obtener_saldo(self):
        return self.saldo_cuenta

    def actualizar_saldo(self, monto):
        self.saldo_cuenta += monto

    def bloquear(self):
        self.bloqueado = True

    def desbloquear(self):
        self.bloqueado = False
        self.intentos_fallidos = 0

    def incrementar_intentos_fallidos(self):
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 3:
            self.bloquear()