import os
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from persistencia.crear_db import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario


DEPARTAMENTOS_SEMILLA = (
    "Desarrollo",
    "Operaciones",
    "Recursos Humanos",
    "Finanzas",
    "Tecnologia",
)
ADMIN_EMAIL_SEMILLA = "ana.torres@ecotech.example"
ADMIN_USERNAME_SEMILLA = "admin"
EMPLEADO_USERNAME_SEMILLA = "empleado"
EMPLEADO_EMAIL_SEMILLA = "carla.mendez@ecotech.example"

EMPLEADOS_SEMILLA = (
    {"nombre": "Ana Torres", "direccion": "Av. Los Robles 101", "telefono": "+56970000001", "email": "ana.torres@ecotech.example", "fecha": date(2024, 1, 15), "salario": 1450000, "departamento": "Desarrollo"},
    {"nombre": "Bruno Silva", "direccion": "Calle El Sol 102", "telefono": "+56970000002", "email": "bruno.silva@ecotech.example", "fecha": date(2024, 2, 1), "salario": 1320000, "departamento": "Desarrollo"},
    {"nombre": "Carla Mendez", "direccion": "Pasaje Norte 103", "telefono": "+56970000003", "email": "carla.mendez@ecotech.example", "fecha": date(2024, 2, 19), "salario": 1280000, "departamento": "Desarrollo"},
    {"nombre": "Diego Fuentes", "direccion": "Av. Central 104", "telefono": "+56970000004", "email": "diego.fuentes@ecotech.example", "fecha": date(2024, 3, 4), "salario": 1210000, "departamento": "Desarrollo"},
    {"nombre": "Elena Rojas", "direccion": "Calle Verde 105", "telefono": "+56970000005", "email": "elena.rojas@ecotech.example", "fecha": date(2024, 3, 18), "salario": 1180000, "departamento": "Tecnologia"},
    {"nombre": "Felipe Soto", "direccion": "Av. Cordillera 201", "telefono": "+56970000006", "email": "felipe.soto@ecotech.example", "fecha": date(2023, 7, 10), "salario": 1500000, "departamento": "Operaciones"},
    {"nombre": "Gabriela Perez", "direccion": "Calle Los Pinos 202", "telefono": "+56970000007", "email": "gabriela.perez@ecotech.example", "fecha": date(2023, 8, 2), "salario": 1360000, "departamento": "Operaciones"},
    {"nombre": "Hugo Vargas", "direccion": "Pasaje Las Flores 203", "telefono": "+56970000008", "email": "hugo.vargas@ecotech.example", "fecha": date(2023, 8, 21), "salario": 1290000, "departamento": "Operaciones"},
    {"nombre": "Isabel Castro", "direccion": "Av. del Parque 204", "telefono": "+56970000009", "email": "isabel.castro@ecotech.example", "fecha": date(2023, 9, 5), "salario": 1240000, "departamento": "Operaciones"},
    {"nombre": "Jorge Navarro", "direccion": "Calle La Estrella 205", "telefono": "+56970000010", "email": "jorge.navarro@ecotech.example", "fecha": date(2023, 9, 25), "salario": 1190000, "departamento": "Tecnologia"},
    {"nombre": "Karen Morales", "direccion": "Av. Libertad 301", "telefono": "+56970000011", "email": "karen.morales@ecotech.example", "fecha": date(2022, 4, 11), "salario": 1420000, "departamento": "Recursos Humanos"},
    {"nombre": "Luis Herrera", "direccion": "Calle Nueva 302", "telefono": "+56970000012", "email": "luis.herrera@ecotech.example", "fecha": date(2022, 5, 3), "salario": 1300000, "departamento": "Recursos Humanos"},
    {"nombre": "Maria Paredes", "direccion": "Pasaje Los Alpes 303", "telefono": "+56970000013", "email": "maria.paredes@ecotech.example", "fecha": date(2022, 5, 23), "salario": 1250000, "departamento": "Recursos Humanos"},
    {"nombre": "Nicolas Reyes", "direccion": "Av. Las Naciones 304", "telefono": "+56970000014", "email": "nicolas.reyes@ecotech.example", "fecha": date(2022, 6, 13), "salario": 1170000, "departamento": "Recursos Humanos"},
    {"nombre": "Olivia Fuentes", "direccion": "Calle del Valle 305", "telefono": "+56970000015", "email": "olivia.fuentes@ecotech.example", "fecha": date(2022, 7, 4), "salario": 1140000, "departamento": "Tecnologia"},
    {"nombre": "Pablo Contreras", "direccion": "Av. del Mar 401", "telefono": "+56970000016", "email": "pablo.contreras@ecotech.example", "fecha": date(2021, 1, 18), "salario": 1550000, "departamento": "Finanzas"},
    {"nombre": "Rosa Vidal", "direccion": "Calle Uno 402", "telefono": "+56970000017", "email": "rosa.vidal@ecotech.example", "fecha": date(2021, 2, 8), "salario": 1380000, "departamento": "Finanzas"},
    {"nombre": "Sergio Leon", "direccion": "Pasaje Sur 403", "telefono": "+56970000018", "email": "sergio.leon@ecotech.example", "fecha": date(2021, 3, 1), "salario": 1270000, "departamento": "Finanzas"},
    {"nombre": "Tamara Vidal", "direccion": "Av. Horizonte 404", "telefono": "+56970000019", "email": "tamara.vidal@ecotech.example", "fecha": date(2021, 3, 22), "salario": 1220000, "departamento": "Finanzas"},
    {"nombre": "Victor Araya", "direccion": "Calle Los Cerezos 405", "telefono": "+56970000020", "email": "victor.araya@ecotech.example", "fecha": date(2021, 4, 12), "salario": 1160000, "departamento": "Tecnologia"},
)

