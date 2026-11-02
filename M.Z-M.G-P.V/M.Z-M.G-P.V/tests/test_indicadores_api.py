import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from servicios.indicadores_api import extraer_indicador, obtener_datos


class IndicadoresApiTests(unittest.TestCase):
    def test_obtener_datos_consulta_get_con_timeout(self):
        respuesta = Mock()
        respuesta.json.return_value = {"codigo": "dolar", "serie": []}

        with patch("servicios.indicadores_api.requests.get", return_value=respuesta) as get:
            datos = obtener_datos()

        get.assert_called_once_with(
            "https://mindicador.cl/api/dolar",
            headers={
                "Accept": "application/json",
                "User-Agent": "EcoTech/1.0",
            },
            timeout=(5, 10),
        )
        respuesta.raise_for_status.assert_called_once_with()
        self.assertEqual(datos["codigo"], "dolar")

    def test_extraer_indicador_devuelve_registro_mas_reciente(self):
        datos = {
            "codigo": "dolar",
            "unidad_medida": "Pesos",
            "serie": [
                {"fecha": "2026-10-01T00:00:00.000Z", "valor": 900},
                {"fecha": "2026-10-02T00:00:00.000Z", "valor": 950.5},
            ],
        }

        indicador = extraer_indicador(datos)

        self.assertEqual(indicador["fecha"], "2026-10-02T00:00:00.000Z")
        self.assertEqual(indicador["valor"], 950.5)

    def test_extraer_indicador_rechaza_serie_vacia(self):
        datos = {
            "codigo": "dolar",
            "unidad_medida": "Pesos",
            "serie": [],
        }

        with self.assertRaises(ValueError):
            extraer_indicador(datos)

    def test_extraer_indicador_rechaza_valor_booleano(self):
        datos = {
            "codigo": "dolar",
            "unidad_medida": "Pesos",
            "serie": [{"fecha": "2026-10-02T00:00:00.000Z", "valor": True}],
        }

        with self.assertRaises(ValueError):
            extraer_indicador(datos)


if __name__ == "__main__":
    unittest.main()
