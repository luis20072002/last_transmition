"""Punto de entrada: python -m transmision <archivo.json>"""
import sys

from transmision.contenido.cargador import cargar_historia
from transmision.dominio.errores import ErrorContenido
from transmision.interfaz.consola import ejecutar
from transmision.motor.sesion import Sesion


def main() -> int:
    ruta = sys.argv[1] if len(sys.argv) > 1 else "historias/la_ultima_transmision.json"
    try:
        historia = cargar_historia(ruta)
    except ErrorContenido as error:
        print("No se puede jugar este archivo. Corrige lo siguiente:")
        for mensaje in error.mensajes:
            print(f"  - {mensaje}")
        return 1
    ejecutar(Sesion(historia))
    return 0


if __name__ == "__main__":
    sys.exit(main())