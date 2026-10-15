# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software, Universidad Tecnológica de Bolívar.

**Integrantes**

- Josh Robinson Ortega Castellón
- Luis Eduardo Mendoza Angulo

Motor de consola que carga historias desde archivos JSON, muestra solo las opciones cuyas condiciones se cumplen, aplica sus efectos sobre variables booleanas, detecta errores del contenido antes de jugar y permite deshacer la última decisión.

## Versiones requeridas

| Herramienta | Versión |
|---|---|
| Python | 3.10 o superior (probado con 3.14) |
| pytest | 8 o superior (probado con 9.1.1), solo para las pruebas |

El motor usa únicamente la biblioteca estándar de Python (`json`, `dataclasses`, `pathlib`, `typing`). No requiere internet, base de datos ni cuentas.

## Instalación

```bash
git clone https://github.com/luis20072002/last_transmition.git
cd last_transmition
python -m pip install -r requirements.txt
```

Si se recibe el ZIP, basta con descomprimirlo y abrir una terminal en la carpeta raíz del proyecto (la que contiene este README).

## Ejecución

El código vive en `src/`, por lo que hay que indicarle a Python esa carpeta con la variable `PYTHONPATH`. Todos los comandos se ejecutan desde la raíz del proyecto.

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = "src"
python -m transmision historias/la_ultima_transmision.json
```

**Windows (cmd)**

```bat
set PYTHONPATH=src
python -m transmision historias/la_ultima_transmision.json
```

**Linux / macOS / Git Bash**

```bash
PYTHONPATH=src python -m transmision historias/la_ultima_transmision.json
```

Si no se indica archivo, se carga `historias/la_ultima_transmision.json`. Para jugar la segunda historia con el mismo motor:

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = "src"
python -m transmision historias/historia2.json
```

**Windows (cmd)**

```bat
set PYTHONPATH=src
python -m transmision historias/historia2.json
```

**Linux / macOS / Git Bash**

```bash
PYTHONPATH=src python -m transmision historias/historia2.json
```

### Controles

| Tecla | Acción |
|---|---|
| `1`, `2`, ... | Elegir la opción con ese número |
| `d` | Deshacer la última decisión (solo un nivel; aparece cuando está disponible) |
| `r` | Reiniciar la partida |
| `s` | Salir |

## Pruebas

```bash
# PowerShell / cmd / bash: pytest ya toma src/ desde pytest.ini
python -m pytest -v
```

Resultado de la última ejecución: `evidencias/pytest_ultima_ejecucion.txt` (74 pruebas, todas aprobadas).

| Escenario | Archivo | Qué comprueba |
|---|---|---|
| U1 | `tests/test_reglas.py` | Las condiciones habilitan solo las opciones correspondientes |
| U2 | `tests/test_sesion.py` | Una elección válida aplica efectos y avanza al destino |
| U3 | `tests/test_sesion.py` | Una opción inexistente o no habilitada no altera el estado |
| U4 | `tests/test_validacion.py` | Los 9 tipos de error de contenido se rechazan con causa e ID |
| U5 | `tests/test_sesion.py` | Reiniciar restaura escena y variables y elimina el historial |
| U6 | `tests/test_sesion.py` | Deshacer restaura escena y variables y consume el retroceso |
| Bloqueo | `tests/test_sesion.py` | Escena no final sin opciones habilitadas: se informa y se puede reiniciar |
| I1 | `tests/test_integracion.py` | Archivo real + motor + consola hasta los tres finales, deshacer desde un final |
| RNF01-03 | `tests/test_rnf.py` | Modificabilidad, confiabilidad y claridad de errores |

## Rutas para demostrar cada final

Historia de referencia (`historias/la_ultima_transmision.json`). Se escriben los números en orden:

| Final | Entradas | Recorrido |
|---|---|---|
| E4 Rescate | `1`, `1`, `1` | Revisar señal → Investigar archivo → Activar con código |
| E5 El eco | `1`, `2`, `1` | Revisar señal → Continuar sin investigar → Activar sin verificar |
| E6 Silencio | `1`, `1`, `2` | Revisar señal → Investigar archivo → Cortar comunicación |

Cómo una condición cambia las opciones: en E3, si se investigó el archivo aparece "Activar con código"; si no, aparece "Activar sin verificar".

Deshacer (solicitud de cambio de la hora 6): `1`, `1`, `d` vuelve a E2 con `conoce_origen` en falso; un segundo `d` no cambia nada; luego `2` (continuar sin investigar) muestra en E3 "Activar sin verificar" y "Cortar comunicación". Desde cualquier final, `d` regresa a E3.

Capturas de los tres recorridos en consola: `docs/finales/historia/111.png` (E4), `121.png` (E5) y `112.png` (E6).

## Segunda historia: "El faro sin luz"

Archivo `historias/historia2.json`. Demuestra que el motor carga y juega otra historia sin modificar código (RNF01): usa IDs de escena distintos a E1–E6, otra variable y su propia condición y efecto.

