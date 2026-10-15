"""Interfaz de consola (RF03, RF07, RF09 a RF12, RF20).

El lector elige por número; aquí se traduce a ID de opción. d = deshacer,
r = reiniciar, s = salir.
"""
from transmision.dominio.errores import OpcionInvalida
from transmision.motor.sesion import Sesion


def _mostrar(sesion: Sesion, escribir) -> None:
    escribir("")
    escribir(sesion.escena.texto)
    if sesion.es_final:
        escribir("\n=== FIN DE LA PARTIDA ===")
    elif sesion.bloqueada:
        escribir("\nNo hay opciones disponibles: la partida está bloqueada.")
    else:
        for numero, opcion in enumerate(sesion.opciones_habilitadas, start=1):
            escribir(f"  {numero}. {opcion.texto}")
    comandos = ["r = reiniciar", "s = salir"]
    if sesion.puede_deshacer:
        comandos.insert(0, "d = deshacer")
    escribir("[" + " | ".join(comandos) + "]")


def ejecutar(sesion: Sesion, leer=input, escribir=print) -> None:
    escribir(f"--- {sesion.titulo} ---")
    while True:
        _mostrar(sesion, escribir)
        try:
            entrada = leer("> ").strip().lower()
        except EOFError:
            return

        if entrada == "s":
            escribir("Hasta pronto.")
            return
        if entrada == "r":
            sesion.reiniciar()
            escribir("Partida reiniciada.")
        elif entrada == "d":
            if sesion.deshacer():
                escribir("Se deshizo la última decisión.")
            else:
                escribir("No hay una decisión que deshacer.")
        elif entrada.isdigit() and not sesion.es_final:
            opciones = sesion.opciones_habilitadas
            numero = int(entrada)
            if 1 <= numero <= len(opciones):
                try:
                    sesion.elegir(opciones[numero - 1].id)
                except OpcionInvalida as error:
                    escribir(str(error))
            else:
                escribir(f"Número fuera de rango. Elige entre 1 y {len(opciones)}.")
        else:
            escribir("Entrada no válida. Escribe un número de la lista, d, r o s.")