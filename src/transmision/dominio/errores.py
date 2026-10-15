"""Errores propios del dominio, con mensajes en español."""
from typing import List


class ErrorContenido(Exception):
    """El archivo de historia no es válido (RF13, RF14).

    Guarda todos los problemas encontrados, no solo el primero.
    """

    def __init__(self, mensajes: List[str]):
        self.mensajes = list(mensajes)
        super().__init__("\n".join(self.mensajes))


class OpcionInvalida(Exception):
    """La opción elegida no existe o no está habilitada (RF06)."""