Una tormenta obliga a una guardacostas a refugiarse en un faro apagado; según tome o no la llave, podrá encender el faro o lo dejará a oscuras.

| Escena | Tipo | Opciones (condición → efecto) |
|---|---|---|
| `entrada` | Inicio | "Tomar la llave" (sin condición → `tiene_llave` = verdadero) y "Ir directo a la puerta" (sin condición, sin efecto); ambas llevan a `puerta` |
| `puerta` | Decisión | "Abrir el candado con la llave" solo si `tiene_llave` = verdadero → `luz_encendida`; "Forzar la puerta a golpes" solo si `tiene_llave` = falso → `oscuridad` |
| `luz_encendida` | Final | El faro vuelve a guiar a los barcos |
| `oscuridad` | Final | El faro queda a oscuras hasta el amanecer |

Estado inicial: escena `entrada`, `tiene_llave` = falso. En `puerta` siempre se ve una sola opción, la que corresponde a lo que hizo el lector antes.

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = "src"
python -m transmision historias/historia2.json
```

**Windows (cmd)**

```bat
set PYTHONPATH=src
python -m transmision historias/historia2.json
```

**Linux / macOS / Git Bash**

```bash
PYTHONPATH=src python -m transmision historias/historia2.json
```

| Final | Entradas |
|---|---|
| Luz encendida | `1`, `1` (tomar la llave, abrir el candado) |
| Oscuridad | `2`, `1` (ir sin llave, forzar la puerta) |

Deshacer también funciona aquí: `1`, `d` vuelve a `entrada` con `tiene_llave` en falso.

Verificación: `tests/test_integracion.py::test_i1_segunda_historia_funciona_sin_tocar_el_motor`, `tests/test_rnf.py::test_rnf01_segunda_historia_carga_con_el_mismo_motor` y `evidencias/rnf01.txt`.

## Error de contenido

Archivo con un destino inexistente (E99):

**Windows (PowerShell)**

```powershell
$env:PYTHONPATH = "src"
python -m transmision tests/datos/invalidos/destino_inexistente.json
```

**Windows (cmd)**

```bat
set PYTHONPATH=src
python -m transmision tests/datos/invalidos/destino_inexistente.json
```

**Linux / macOS / Git Bash**

```bash
PYTHONPATH=src python -m transmision tests/datos/invalidos/destino_inexistente.json
```

En `tests/datos/invalidos/` hay un archivo de ejemplo por cada tipo de error.

## Formato de contenido

Se usa el contrato JSON de referencia del enunciado sin cambios de significado:

| Elemento | Campos |
|---|---|
| Historia | `titulo` (texto), `inicio` (ID de escena), `variables` (mapa de booleanos iniciales), `escenas` (lista) |
| Escena | `id` (único), `texto`, `final` (booleano), `opciones` (lista, vacía si es final) |
| Opción | `id` (único dentro de la escena), `texto`, `destino` (ID existente), `condiciones` (mapa de igualdades), `efectos` (mapa de asignaciones) |

Un mapa `condiciones` vacío habilita siempre la opción; si tiene entradas, deben cumplirse todas. Un mapa `efectos` vacío conserva las variables.

La guía para escritores, con ejemplos y reglas, está en `docs/formato_contenido.md`. El catálogo de mensajes de error está en `docs/mensajes_error.md`.

## Estructura del proyecto

```
src/transmision/
  dominio/     Historia, Escena, Opcion y errores propios (datos puros)
  contenido/   Lectura del JSON (cargador) y validación de los 9 defectos
  motor/       Reglas (condiciones y efectos) y Sesion (elegir, reiniciar, deshacer)
  interfaz/    Consola: traduce números a IDs de opción y muestra el estado
historias/     Historia de referencia y segunda historia
tests/         Pruebas automatizadas y archivos defectuosos de prueba
evidencias/    Resultado de pruebas, verificación de RNF e historial de Git
docs/          Informe, guía de formato, mensajes de error y capturas del tablero
```

## Versiones en Git

| Versión | Referencia |
|---|---|
| Anterior al cambio (hora 6) | Etiqueta `v1-hora6` (commit `6eb8b14`) |
| Posterior al cambio | Rama `main` |

## Limitaciones conocidas

- Solo interfaz de consola.
- Deshacer tiene un único nivel y no existe rehacer (así lo pide la solicitud de cambio).
- Las condiciones solo comparan igualdad con verdadero o falso; no hay lenguaje de expresiones.
- No se guarda la partida entre ejecuciones.
- No se analizan automáticamente todos los caminos de una historia: un bloqueo (escena no final sin opciones habilitadas) se detecta durante la partida y se informa, permitiendo reiniciar.
- Si el JSON tiene un error de sintaxis, solo se informa el primero (línea y columna), porque el lector de JSON se detiene ahí. Los errores de estructura sí se informan todos juntos.

## Uso de IA

El registro de uso de herramientas de IA, su finalidad y cómo se verificó cada resultado está en `ia.md`.
