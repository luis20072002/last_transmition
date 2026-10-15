"""Validación del contenido de una historia (RF13, RF14).

Recibe los datos crudos (lo que devuelve json.load) y devuelve la lista de
problemas encontrados. Una lista vacía significa que la historia es válida.
No importa nada del motor ni de la interfaz.
"""
from typing import Any, List


def validar(datos: Any) -> List[str]:
    """Devuelve todos los problemas encontrados, no solo el primero."""
    # Defecto 1: estructura incorrecta
    if not isinstance(datos, dict):
        return ["El archivo debe contener un objeto JSON en su raíz."]

    errores: List[str] = []

    # Defecto 2: campos obligatorios de la historia
    for campo in ("titulo", "inicio", "variables", "escenas"):
        if campo not in datos:
            errores.append(f"Falta el campo obligatorio '{campo}' de la historia.")

    variables = datos.get("variables")
    if "variables" in datos:
        if not isinstance(variables, dict):
            errores.append("El campo 'variables' debe ser un mapa de nombres a verdadero/falso.")
            variables = {}
        else:
            for nombre, valor in variables.items():
                if not isinstance(valor, bool):
                    errores.append(
                        f"Variable '{nombre}': el valor inicial debe ser verdadero o falso, no {valor!r}."
                    )
    else:
        variables = {}

    escenas = datos.get("escenas")
    if "escenas" in datos and not isinstance(escenas, list):
        errores.append("El campo 'escenas' debe ser una lista.")
        escenas = []
    if escenas is None:
        escenas = []

    # Defecto 4: IDs de escena duplicados (y recolección de IDs válidos)
    ids_escenas = set()
    for escena in escenas:
        if isinstance(escena, dict) and isinstance(escena.get("id"), str):
            if escena["id"] in ids_escenas:
                errores.append(f"Escena '{escena['id']}': el ID está repetido.")
            ids_escenas.add(escena["id"])

    # Defecto 3: escena inicial inexistente
    inicio = datos.get("inicio")
    if "inicio" in datos and inicio not in ids_escenas:
        errores.append(f"El campo 'inicio' apunta a la escena '{inicio}', que no existe.")

    for posicion, escena in enumerate(escenas, start=1):
        errores.extend(_validar_escena(escena, posicion, ids_escenas, variables))

    return errores


def _validar_escena(escena: Any, posicion: int, ids_escenas: set, variables: dict) -> List[str]:
    if not isinstance(escena, dict):
        return [f"La escena número {posicion} debe ser un objeto."]

    errores: List[str] = []
    for campo in ("id", "texto", "final", "opciones"):
        if campo not in escena:
            errores.append(f"Escena número {posicion}: falta el campo obligatorio '{campo}'.")

    nombre = escena.get("id", f"número {posicion}")
    etiqueta = f"Escena '{nombre}'"

    if "final" in escena and not isinstance(escena["final"], bool):
        errores.append(f"{etiqueta}: el campo 'final' debe ser verdadero o falso.")

    opciones = escena.get("opciones")
    if "opciones" in escena and not isinstance(opciones, list):
        errores.append(f"{etiqueta}: el campo 'opciones' debe ser una lista.")
        return errores
    if opciones is None:
        return errores

    # Defecto 9: cantidad de opciones incompatible con el carácter final
    if escena.get("final") is True and len(opciones) > 0:
        errores.append(f"{etiqueta}: es una escena final y no debe tener opciones.")
    if escena.get("final") is False and len(opciones) == 0:
        errores.append(f"{etiqueta}: no es final y debe tener al menos una opción.")

    ids_opciones = set()
    for pos_op, opcion in enumerate(opciones, start=1):
        if not isinstance(opcion, dict):
            errores.append(f"{etiqueta}: la opción número {pos_op} debe ser un objeto.")
            continue

        for campo in ("id", "texto", "destino", "condiciones", "efectos"):
            if campo not in opcion:
                errores.append(
                    f"{etiqueta}, opción número {pos_op}: falta el campo obligatorio '{campo}'."
                )

        nombre_op = opcion.get("id", f"número {pos_op}")
        etiqueta_op = f"{etiqueta}, opción '{nombre_op}'"

        # Defecto 5: ID de opción duplicado dentro de la escena
        if isinstance(opcion.get("id"), str):
            if opcion["id"] in ids_opciones:
                errores.append(f"{etiqueta}: el ID de opción '{opcion['id']}' está repetido.")
            ids_opciones.add(opcion["id"])

        # Defecto 6: destino inexistente
        if "destino" in opcion and opcion["destino"] not in ids_escenas:
            errores.append(f"{etiqueta_op}: el destino '{opcion['destino']}' no existe.")

        # Defectos 7 y 8: variables no declaradas y valores no booleanos
        for campo in ("condiciones", "efectos"):
            if campo not in opcion:
                continue
            mapa = opcion[campo]
            if not isinstance(mapa, dict):
                errores.append(f"{etiqueta_op}: el campo '{campo}' debe ser un mapa.")
                continue
            for variable, valor in mapa.items():
                if variable not in variables:
                    errores.append(
                        f"{etiqueta_op}: la variable '{variable}' en '{campo}' no está declarada."
                    )
                if not isinstance(valor, bool):
                    errores.append(
                        f"{etiqueta_op}: el valor de '{variable}' en '{campo}' debe ser "
                        f"verdadero o falso, no {valor!r}."
                    )

    return errores