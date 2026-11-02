from getpass import getpass

import requests

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.entrada import limpiar_consola, pedir_dato, pausar
from servicios.autenticacion import autenticar, registrar_usuario
from servicios.indicadores_api import extraer_indicador, obtener_datos


def solicitar_registro():
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        if empleado_id <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        usuario = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        return None
    print(f"Cuenta creada correctamente. ID: {usuario.id}")
    return usuario.id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    empleado = EmpleadoDAO.obtenerPorId(usuario_actual["empleado_id"])
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {empleado.nombre if empleado else 'No encontrado'}")
    print(f"ID del empleado: {usuario_actual['empleado_id']}")


def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    try:
        indicador = extraer_indicador(obtener_datos())
    except requests.exceptions.RequestException:
        print("No fue posible consultar la API del dolar. Verifique su conexion.")
        return
    except (KeyError, TypeError, ValueError) as error:
        print(f"La API devolvio datos invalidos: {error}")
        return

    print("\nIndicador observado del dolar")
    print(f"Codigo: {indicador['codigo']}")
    print(f"Unidad: {indicador['unidad_medida']}")
    print(f"Fecha: {indicador['fecha']}")
    print(f"Valor: ${indicador['valor']:,.2f}")


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        limpiar_consola()
        print("\n===== SESIÓN ECOTECH =====")
        print("1. Registrar cuenta")
        print("2. Ver perfil")
        print("3. Consultar indicador")
        print("4. Abrir gestión del sistema")
        print("9. Cerrar sesión")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            solicitar_registro()
            pausar()
        elif opcion == "2":
            mostrar_perfil(usuario_actual)
            pausar()
        elif opcion == "3":
            consultar_indicador(usuario_actual)
            pausar()
        elif opcion == "4":
            from presentacion.menu_principal import iniciar_menu_principal

            iniciar_menu_principal()
        else:
            print("Opción no válida.")