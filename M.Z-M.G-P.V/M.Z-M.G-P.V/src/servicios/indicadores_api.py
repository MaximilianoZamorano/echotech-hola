import math
import datetime
import requests


URL_DOLAR = "https://mindicador.cl/api/dolar"
ENCABEZADOS = {
    "Accept": "application/json",
    "User-Agent": "EcoTech/1.0",
}
INTENTOS = 3


def obtener_datos(url=URL_DOLAR):
    """Realiza la petición HTTP a la API con una estrategia de reintentos."""
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
        raise ValueError(
            "La respuesta de la API no contiene un objeto JSON valido."
        )
    return datos


def _procesar_fecha_actualizacion(fecha_unix):
    """Convierte la marca de tiempo UNIX de la API a un objeto datetime UTC."""
    if not isinstance(fecha_unix, (int, float)):
        raise ValueError("La API no devolvió una fecha Unix válida.")
    try:
        return datetime.datetime.fromtimestamp(fecha_unix, tz=datetime.timezone.utc)
    except (ValueError, OverflowError) as error:
        raise ValueError("Error al procesar el formato de fecha.") from error


def extraer_indicador(datos, moneda_destino="CLP"):
    """Valida los datos de la API y extrae el valor de cambio y su fecha."""
    if not isinstance(datos, dict):
        raise ValueError("La respuesta de la API tiene un formato invalido.")

    if "serie" in datos:
        if datos.get("codigo") != "dolar":
            raise ValueError("La API no devolvió el indicador del dólar.")
        serie = datos.get("serie")
        if not isinstance(serie, list) or not serie:
            raise ValueError("La API no devolvió registros del dólar.")

        registros_validos = []
        for registro in serie:
            if not isinstance(registro, dict):
                continue
            valor = registro.get("valor")
            fecha = registro.get("fecha")
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or isinstance(fecha, (bool)) or not isinstance(fecha, str)
            ):
                continue
            valor = float(valor)
            if math.isfinite(valor) and valor > 0:
                registros_validos.append((fecha, valor))

        if not registros_validos:
            raise ValueError("La API no devolvió registros válidos del dólar.")

        fecha, valor = max(registros_validos, key=lambda registro: registro[0])
        return {
            "codigo": "dolar",
            "codigo_base": "USD",
            "unidad_medida": datos.get("unidad_medida", "Pesos"),
            "moneda_destino": moneda_destino,
            "fecha": fecha,
            "valor": valor,
        }

    if datos.get("result") != "success" or datos.get("base_code") != "USD":
        raise ValueError("La API devolvió datos de cambio no válidos.")

    tasas = datos.get("rates")
    if not isinstance(tasas, dict) or moneda_destino not in tasas:
        raise ValueError(f"La API no devolvió registros para la moneda {moneda_destino}.")

    valor = tasas[moneda_destino]
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"El valor de cambio para {moneda_destino} no es numérico.")

    valor = float(valor)
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"El valor de cambio para {moneda_destino} es inválido.")

    fecha_dt = _procesar_fecha_actualizacion(datos.get("time_last_update_unix"))
    return {
        "codigo": "dolar",
        "codigo_base": "USD",
        "unidad_medida": moneda_destino,
        "moneda_destino": moneda_destino,
        "fecha": fecha_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "valor": valor,
    }


def calcular_cambio_dolar(cantidad_usd, moneda_destino="CLP"):
    """Une las funciones para descargar, validar y calcular la conversión monetaria."""
    try:
 
        datos_api = obtener_datos()

       
        info_cambio = extraer_indicador(datos_api, moneda_destino)

        precio_dolar = info_cambio["valor"]
        total_convertido = cantidad_usd * precio_dolar

      
        print(f"\n--- Conversión USD a {moneda_destino} (ExchangeRate-API) ---")
        print(f"Valor actual de 1 USD: {precio_dolar:,.2f} {moneda_destino}")
        print(f"Última actualización API: {info_cambio['fecha']}")
        print(f"-------------------------------------------------------")
        print(
            f"{cantidad_usd:,.2f} USD equivalen a: {total_convertido:,.2f} {moneda_destino}\n"
        )

        return total_convertido

    except Exception as e:
        print(f"Error al realizar el cálculo del cambio: {e}")
        return None



if __name__ == "__main__":
    dolares_a_convertir = 100.00
    
   
    calcular_cambio_dolar(dolares_a_convertir, moneda_destino="CLP")
    
