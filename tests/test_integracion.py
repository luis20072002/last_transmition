"""I1: lectura de archivos reales + motor + consola funcionando juntos."""
import os
import subprocess
import sys

from conftest import RAIZ, RUTA_HISTORIA2, RUTA_REFERENCIA
from transmision.contenido.cargador import cargar_historia
from transmision.interfaz.consola import ejecutar
from transmision.motor.sesion import Sesion


def jugar(ruta, entradas):
    """Ejecuta la consola con entradas simuladas y devuelve lo impreso."""
    salida = []
    pendientes = iter(entradas)
    ejecutar(Sesion(cargar_historia(ruta)), leer=lambda _: next(pendientes), escribir=salida.append)
    return "\n".join(salida)


def test_i1_recorre_los_tres_finales_y_deshace_desde_un_final():
    # 1=revisar, 1=investigar, luego en E3: 1=activar con código -> E4
    assert "FIN DE LA PARTIDA" in jugar(RUTA_REFERENCIA, ["1", "1", "1", "s"])
    # continuar sin investigar -> activar sin verificar -> E5
    assert "FIN DE LA PARTIDA" in jugar(RUTA_REFERENCIA, ["1", "2", "1", "s"])
    # cortar comunicación -> E6
    assert "FIN DE LA PARTIDA" in jugar(RUTA_REFERENCIA, ["1", "1", "2", "s"])
    # deshacer desde el final vuelve a E3 con sus opciones
    texto = jugar(RUTA_REFERENCIA, ["1", "1", "1", "d", "s"])
    assert "Se deshizo la última decisión." in texto
    assert "Activar con código" in texto.split("Se deshizo")[1]


def test_i1_segunda_historia_funciona_sin_tocar_el_motor():
    con_llave = jugar(RUTA_HISTORIA2, ["1", "1", "s"])      # tomar llave, abrir candado
    assert "FIN DE LA PARTIDA" in con_llave
    sin_llave = jugar(RUTA_HISTORIA2, ["2", "1", "s"])      # sin llave, forzar puerta
    assert "FIN DE LA PARTIDA" in sin_llave


def test_i1_programa_completo_rechaza_destino_inexistente_sin_traceback():
    env = dict(os.environ, PYTHONPATH=str(RAIZ / "src"))
    resultado = subprocess.run(
        [sys.executable, "-m", "transmision", str(RAIZ / "tests" / "datos" / "invalidos" / "destino_inexistente.json")],
        capture_output=True, text=True, env=env, cwd=RAIZ,
    )
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 1
    assert "E99" in salida
    assert "Traceback" not in salida