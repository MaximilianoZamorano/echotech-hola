# Sistema de Gestión EcoTechSolutions

Aplicación de consola en Python para administrar departamentos, empleados,
proyectos y registros de tiempo. La implementación está organizada en capas:

- `src/dominio`: clases y relaciones del diagrama UML.
- `src/persistencia`: conexión, creación de tablas y objetos DAO con operaciones
  CRUD parametrizadas.
- `src/presentacion`: menús y validación de entradas.
- `src/main.py`: inicialización de la base de datos y coordinación de los menús.

## Ejecución local con SQLite

Se requiere Python 3.10 o superior.

```powershell
python -m pip install -r requirement.txt
python src/main.py
```

SQLite se utiliza por defecto y crea `src/persistencia/ecotech.db`. Para cambiar
la configuración, copia `.env_example` a `.env`. No subas `.env` ni credenciales
reales al repositorio.

Para cargar dos empleados y datos relacionados de demostración (departamento,
gerente, proyectos y horas) ejecuta:

```powershell
python src/cargar_ejemplos.py
```

La carga es repetible y no duplica los ejemplos si vuelves a ejecutarla.
Después inicia la aplicación normalmente con `python src/main.py`.

### Semilla completa

Para preparar una base con datos ficticios más completos ejecuta:

```powershell
python src/semilla_bd.py
```

La semilla crea, si todavía no existen:

- 5 departamentos, cada uno con un gerente.
- 20 empleados con nombre, dirección, teléfono, correo, fecha de contrato,
  salario y departamento.
- 4 proyectos con descripción y fecha de inicio.
- 20 registros de tiempo vinculados a empleados y proyectos.

La carga es idempotente: puede ejecutarse varias veces y reconoce los
departamentos, empleados, proyectos y registros ya existentes sin duplicarlos.
La salida muestra el resumen de entidades preparadas. Para revisar el resultado
desde la aplicación, ejecuta después `python src/main.py`.

La semilla también prepara una cuenta inicial de acceso asociada a Ana Torres:

- Usuario: `admin`
- Contraseña inicial: `admin123`
- Empleado vinculado: `ana.torres@ecotech.example`

La contraseña se guarda únicamente como hash bcrypt. Para usar otra clave al
crear la cuenta inicial, define `ECOTECH_ADMIN_PASSWORD` antes de ejecutar la
semilla. Si la cuenta ya existe, conserva su ID, hash y vínculo.

## Registro y acceso

La aplicación inicia solicitando usuario y contraseña. Cada cuenta pertenece a
un empleado mediante `usuario.empleado_id`, que es obligatorio y único. Una
sesión válida permite:

- Registrar una cuenta para otro empleado existente.
- Consultar el perfil y las horas registradas del empleado autenticado.
- Abrir la gestión completa de departamentos, empleados, proyectos y tiempos.
- Cerrar sesión con la opción `9` o salir con la opción `0`.

Para preparar la base y probar el recorrido completo:

```powershell
python -m pip install -r requirement.txt
python src/semilla_bd.py
python src/main.py
```

Un login incorrecto no permite acceder al menú privado. Un login correcto
entrega `id`, `nombre_usuario` e `id_empleado`; al cerrar sesión se elimina el
estado de acceso y se solicita nuevamente el login.

## Uso de MySQL

Configura en `.env` `DB_ENGINE=mysql`, el host, puerto, nombre de base de datos,
usuario y contraseña. El usuario de la aplicación debe tener permisos limitados
a las operaciones requeridas; la contraseña se lee desde el entorno y no se
incluye en el código. La aplicación informa las variables obligatorias que
falten y no intenta conectarse con credenciales predeterminadas.

## Relaciones principales

- Un departamento contiene empleados y puede tener un empleado gerente.
- Un empleado puede pertenecer a un departamento y registrar varios tiempos.
- Cada registro de tiempo corresponde a un empleado y a un proyecto.
- Un proyecto agrupa sus registros; `calcularHorasTotales()` suma las horas
  recuperadas desde la base de datos.

Los DAO usan consultas parametrizadas, cierran las conexiones incluso cuando
ocurre un error y revierten la transacción antes de propagar la excepción. Los
formularios validan los datos y vuelven a solicitar las entradas que no cumplen
el formato esperado: fechas `AAAA-MM-DD`, horas y montos con hasta dos decimales
(punto o coma), IDs enteros positivos, correos y teléfonos válidos. El salario
puede ser cero y las horas registradas deben ser mayores que cero. La consola se
limpia entre operaciones y espera confirmación para que se alcance a leer el
resultado.

## Validación

Ejecuta las pruebas automatizadas desde la raíz del repositorio:

```powershell
python -m unittest discover -s tests -v
```

La revisión técnica final y la explicación de los aportes individuales y del uso
de herramientas de IA deben ser realizadas y justificadas por el equipo.
