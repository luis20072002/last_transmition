# Gestión del cambio de la hora 6 y trazabilidad

Borrador para el informe (sección de cambio) y el anexo (matriz). Los nombres de modelos D1 a D6 corresponden a los diagramas del anexo.

## 1. Solicitud recibida

El colectivo decidió que el lector pueda deshacer su última decisión, revirtiendo todas sus consecuencias. La solicitud reemplaza el acuerdo provisional de no implementar retroceso (pregunta 2 de la sección de preguntas y supuestos), que queda respondida por el cliente.

## 2. Versión de partida y versión posterior

| Versión | Referencia Git | Contenido |
|---|---|---|
| Anterior al cambio | Etiqueta `v1-hora6`, commit `6eb8b14` (15-10-2026 02:37) | Informe v1 (`docs/informe/version1.pdf`), capturas iniciales del tablero, historia de referencia y estructura de carpetas del proyecto con los módulos creados pero sin implementar. |
| Posterior al cambio | Rama `main` desde el commit `ee4cf43` | Motor, validación, consola y deshacer implementados; pruebas U1 a U6 e I1; segunda historia. |

Declaración: al cumplirse la hora 6 la implementación aún no había empezado; la versión guardada contiene la especificación y la estructura, no código ejecutable. Por eso la primera implementación del motor ya incorporó RF20 (commit `ee4cf43`) y no existe un commit intermedio con motor sin retroceso. El enunciado permite que la versión de partida esté incompleta.

## 3. Nuevo requisito

| ID | Necesidad | Requisito | Criterios de aceptación |
|---|---|---|---|
| RF20 | N03, N04, N05 | El lector puede deshacer su última elección válida; se restauran exactamente la escena y todas las variables previas a esa elección. Hay un solo nivel de retroceso. | **CA20.1** Desde E2, "Investigar archivo" lleva a E3 con `conoce_origen` verdadero; deshacer devuelve a E2 con `conoce_origen` falso. **CA20.2** Un segundo deshacer seguido no cambia nada. **CA20.3** Tras CA20.1, "Continuar sin investigar" muestra en E3 "Activar sin verificar" y "Cortar comunicación". **CA20.4** Al comenzar y después de reiniciar no hay retroceso disponible. **CA20.5** Una opción inexistente o no habilitada no modifica la sesión ni el historial. **CA20.6** Desde E4, E5 o E6 deshacer regresa a E3 con los valores previos a esa elección. **CA20.7** Una nueva elección válida vuelve a habilitar el retroceso. |

Requisitos existentes modificados:

| ID | Cambio |
|---|---|
| RF12 | Reiniciar además elimina el historial de retroceso (CA20.4). |
| RF06, RF07 | Una entrada inválida tampoco sustituye el historial de la última elección válida (CA20.5). |

## 4. Análisis de impacto

| Artefacto | ¿Afectado? | Qué cambió |
|---|---|---|
| Requisitos | Sí | Nuevo RF20; RF06, RF07 y RF12 extendidos; pregunta 2 respondida; alcance actualizado (el retroceso pasa de "fuera" a "dentro"). |
| D2 Casos de uso | Sí | Nuevo caso de uso "Deshacer decisión" para el actor Lector. |
| D3 Clases del dominio | Sí | `Sesion` agrega el atributo `_anterior` (escena y variables previas), la propiedad `puede_deshacer` y el método `deshacer()`. `Historia`, `Escena` y `Opcion` no cambian. |
| D4 Secuencia "elegir opción" | Sí | Antes de aplicar los efectos, `Sesion.elegir` guarda la escena y una copia de las variables. |
| D5 Estados de la sesión | Sí | Nuevas transiciones "deshacer" desde En juego, Final y Bloqueada hacia el estado anterior, con la guarda `puede_deshacer`. |
| D1 Contexto, D6 Componentes | No | Mismos actores y componentes; el cambio queda dentro del motor y la interfaz. |
| `motor/sesion.py` | Sí | `elegir()` guarda el estado previo; nuevo `deshacer()`; `reiniciar()` borra el historial. |
| `interfaz/consola.py` | Sí | Comando `d`, visible solo cuando `puede_deshacer` es verdadero. |
| `motor/reglas.py`, `contenido/`, `dominio/` | No | Sin cambios. |
| Formato JSON e historias | No | El cambio no exige tocar ningún archivo de historia. |
| Pruebas | Sí | Nuevo U6 (5 pruebas, una parametrizada con los 3 finales); U5 extendido (reinicio borra historial, sin retroceso al comenzar); I1 extendido (deshacer desde un final con archivo real). |
| Documentación | Sí | `README.md` (controles y ruta de demostración), `docs/formato_contenido.md` (tecla `d`), `ia.md`. |
| Backlog y tablero | Sí | Tarjeta nueva "RF20: deshacer la última decisión" (implementación, pruebas U6, actualización de modelos y trazabilidad). |

