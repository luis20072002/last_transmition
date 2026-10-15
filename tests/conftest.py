"""Fixtures compartidas por las pruebas."""
from pathlib import Path

import pytest

from transmision.contenido.cargador import cargar_historia
from transmision.motor.sesion import Sesion

RAIZ = Path(__file__).resolve().parent.parent
RUTA_REFERENCIA = RAIZ / "historias" / "la_ultima_transmision.json"
RUTA_HISTORIA2 = RAIZ / "historias" / "historia2.json"


@pytest.fixture
def historia():
    return cargar_historia(RUTA_REFERENCIA)


@pytest.fixture
def sesion(historia):
    return Sesion(historia)