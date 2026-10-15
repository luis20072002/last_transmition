"""Lee un archivo JSON, lo valida y construye la Historia (RF01, RF13 a RF15)."""
import json
from pathlib import Path

from transmision.contenido.validador import validar
from transmision.dominio.errores import ErrorContenido
from transmision.dominio.modelos import Escena, Historia, Opcion


def cargar_historia(ruta) -> Historia:
    """Devuelve una Historia o lanza ErrorContenido con todos los problemas."""
    try:
        texto = Path(ruta).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ErrorContenido([f"No se encontró el archivo '{ruta}'."])
    except (OSError, UnicodeDecodeError):
        raise ErrorContenido([f"No se pudo leer el archivo '{ruta}'."])

    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ErrorContenido(
            [f"El archivo no es un JSON válido (línea {e.lineno}, columna {e.colno})."]
        )

    errores = validar(datos)
    if errores:
        raise ErrorContenido(errores)

    escenas = {}
    for e in datos["escenas"]:
        opciones = tuple(
            Opcion(
                id=o["id"],
                texto=o["texto"],
                destino=o["destino"],
                condiciones=dict(o["condiciones"]),
                efectos=dict(o["efectos"]),
            )
            for o in e["opciones"]
        )
        escenas[e["id"]] = Escena(id=e["id"], texto=e["texto"], final=e["final"], opciones=opciones)

    return Historia(
        titulo=datos["titulo"],
        inicio=datos["inicio"],
        variables=dict(datos["variables"]),
        escenas=escenas,
    )