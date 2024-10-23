def validar(valor1, valor2):
    if valor1 == valor2:
        return 'Validado exitosamente'
    else:
        return 'error al validar'


contraseña = 12
inversor_instancia = [1,12]

print(validar(contraseña, inversor_instancia[0]))