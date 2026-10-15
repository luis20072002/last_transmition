"""RNF01 (modificabilidad), RNF02 (confiabilidad) y RNF03 (claridad de errores)."""
import json
import os
import re
import subprocess
import sys

import pytest

from conftest import RAIZ, RUTA_HISTORIA2, RUTA_REFERENCIA
from transmision.contenido.cargador import cargar_historia
from transmision.dominio.errores import ErrorContenido, OpcionInvalida
from transmision.interfaz.consola import ejecutar
from transmision.motor.sesion import Sesion

INVALIDOS = RAIZ / "tests" / "datos" / "invalidos"
ARCHIVOS_INVALIDOS = sorted(INVALIDOS.glob("*.json"))
ENV = dict(os.environ, PYTHONPATH=str(RAIZ / "src"))


# ======================= RNF01: modificabilidad =======================
def test_motor_sin_ids_de_historia():
    """0 apariciones de E1 a E6 en el código fuente."""
    patron = re.compile(r"\bE[1-6]\b")
    encontrados = []
    for archivo in (RAIZ / "src").rglob("*.py"):
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            if patron.search(linea):
                encontrados.append(f"{archivo.name}:{n}: {linea.strip()}")
    assert encontrados == [], "IDs de la historia en el código:\n" + "\n".join(encontrados)


def test_rnf01_segunda_historia_carga_con_el_mismo_motor():
    historia = cargar_historia(RUTA_HISTORIA2)
    sesion = Sesion(historia)
    assert historia.titulo != cargar_historia(RUTA_REFERENCIA).titulo
    assert sesion.escena.id == historia.inicio


def test_rnf01_editar_el_archivo_cambia_el_comportamiento(tmp_path):
    """Cambiar un destino en una copia del JSON se refleja sin tocar código."""
    datos = json.loads(RUTA_REFERENCIA.read_text(encoding="utf-8"))
    for escena in datos["escenas"]:
        for opcion in escena["opciones"]:
            if opcion["id"] == "investigar":
                opcion["destino"] = "E4"
    copia = tmp_path / "editada.json"
    copia.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")

    sesion = Sesion(cargar_historia(copia))
    sesion.elegir("revisar")
    sesion.elegir("investigar")
    assert sesion.escena.id == "E4"


# ======================= RNF02: confiabilidad =======================
def test_rnf02_hay_11_archivos_defectuosos():
    assert len(ARCHIVOS_INVALIDOS) == 11


@pytest.mark.parametrize("archivo", ARCHIVOS_INVALIDOS, ids=lambda a: a.stem)
def test_rnf02_archivo_defectuoso_termina_controlado(archivo):
    resultado = subprocess.run(
        [sys.executable, "-m", "transmision", str(archivo)],
        capture_output=True, text=True, env=ENV, cwd=RAIZ,
    )
    salida = resultado.stdout + resultado.stderr
    assert resultado.returncode == 1
    assert "Traceback" not in salida
    assert "Corrige lo siguiente" in resultado.stdout


@pytest.mark.parametrize("entrada", ["", "abc", "0", "-1", "7", "1.5", "   "])
def test_rnf02_entrada_de_lector_invalida_no_altera_la_partida(entrada):
    sesion = Sesion(cargar_historia(RUTA_REFERENCIA))
    salida = []
    pendientes = iter([entrada, "s"])
    ejecutar(sesion, leer=lambda _: next(pendientes), escribir=salida.append)
    texto = "\n".join(salida)
    assert "Entrada no válida" in texto or "fuera de rango" in texto
    assert sesion.escena.id == "E1"
    assert sesion.puede_deshacer is False


@pytest.mark.parametrize(
    "ruta_previa, id_invalido",
    [([], "inexistente"), (["revisar", "continuar"], "activar_codigo")],
)
def test_rnf02_id_invalido_en_el_motor_es_error_controlado(ruta_previa, id_invalido):
    sesion = Sesion(cargar_historia(RUTA_REFERENCIA))
    for id_opcion in ruta_previa:
        sesion.elegir(id_opcion)
    antes = (sesion.escena.id, sesion.variables)
    with pytest.raises(OpcionInvalida):
        sesion.elegir(id_invalido)
    assert (sesion.escena.id, sesion.variables) == antes


# ======================= RNF03: claridad de errores =======================
CAMPO_ESPERADO = {
    "ilegible": "línea",
    "raiz_lista": "raíz",
    "sin_inicio": "'inicio'",
    "inicio_inexistente": "'Z'",
    "escena_duplicada": "'B'",
    "opcion_duplicada": "'o'",
    "destino_inexistente": "'E99'",
    "variable_no_declarada": "'y'",
    "valor_no_booleano": "'x'",
    "final_con_opciones": "'B'",
    "no_final_sin_opciones": "'A'",
}
PROHIBIDOS = ["Error", "Exception", "Traceback", "JSONDecode", "KeyError", "TypeError"]


@pytest.mark.parametrize("nombre, campo", CAMPO_ESPERADO.items())
def test_rnf03_mensajes_claros(nombre, campo):
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(INVALIDOS / f"{nombre}.json")
    assert info.value.mensajes, "No hay mensajes"
    for mensaje in info.value.mensajes:
        for palabra in PROHIBIDOS:
            assert palabra not in mensaje, f"Nombre interno '{palabra}' en: {mensaje}"
    assert campo in "\n".join(info.value.mensajes)