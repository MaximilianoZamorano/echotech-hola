class PermisoDenegado(PermissionError):
    pass


def requiere_sesion(sesion):
    if not isinstance(sesion, dict) or sesion.get("empleado_id") is None:
        raise PermisoDenegado("Debe iniciar sesión para realizar esta operación.")


def requiere_admin(sesion):
    requiere_sesion(sesion)
    if sesion.get("rol") != "admin":
        raise PermisoDenegado("Esta operación requiere el rol administrador.")


def es_admin(sesion):
    return isinstance(sesion, dict) and sesion.get("rol") == "admin"

