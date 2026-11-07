from persistencia.conexion import conexion_segura, marcador_sql


def guardar_indicador(indicador):
    marcador = marcador_sql()
    sql = f"""
        INSERT INTO indicador_consulta
            (codigo, codigo_base, unidad_medida, moneda_destino, fecha_indicador, valor)
        VALUES ({marcador}, {marcador}, {marcador}, {marcador}, {marcador}, {marcador})
    """
    with conexion_segura() as conexion:
        conexion.execute(
            sql,
            (
                indicador["codigo"],
                indicador["codigo_base"],
                indicador["unidad_medida"],
                indicador["moneda_destino"],
                indicador["fecha"],
                indicador["valor"],
            ),
        )
        conexion.commit()
