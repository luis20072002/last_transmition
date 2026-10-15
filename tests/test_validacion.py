"""U4: los errores de contenido producen rechazo controlado, con causa e ID (RF13 a RF15)."""
from pathlib import Path

import pytest

from transmision.contenido.cargador import cargar_historia
from transmision.dominio.errores import ErrorContenido

INVALIDOS = Path(__file__).parent / "datos" / "invalidos"

CASOS = [
    ("ilegible", ["JSON válido"]),
    ("raiz_lista", ["objeto JSON", "raíz"]),
    ("sin_inicio", ["campo obligatorio", "'inicio'"]),
    ("inicio_inexistente", ["'inicio'", "'Z'", "no existe"]),
    ("escena_duplicada", ["Escena 'B'", "repetido"]),
    ("opcion_duplicada", ["Escena 'A'", "'o'", "repetido"]),
    ("destino_inexistente", ["Escena 'A'", "opción 'o'", "'E99'", "no existe"]),
    ("variable_no_declarada", ["opción 'o'", "'y'", "no está declarada"]),
    ("valor_no_booleano", ["opción 'o'", "'x'", "'si'", "verdadero o falso"]),
    ("final_con_opciones", ["Escena 'B'", "final", "no debe tener opciones"]),
    ("no_final_sin_opciones", ["Escena 'A'", "al menos una opción"]),
]


@pytest.mark.parametrize("nombre, fragmentos", CASOS)
def test_u4_archivo_defectuoso_se_rechaza_con_causa_e_id(nombre, fragmentos):
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(INVALIDOS / f"{nombre}.json")
    mensaje = "\n".join(info.value.mensajes)
    for fragmento in fragmentos:
        assert fragmento in mensaje, f"Falta '{fragmento}' en: {mensaje}"


def test_u4_archivo_inexistente_se_rechaza():
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(INVALIDOS / "no_existe.json")
    assert "No se encontró" in info.value.mensajes[0]