PROYECTOS_SEMILLA = (
    {"nombre": "Plataforma EcoTech", "descripcion": "Evolucion de la plataforma interna.", "fecha": date(2026, 1, 10)},
    {"nombre": "Panel de Indicadores", "descripcion": "Indicadores operacionales y financieros.", "fecha": date(2026, 2, 1)},
    {"nombre": "Automatizacion de Soporte", "descripcion": "Flujos para mejorar la atencion interna.", "fecha": date(2026, 2, 15)},
    {"nombre": "Seguridad de Datos", "descripcion": "Controles y respaldo de informacion.", "fecha": date(2026, 3, 1)},
)


def _cargar_departamentos():
    existentes = {departamento.nombre: departamento for departamento in DepartamentoDAO.listar()}
    departamentos = {}
    for nombre in DEPARTAMENTOS_SEMILLA:
        departamentos[nombre] = existentes.get(nombre) or DepartamentoDAO.insertar(Departamento(nombre))
    return departamentos


def _cargar_empleados(departamentos):
    existentes = {empleado.email: empleado for empleado in EmpleadoDAO.listar()}
    empleados = {}
    for datos in EMPLEADOS_SEMILLA:
        departamento = departamentos[datos["departamento"]]
        empleado = existentes.get(datos["email"])
        if empleado is None:
            empleado = EmpleadoDAO.insertar(
                Empleado(
                    datos["nombre"],
                    datos["direccion"],
                    datos["telefono"],
                    datos["email"],
                    datos["fecha"],
                    datos["salario"],
                    departamento.id,
                )
            )
        elif empleado.departamento_id != departamento.id:
            empleado.asignarDepartamento(departamento.id)
            EmpleadoDAO.actualizar(empleado)
        empleados[datos["email"]] = empleado
    return empleados


def _asignar_gerentes(departamentos, empleados):
    for nombre, departamento in departamentos.items():
        gerente_email = next(
            datos["email"]
            for datos in EMPLEADOS_SEMILLA
            if datos["departamento"] == nombre
        )
        gerente = empleados[gerente_email]
        departamento = DepartamentoDAO.obtenerPorId(departamento.id)
        departamento.asignarGerente(gerente)
        DepartamentoDAO.actualizar(departamento)


def _cargar_proyectos():
    existentes = {proyecto.nombre: proyecto for proyecto in ProyectoDAO.listar()}
    proyectos = {}
    for datos in PROYECTOS_SEMILLA:
        proyectos[datos["nombre"]] = existentes.get(datos["nombre"]) or ProyectoDAO.insertar(
            Proyecto(datos["nombre"], datos["descripcion"], datos["fecha"])
        )
    return proyectos


def _cargar_registros(empleados, proyectos):
    existentes = {
        (registro.empleado_id, registro.proyecto_id, registro.descripcion)
        for registro in RegistroTiempoDAO.listar()
    }
    for posicion, datos in enumerate(EMPLEADOS_SEMILLA):
        empleado = empleados[datos["email"]]
        proyecto = proyectos[PROYECTOS_SEMILLA[posicion % len(PROYECTOS_SEMILLA)]["nombre"]]
        registro = (empleado.id, proyecto.id, f"Tarea inicial de {empleado.nombre}.")
        if registro not in existentes:
            RegistroTiempoDAO.insertar(
                RegistroTiempo(
                    fecha=date(2026, 3, 10 + posicion % 10),
                    horas=2.0 + (posicion % 4) * 0.5,
                    descripcion=registro[2],
                    empleado_id=empleado.id,
                    proyecto_id=proyecto.id,
                    empleado=empleado,
                    proyecto=proyecto,
                )
            )
            existentes.add(registro)


def _cargar_cuentas_prueba(empleados):
    empleado = empleados[ADMIN_EMAIL_SEMILLA]
    cuenta = UsuarioDAO.buscar_por_nombre(ADMIN_USERNAME_SEMILLA)
    if cuenta is None and UsuarioDAO.buscar_por_empleado(empleado.id) is None:
        registrar_usuario(
            empleado.id,
            ADMIN_USERNAME_SEMILLA,
            os.getenv("ECOTECH_ADMIN_PASSWORD", "admin123"),
            rol="admin",
        )
    elif cuenta is not None and cuenta.rol != "admin":
        UsuarioDAO.actualizar_rol(cuenta.id, "admin")
    empleado = empleados[EMPLEADO_EMAIL_SEMILLA]
    if (
        UsuarioDAO.buscar_por_nombre(EMPLEADO_USERNAME_SEMILLA) is None
        and UsuarioDAO.buscar_por_empleado(empleado.id) is None
    ):
        registrar_usuario(
            empleado.id,
            EMPLEADO_USERNAME_SEMILLA,
            os.getenv("ECOTECH_EMPLEADO_PASSWORD", "empleado123"),
            rol="empleado",
        )


def cargar_semilla() -> None:
    crear_tablas()
    departamentos = _cargar_departamentos()
    empleados = _cargar_empleados(departamentos)
    _asignar_gerentes(departamentos, empleados)
    proyectos = _cargar_proyectos()
    _cargar_registros(empleados, proyectos)
    _cargar_cuentas_prueba(empleados)
    print(
        f"Semilla lista: {len(departamentos)} departamentos, "
        f"{len(empleados)} empleados, {len(proyectos)} proyectos."
    )


if __name__ == "__main__":
    cargar_semilla()