Consecuencia arquitectónica: el cambio solo tocó el motor y la interfaz. El contenido, las reglas y el formato de archivo no cambiaron, lo que confirma la separación entre contenido, reglas e interfaz (riesgo R1 y RNF01).

## 5. Evidencia del comportamiento nuevo

| Regla del anexo | Prueba |
|---|---|
| Restauración | `tests/test_sesion.py::test_u6_deshacer_restaura_escena_y_variables_y_consume_el_retroceso` |
| Un solo nivel | La misma prueba (segundo `deshacer()` devuelve falso y no cambia el estado) |
| Ejemplo de la solicitud | `tests/test_sesion.py::test_u6_ejemplo_de_la_solicitud_de_cambio` |
| Inicio y reinicio | `tests/test_sesion.py::test_u5_al_comenzar_no_hay_retroceso`, `test_u5_reiniciar_elimina_el_historial` |
| Entrada inválida | `tests/test_sesion.py::test_u6_entrada_invalida_preserva_el_historial` |
| Nueva elección habilita | `tests/test_sesion.py::test_u6_nueva_eleccion_vuelve_a_habilitar_el_retroceso` |
| Desde un final | `tests/test_sesion.py::test_u6_deshacer_desde_un_final_regresa_a_e3` (E4, E5, E6) |
| Integración | `tests/test_integracion.py::test_i1_recorre_los_tres_finales_y_deshace_desde_un_final` |

Resultado: `evidencias/pytest_ultima_ejecucion.txt`.

## 6. Matriz de trazabilidad

Modelos: D1 Contexto, D2 Casos de uso, D3 Clases del dominio, D4 Secuencia "elegir opción", D5 Estados de la sesión, D6 Componentes. Rutas de código relativas a `src/transmision/`; pruebas relativas a `tests/`.

