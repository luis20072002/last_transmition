"""U2, U3, U5 y U6: elegir, entradas inválidas, reiniciar y deshacer."""
import pytest

from transmision.dominio.errores import OpcionInvalida


def estado(sesion):
    return (sesion.escena.id, sesion.variables, sesion.puede_deshacer)


# ---------- U2: una elección válida aplica efectos y avanza ----------
@pytest.mark.parametrize(
    "ruta, escena_final, variables_esperadas",
    [
        (["revisar"], "E2", {"conoce_origen": False, "confia_en_la_voz": False}),
        (["revisar", "investigar"], "E3", {"conoce_origen": True, "confia_en_la_voz": False}),
        (["revisar", "continuar"], "E3", {"conoce_origen": False, "confia_en_la_voz": False}),
        (["revisar", "investigar", "activar_codigo"], "E4", {"conoce_origen": True, "confia_en_la_voz": True}),
        (["revisar", "continuar", "activar_sin_verificar"], "E5", {"conoce_origen": False, "confia_en_la_voz": True}),
        (["revisar", "investigar", "cortar"], "E6", {"conoce_origen": True, "confia_en_la_voz": False}),
    ],
)
def test_u2_eleccion_valida_aplica_efectos_y_avanza(sesion, ruta, escena_final, variables_esperadas):
    for id_opcion in ruta:
        sesion.elegir(id_opcion)
    assert sesion.escena.id == escena_final
    assert sesion.variables == variables_esperadas


# ---------- U3: opción inexistente o no habilitada deja el estado intacto ----------
@pytest.mark.parametrize(
    "ruta_previa, id_invalido",
    [
        ([], "inexistente"),                                  # no existe
        (["revisar", "continuar"], "activar_codigo"),          # existe pero no habilitada (CA02)
        (["revisar", "investigar"], "activar_sin_verificar"),  # existe pero no habilitada
        (["revisar"], ""),                                     # vacía
    ],
)
def test_u3_opcion_invalida_no_modifica_el_estado(sesion, ruta_previa, id_invalido):
    for id_opcion in ruta_previa:
        sesion.elegir(id_opcion)
    antes = estado(sesion)
    with pytest.raises(OpcionInvalida):
        sesion.elegir(id_invalido)
    assert estado(sesion) == antes


# ---------- U5: reiniciar restaura el estado inicial y elimina el historial ----------
def test_u5_reiniciar_restaura_escena_y_variables(sesion):
    for id_opcion in ["revisar", "investigar", "activar_codigo"]:
        sesion.elegir(id_opcion)
    assert sesion.escena.id == "E4"
    sesion.reiniciar()
    assert sesion.escena.id == "E1"
    assert sesion.variables == {"conoce_origen": False, "confia_en_la_voz": False}


def test_u5_reiniciar_elimina_el_historial(sesion):
    sesion.elegir("revisar")
    assert sesion.puede_deshacer is True
    sesion.reiniciar()
    assert sesion.puede_deshacer is False
    assert sesion.deshacer() is False
    assert sesion.escena.id == "E1"


def test_u5_al_comenzar_no_hay_retroceso(sesion):
    assert sesion.puede_deshacer is False
    assert sesion.deshacer() is False


# ---------- U6: deshacer ----------
def test_u6_deshacer_restaura_escena_y_variables_y_consume_el_retroceso(sesion):
    sesion.elegir("revisar")
    sesion.elegir("investigar")
    assert sesion.escena.id == "E3"
    assert sesion.variables["conoce_origen"] is True

    assert sesion.deshacer() is True
    assert sesion.escena.id == "E2"
    assert sesion.variables == {"conoce_origen": False, "confia_en_la_voz": False}
    assert sesion.puede_deshacer is False          # consumido

    antes = estado(sesion)
    assert sesion.deshacer() is False              # un solo nivel
    assert estado(sesion) == antes


def test_u6_ejemplo_de_la_solicitud_de_cambio(sesion):
    sesion.elegir("revisar")
    sesion.elegir("investigar")
    sesion.deshacer()
    sesion.elegir("continuar")
    assert [o.id for o in sesion.opciones_habilitadas] == ["activar_sin_verificar", "cortar"]


def test_u6_entrada_invalida_preserva_el_historial(sesion):
    sesion.elegir("revisar")
    sesion.elegir("investigar")                    # historial: estado en E2
    with pytest.raises(OpcionInvalida):
        sesion.elegir("activar_sin_verificar")     # no habilitada
    with pytest.raises(OpcionInvalida):
        sesion.elegir("inexistente")
    assert sesion.puede_deshacer is True
    assert sesion.deshacer() is True
    assert sesion.escena.id == "E2"                # sigue restaurando la última elección válida
    assert sesion.variables["conoce_origen"] is False


def test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso(sesion):
    sesion.elegir("revisar")
    sesion.elegir("investigar")
    sesion.deshacer()
    assert sesion.puede_deshacer is False
    sesion.elegir("continuar")
    assert sesion.puede_deshacer is True
    assert sesion.deshacer() is True
    assert sesion.escena.id == "E2"


@pytest.mark.parametrize(
    "ruta, opcion_final, variables_previas",
    [
        (["revisar", "investigar"], "activar_codigo", {"conoce_origen": True, "confia_en_la_voz": False}),
        (["revisar", "continuar"], "activar_sin_verificar", {"conoce_origen": False, "confia_en_la_voz": False}),
        (["revisar", "investigar"], "cortar", {"conoce_origen": True, "confia_en_la_voz": False}),
    ],
)
def test_u6_deshacer_desde_un_final_regresa_a_e3(sesion, ruta, opcion_final, variables_previas):
    for id_opcion in ruta:
        sesion.elegir(id_opcion)
    sesion.elegir(opcion_final)
    assert sesion.es_final is True
    assert sesion.deshacer() is True
    assert sesion.escena.id == "E3"
    assert sesion.variables == variables_previas

# ---------- Bloqueo: escena no final sin opciones habilitadas (RF11) ----------
def _historia_con_bloqueo():
    """El archivo es válido, pero la única opción de 'pasillo' exige una variable que ya cambió."""
    from transmision.dominio.modelos import Escena, Historia, Opcion

    return Historia(
        titulo="Bloqueo",
        inicio="sala",
        variables={"abierta": True},
        escenas={
            "sala": Escena("sala", "Sala.", False, (Opcion("cerrar", "Cerrar", "pasillo", {}, {"abierta": False}),)),
            "pasillo": Escena("pasillo", "Pasillo.", False, (Opcion("salir", "Salir", "fin", {"abierta": True}, {}),)),
            "fin": Escena("fin", "Fin.", True, ()),
        },
    )


def test_bloqueo_se_informa_y_permite_reiniciar():
    from transmision.interfaz.consola import ejecutar
    from transmision.motor.sesion import Sesion

    sesion = Sesion(_historia_con_bloqueo())
    sesion.elegir("cerrar")
    assert sesion.bloqueada is True
    assert sesion.es_final is False
    assert sesion.opciones_habilitadas == []

    salida = []
    entradas = iter(["1", "r", "s"])
    ejecutar(sesion, leer=lambda _: next(entradas), escribir=salida.append)
    texto = "\n".join(salida)
    assert "la partida está bloqueada" in texto
    assert "Partida reiniciada." in texto
    assert sesion.escena.id == "sala"
    assert sesion.variables == {"abierta": True}
