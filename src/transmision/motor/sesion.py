"""Estado de una partida: elegir, finales, bloqueo, reinicio y deshacer
(RF05 a RF12 y RF20)."""
from typing import Dict, List, Optional, Tuple

from transmision.dominio.errores import OpcionInvalida
from transmision.dominio.modelos import Escena, Historia, Opcion
from transmision.motor.reglas import aplicar_efectos, esta_habilitada


class Sesion:
    def __init__(self, historia: Historia):
        self._historia = historia
        self._escena_id: str = historia.inicio
        self._variables: Dict[str, bool] = dict(historia.variables)
        # Un solo nivel de retroceso: (escena_id, variables) previos a la última elección válida.
        self._anterior: Optional[Tuple[str, Dict[str, bool]]] = None

    # ---- consulta ----
    @property
    def escena(self) -> Escena:
        return self._historia.escenas[self._escena_id]

    @property
    def variables(self) -> Dict[str, bool]:
        return dict(self._variables)

    @property
    def opciones_habilitadas(self) -> List[Opcion]:
        return [o for o in self.escena.opciones if esta_habilitada(o, self._variables)]

    @property
    def es_final(self) -> bool:
        return self.escena.final

    @property
    def bloqueada(self) -> bool:
        """Escena no final sin ninguna opción habilitada (RF11)."""
        return (not self.escena.final) and not self.opciones_habilitadas

    @property
    def puede_deshacer(self) -> bool:
        return self._anterior is not None

    # ---- acciones ----
    def elegir(self, id_opcion: str) -> None:
        """Aplica una opción válida. Si no existe o no está habilitada, no cambia nada (RF06)."""
        for opcion in self.opciones_habilitadas:
            if opcion.id == id_opcion:
                self._anterior = (self._escena_id, dict(self._variables))
                self._variables = aplicar_efectos(opcion, self._variables)
                self._escena_id = opcion.destino
                return
        raise OpcionInvalida(f"La opción '{id_opcion}' no está disponible en esta escena.")

    def deshacer(self) -> bool:
        """Restaura escena y variables previas a la última elección válida (RF20).

        Devuelve False si no hay nada que deshacer (no cambia nada).
        """
        if self._anterior is None:
            return False
        self._escena_id, self._variables = self._anterior
        self._anterior = None  # un solo nivel: no se permite otro retroceso
        return True

    def reiniciar(self) -> None:
        """Restaura el estado inicial y elimina el historial (RF12)."""
        self._escena_id = self._historia.inicio
        self._variables = dict(self._historia.variables)
        self._anterior = None