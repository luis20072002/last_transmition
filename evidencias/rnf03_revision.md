# RNF03: claridad de errores (revisión cruzada)

**Requisito:** todo mensaje de rechazo incluye la causa y el campo o ID involucrado, está en español y no contiene nombres internos del código.

**Métrica y umbral:** 9 de 9 categorías de error con mensaje que indica causa y campo o ID; 0 mensajes con nombres de clases o excepciones.

## Parte 1: verificación automática

Prueba `tests/test_rnf.py::test_rnf03_mensajes_claros`, parametrizada con los 11 archivos de `tests/datos/invalidos/`. Para cada archivo comprueba que:

- el archivo se rechaza con al menos un mensaje;
- el mensaje contiene el campo o ID esperado;
- el mensaje no contiene `Error`, `Exception`, `Traceback`, `JSONDecode`, `KeyError` ni `TypeError`.

Resultado: 11 de 11 casos aprobados (ver `evidencias/pytest_ultima_ejecucion.txt`).

## Parte 2: revisión cruzada entre integrantes

Procedimiento: un integrante que no escribió el validador lee cada mensaje sin abrir el archivo defectuoso ni el código y responde si sabría qué corregir y dónde. Los mensajes se obtuvieron ejecutando `python -m transmision <archivo>` con la versión del commit indicado al final.

| # | Categoría de error (enunciado) | Archivo | Mensaje que ve la escritora | Causa | Campo o ID | ¿Sabría qué corregir? |
|---|---|---|---|---|---|---|
| 1 | Archivo ilegible o estructura incorrecta | `ilegible.json` | El archivo no es un JSON válido (línea 1, columna 3). | Sí | Línea y columna | |
| 1 | Archivo ilegible o estructura incorrecta | `raiz_lista.json` | El archivo debe contener un objeto JSON en su raíz. | Sí | Raíz | |
| 2 | Campo obligatorio ausente | `sin_inicio.json` | Falta el campo obligatorio 'inicio' de la historia. | Sí | `inicio` | |
| 3 | Inicio inexistente | `inicio_inexistente.json` | El campo 'inicio' apunta a la escena 'Z', que no existe. | Sí | `inicio`, `Z` | |
| 4 | ID de escena duplicado | `escena_duplicada.json` | Escena 'B': el ID está repetido. | Sí | `B` | |
| 5 | ID de opción duplicado en la escena | `opcion_duplicada.json` | Escena 'A': el ID de opción 'o' está repetido. | Sí | `A`, `o` | |
| 6 | Destino inexistente | `destino_inexistente.json` | Escena 'A', opción 'o': el destino 'E99' no existe. | Sí | `A`, `o`, `E99` | |
| 7 | Variable no declarada | `variable_no_declarada.json` | Escena 'A', opción 'o': la variable 'y' en 'efectos' no está declarada. | Sí | `A`, `o`, `y` | |
| 8 | Valor no booleano | `valor_no_booleano.json` | Escena 'A', opción 'o': el valor de 'x' en 'condiciones' debe ser verdadero o falso, no 'si'. | Sí | `A`, `o`, `x` | |
| 9 | Opciones incompatibles con el carácter final | `final_con_opciones.json` | Escena 'B': es una escena final y no debe tener opciones. | Sí | `B` | |
| 9 | Opciones incompatibles con el carácter final | `no_final_sin_opciones.json` | Escena 'A': no es final y debe tener al menos una opción. | Sí | `A` | |

Revisor: _______________________  Fecha: ____________  Commit: ____________

## Resultado

- Categorías con causa y campo o ID: ___ de 9.
- Mensajes con nombres internos del código: ___.
- Observaciones o mensajes que se reescribieron tras la revisión:

## Respuesta ante bloqueo durante la partida

Una escena no final sin opciones habilitadas no es un error del archivo, sino del recorrido. La consola muestra "No hay opciones disponibles: la partida está bloqueada." y ofrece reiniciar (`r`). Se cubre en `tests/test_sesion.py::test_bloqueo_se_informa_y_permite_reiniciar`.
