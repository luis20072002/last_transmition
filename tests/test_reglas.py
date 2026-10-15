"""U1: las condiciones cumplidas y no cumplidas habilitan solo las opciones correspondientes."""
import pytest

from transmision.motor.sesion import Sesion


def ids_habilitadas(sesion):
    return [o.id for o in sesion.opciones_habilitadas]


@pytest.mark.parametrize(
    "ruta, esperadas",
    [
        # E3 con origen conocido (CA01)
        (["revisar", "investigar"], ["activar_codigo", "cortar"]),
        # E3 sin origen
        (["revisar", "continuar"], ["activar_sin_verificar", "cortar"]),
    ],
)
def test_u1_condiciones_habilitan_solo_las_correspondientes(sesion, ruta, esperadas):
    for id_opcion in ruta:
        sesion.elegir(id_opcion)
    assert sesion.escena.id == "E3"
    assert ids_habilitadas(sesion) == esperadas
    assert len(ids_habilitadas(sesion)) == 2


def test_u1_opcion_sin_condiciones_siempre_se_muestra(sesion):
    assert ids_habilitadas(sesion) == ["revisar"]