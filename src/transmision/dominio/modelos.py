"""Modelos del dominio: Historia, Escena y Opcion.

Son datos puros e inmutables. No leen archivos ni imprimen nada.
"""
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class Opcion:
    id: str
    texto: str
    destino: str
    condiciones: Dict[str, bool]
    efectos: Dict[str, bool]


@dataclass(frozen=True)
class Escena:
    id: str
    texto: str
    final: bool
    opciones: Tuple[Opcion, ...]


@dataclass(frozen=True)
class Historia:
    titulo: str
    inicio: str
    variables: Dict[str, bool]
    escenas: Dict[str, Escena]  # clave: id de la escena