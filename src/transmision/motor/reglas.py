"""Reglas puras del juego: evaluar condiciones y aplicar efectos (RF04, RF05).

No conoce ninguna historia concreta ni identificadores de escena (RNF01).
"""
from typing import Dict

from transmision.dominio.modelos import Opcion


def esta_habilitada(opcion: Opcion, variables: Dict[str, bool]) -> bool:
    """Una opción sin condiciones siempre está habilitada; si tiene, deben cumplirse todas."""
    return all(variables.get(nombre) == valor for nombre, valor in opcion.condiciones.items())


def aplicar_efectos(opcion: Opcion, variables: Dict[str, bool]) -> Dict[str, bool]:
    """Devuelve una copia nueva de las variables con los efectos aplicados."""
    nuevas = dict(variables)
    nuevas.update(opcion.efectos)
    return nuevas