| Requisito | Necesidad | Modelos | Componente o archivo | Evidencia de verificación |
|---|---|---|---|---|
| RF01 Cargar historia desde archivo | N01 | D1, D2, D6 | `contenido/cargador.py` (`cargar_historia`), `__main__.py` | `test_rnf.py::test_rnf01_segunda_historia_carga_con_el_mismo_motor`; `test_integracion.py::test_i1_segunda_historia_funciona_sin_tocar_el_motor` |
| RF02 Iniciar en `inicio` con variables iniciales | N01 | D3, D5 | `motor/sesion.py` (`Sesion.__init__`) | `test_rnf.py::test_rnf01_segunda_historia_carga_con_el_mismo_motor`; `test_sesion.py::test_u5_reiniciar_restaura_escena_y_variables` |
| RF03 Mostrar texto de la escena | N02 | D2, D4 | `interfaz/consola.py` (`_mostrar`) | `test_integracion.py::test_i1_recorre_los_tres_finales_y_deshace_desde_un_final` |
| RF04 Mostrar solo opciones habilitadas | N02 | D3, D4 | `motor/reglas.py` (`esta_habilitada`), `Sesion.opciones_habilitadas` | `test_reglas.py::test_u1_condiciones_habilitan_solo_las_correspondientes`; `test_u1_opcion_sin_condiciones_siempre_se_muestra` |
| RF05 Aplicar efectos y avanzar | N03 | D4 | `motor/reglas.py` (`aplicar_efectos`), `Sesion.elegir` | `test_sesion.py::test_u2_eleccion_valida_aplica_efectos_y_avanza` |
| RF06 Rechazar opción inexistente o no habilitada | N03 | D4, D5 | `Sesion.elegir`, `dominio/errores.py` (`OpcionInvalida`) | `test_sesion.py::test_u3_opcion_invalida_no_modifica_el_estado`; `test_rnf.py::test_rnf02_id_invalido_en_el_motor_es_error_controlado` |
| RF07 Entrada de lector inválida recuperable | N03 | D4 | `interfaz/consola.py` (`ejecutar`) | `test_rnf.py::test_rnf02_entrada_de_lector_invalida_no_altera_la_partida` |
| RF08 Conservar variables entre escenas | N04 | D3, D5 | `Sesion._variables` | `test_sesion.py::test_u2_eleccion_valida_aplica_efectos_y_avanza` (rutas de 3 pasos); `test_reglas.py::test_u1_condiciones_habilitan_solo_las_correspondientes` |
| RF09 Escena final y aviso de fin | N05 | D5 | `Sesion.es_final`, `consola._mostrar` | `test_integracion.py::test_i1_recorre_los_tres_finales_y_deshace_desde_un_final` |
| RF10 Tres finales alcanzables | N05 | D5 | `historias/la_ultima_transmision.json`, `Sesion` | `test_sesion.py::test_u2_eleccion_valida_aplica_efectos_y_avanza` (E4, E5, E6); `test_integracion.py::test_i1_recorre_los_tres_finales_y_deshace_desde_un_final` |
| RF11 Informar bloqueo | N05 | D5 | `Sesion.bloqueada`, `consola._mostrar` | `test_sesion.py::test_bloqueo_se_informa_y_permite_reiniciar` |
| RF12 Reiniciar | N05 | D2, D5 | `Sesion.reiniciar` | `test_sesion.py::test_u5_reiniciar_restaura_escena_y_variables`; `test_u5_reiniciar_elimina_el_historial` |
| RF13 Rechazar los 9 defectos | N06 | D1, D2, D6 | `contenido/validador.py` (`validar`), `contenido/cargador.py` | `test_validacion.py::test_u4_archivo_defectuoso_se_rechaza_con_causa_e_id`; `test_rnf.py::test_rnf02_archivo_defectuoso_termina_controlado` |
| RF14 Causa y campo o ID en el rechazo | N06 | D6 | `contenido/validador.py`, `dominio/errores.py` (`ErrorContenido`) | `test_validacion.py::test_u4_archivo_defectuoso_se_rechaza_con_causa_e_id`; `test_rnf.py::test_rnf03_mensajes_claros` |
| RF15 Sin partida con archivo rechazado | N06 | D1, D6 | `__main__.py` (`main`), `contenido/cargador.py` | `test_integracion.py::test_i1_programa_completo_rechaza_destino_inexistente_sin_traceback` |
| RF20 Deshacer la última decisión | N03, N04, N05 | D2, D3, D4, D5 | `Sesion.deshacer`, `Sesion.puede_deshacer`, `Sesion.elegir`, `consola.ejecutar` (comando `d`) | `test_sesion.py::test_u6_*` (5 pruebas), `test_u5_al_comenzar_no_hay_retroceso`, `test_u5_reiniciar_elimina_el_historial`; `test_integracion.py::test_i1_recorre_los_tres_finales_y_deshace_desde_un_final` |
| RNF01 Modificabilidad | N01 | D6 | Separación `contenido/`, `motor/`, `interfaz/`; `motor/reglas.py` sin IDs de escena | `test_rnf.py::test_motor_sin_ids_de_historia`; `test_rnf01_*`; `evidencias/rnf01.txt` |
| RNF02 Confiabilidad | N03, N06 | D5, D6 | `__main__.py`, `contenido/cargador.py`, `consola.ejecutar` | `test_rnf.py::test_rnf02_*` (11 archivos + entradas inválidas, subproceso sin Traceback); `evidencias/pytest_ultima_ejecucion.txt` |
| RNF03 Claridad de errores | N06 | D6 | `contenido/validador.py` | `test_rnf.py::test_rnf03_mensajes_claros`; `evidencias/rnf03_revision.md`; `docs/mensajes_error.md` |

Nota: RF16 a RF19 no se usan; se reservaron IDs desde RF20 para el cambio (mitigación del riesgo R2).
