import math
from datetime import datetime, timezone

import requests


URL_DOLAR = "https://mindicador.cl/api/dolar"
ENCABEZADOS = {
    "Accept": "application/json",
    "User-Agent": "EcoTech/1.0",
}
INTENTOS = 3


def obtener_datos(url=URL_DOLAR):
    ultimo_error = None
    for intento in range(INTENTOS):
        try:
            respuesta = requests.get(
                url,
                headers=ENCABEZADOS,
                timeout=(5, 10),
            )
            respuesta.raise_for_status()
            datos = respuesta.json()
            break
        except requests.exceptions.RequestException as error:
            ultimo_error = error
            if intento == INTENTOS - 1:
                raise
    else:
        raise ultimo_error

    if not isinstance(datos, dict):
        raise ValueError("La respuesta de la API no contiene un objeto JSON valido.")
    return datos


def _fecha_ordenable(fecha):
    if not isinstance(fecha, str) or not fecha.strip():
        raise ValueError("El indicador no tiene una fecha valida.")
    fecha_normalizada = fecha.strip().replace("Z", "+00:00")
    try:
        fecha_hora = datetime.fromisoformat(fecha_normalizada)
    except ValueError as error:
        raise ValueError("El indicador no tiene una fecha valida.") from error
    if fecha_hora.tzinfo is None:
        fecha_hora = fecha_hora.replace(tzinfo=timezone.utc)
    return fecha_hora.astimezone(timezone.utc)


def extraer_indicador(datos):
    if not isinstance(datos, dict):
        raise ValueError("La respuesta de la API tiene un formato invalido.")
    if datos.get("codigo") != "dolar":
        raise ValueError("El indicador recibido no corresponde al dolar.")

    unidad = datos.get("unidad_medida")
    if not isinstance(unidad, str) or "peso" not in unidad.lower():
        raise ValueError("La unidad del dolar no corresponde a pesos.")

    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie:
        raise ValueError("La API no devolvio registros del dolar.")

    registros_validos = []
    for registro in serie:
        if not isinstance(registro, dict):
            continue
        fecha = registro.get("fecha")
        valor = registro.get("valor")
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            continue
        valor = float(valor)
        if not math.isfinite(valor) or valor <= 0:
            continue
        try:
            fecha_orden = _fecha_ordenable(fecha)
        except ValueError:
            continue
        registros_validos.append((fecha_orden, fecha.strip(), valor))

    if not registros_validos:
        raise ValueError("La API no devolvio un registro valido del dolar.")

    _, fecha, valor = max(registros_validos, key=lambda registro: registro[0])
    return {
        "codigo": datos["codigo"],
        "unidad_medida": unidad,
        "fecha": fecha,
        "valor": valor,
    }
