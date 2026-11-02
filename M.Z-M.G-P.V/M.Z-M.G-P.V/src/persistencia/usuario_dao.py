from dominio.usuario import Usuario
from persistencia.conexion import conexion_segura, marcador_sql


class UsuarioDAO:
    @staticmethod
    def insertar(usuario: Usuario) -> Usuario:
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"""
                INSERT INTO usuario (nombre_usuario, password_hash, empleado_id)
                VALUES ({marca}, {marca}, {marca})
                """,
                (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id),
            )
            usuario.id = cursor.lastrowid
            conexion.commit()
        return usuario

    @staticmethod
    def buscar_por_nombre(nombre_usuario: str):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"""
                SELECT id, nombre_usuario, password_hash, empleado_id
                FROM usuario
                WHERE nombre_usuario = {marca}
                """,
                (nombre_usuario,),
            )
            fila = cursor.fetchone()
        return UsuarioDAO._fila_a_usuario(fila) if fila else None

    @staticmethod
    def buscar_por_empleado(id_empleado: int):
        marca = marcador_sql()
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                f"""
                SELECT id, nombre_usuario, password_hash, empleado_id
                FROM usuario
                WHERE empleado_id = {marca}
                """,
                (id_empleado,),
            )
            fila = cursor.fetchone()
        return UsuarioDAO._fila_a_usuario(fila) if fila else None

    @staticmethod
    def listar() -> list[Usuario]:
        with conexion_segura() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id, nombre_usuario, password_hash, empleado_id FROM usuario ORDER BY id"
            )
            filas = cursor.fetchall()
        return [UsuarioDAO._fila_a_usuario(fila) for fila in filas]

    @staticmethod
    def _fila_a_usuario(fila) -> Usuario:
        return Usuario(
            id=fila[0],
            nombre_usuario=fila[1],
            password_hash=fila[2],
            empleado_id=fila[3],
        )