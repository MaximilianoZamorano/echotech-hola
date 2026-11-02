from getpass import getpass

import requests

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.entrada import (
    leer_correo_opcional,
    leer_nombre,
    leer_telefono_opcional,
    leer_texto,
    limpiar_consola,
    pedir_dato,
    pausar,
)
from servicios.autenticacion import autenticar, registrar_usuario
from servicios.mi_cuenta import actualizar_mis_datos, obtener_mis_registros, obtener_mi_ficha
from servicios.permisos import PermisoDenegado, requiere_admin
from servicios.indicadores_api import extraer_indicador, obtener_datos


def solicitar_registro(usuario_actual=None):
    if usuario_actual is not None:
        requiere_admin(usuario_actual)
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        if empleado_id <= 0:
            raise ValueError("El ID del empleado debe ser positivo.")
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        rol = pedir_dato("Rol (admin/empleado): ", Usuario.normalizar_usuario)
        usuario = registrar_usuario(empleado_id, nombre, clave, rol=rol)
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
    empleado = obtener_mi_ficha(usuario_actual)
    print("\n===== CUENTA ACTUAL =====")
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"ID de cuenta: {usuario_actual['id']}")
    print(f"Rol: {usuario_actual['rol']}")
    print(f"Empleado asociado: {empleado.nombre}")
    print(f"ID de empleado: {usuario_actual['empleado_id']}")


def mostrar_mi_ficha(usuario_actual):
    empleado = obtener_mi_ficha(usuario_actual)
    print("\n===== MI FICHA =====")
    print(f"Nombre: {empleado.nombre}")
    print(f"Dirección: {empleado.direccion}")
    print(f"Teléfono: {empleado.telefono}")
    print(f"Correo: {empleado.email}")
    print(f"ID de empleado: {empleado.id}")
    print(f"Departamento: {empleado.departamento_id or 'Sin asignar'}")


def actualizar_mis_datos_menu(usuario_actual):
    empleado = obtener_mi_ficha(usuario_actual)
    print("\n===== MODIFICAR MIS DATOS =====")
    print("No puede modificar el rol, el ID, el salario ni el departamento.")
    nombre = leer_nombre(
        f"Nombre [{empleado.nombre}] (Enter conserva): ",
        obligatorio=False,
    )
    direccion = leer_texto(
        f"Dirección [{empleado.direccion}] (Enter conserva): ",
        obligatorio=False,
        maximo=200,
    )
    telefono = leer_telefono_opcional(
        f"Teléfono [{empleado.telefono}] (Enter conserva): "
    )
    email = leer_correo_opcional(
        f"Correo [{empleado.email}] (Enter conserva): "
    )

    try:
        empleado = actualizar_mis_datos(
            usuario_actual,
            nombre=nombre or None,
            direccion=direccion or None,
            telefono=telefono,
            email=email,
        )
        print("Sus datos personales fueron actualizados correctamente.")
    except (PermissionError, TypeError, ValueError) as error:
        print(f"No fue posible actualizar sus datos: {error}")


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


def _mostrar_mis_registros(usuario_actual):
    empleado = obtener_mi_ficha(usuario_actual)
    registros = obtener_mis_registros(usuario_actual)
    print(f"\nRegistros de {empleado.nombre}:")
    for registro in registros:
        print(f"- {registro.fecha}: {registro.horas} h - {registro.descripcion}")
    if not registros:
        print("No hay registros de tiempo.")


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        limpiar_consola()
        print("\n===== SESIÓN ECOTECH =====")
        if usuario_actual.get("rol") == "admin":
            print("1. Registrar cuenta")
            print("2. Abrir gestión del sistema")
            print("3. Modificar mis datos personales")
        else:
            print("1. Ver mi ficha")
            print("2. Ver mis registros de tiempo")
            print("3. Modificar mis datos personales")
        print("4. Consultar indicador" if usuario_actual.get("rol") == "admin" else "4. Consultar indicador")
        print("5. Ver mi cuenta actual" if usuario_actual.get("rol") == "empleado" else "5. Ver mi cuenta actual")
        print("0. Cerrar sesión")
        print("9. Salir del programa")
        opcion = input("Opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            if usuario_actual.get("rol") == "admin":
                solicitar_registro(usuario_actual)
            else:
                mostrar_mi_ficha(usuario_actual)
            pausar()
        elif opcion == "2":
            if usuario_actual.get("rol") == "admin":
                from presentacion.menu_principal import iniciar_menu_principal

                iniciar_menu_principal(usuario_actual)
            else:
                try:
                    _mostrar_mis_registros(usuario_actual)
                except (PermissionError, ValueError) as error:
                    print(error)
            pausar()
        elif opcion == "3":
            actualizar_mis_datos_menu(usuario_actual)
            pausar()
        elif opcion == "4":
            consultar_indicador(usuario_actual)
            pausar()
        elif opcion == "5":
            mostrar_perfil(usuario_actual)
            pausar()
        else:
            print("Opción no válida.")