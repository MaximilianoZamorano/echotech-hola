from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import requiere_sesion


def obtener_mi_ficha(sesion):
    requiere_sesion(sesion)
    empleado = EmpleadoDAO.obtenerPorId(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("No se encontró el empleado asociado a la sesión.")
    return empleado


def obtener_mis_registros(sesion):
    requiere_sesion(sesion)
    return RegistroTiempoDAO.listarPorEmpleado(sesion["empleado_id"])


def actualizar_mis_datos(
    sesion,
    nombre=None,
    direccion=None,
    telefono=None,
    email=None,
):
    requiere_sesion(sesion)
    empleado = obtener_mi_ficha(sesion)

    if nombre is not None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        empleado.nombre = nombre.strip()
    if direccion is not None:
        if not isinstance(direccion, str) or not direccion.strip():
            raise ValueError("La dirección no puede estar vacía.")
        empleado.direccion = direccion.strip()
    if telefono is not None:
        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El teléfono no puede estar vacío.")
        empleado.telefono = telefono.strip()
    if email is not None:
        if not isinstance(email, str):
            raise ValueError("El email del empleado no es válido.")
        email = email.strip().lower()
        if "@" not in email or email.startswith("@") or email.endswith("@"):
            raise ValueError("El email del empleado no es válido.")
        empleado.email = email.strip().lower()

    if not EmpleadoDAO.actualizar(empleado):
        raise ValueError("No fue posible actualizar la ficha.")
    return empleado
