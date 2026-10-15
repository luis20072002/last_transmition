# Borrador de secciones faltantes del informe

Texto para revisar, ajustar a lo que realmente hicieron y pasar al PDF. Las partes entre corchetes `[...]` las tienen que completar ustedes.

---

## Unidad 1: decisión de responsabilidad profesional

**Decisión: declarar el uso de IA y distinguir el trabajo propio del adaptado (autoría).** Usamos un asistente de IA para borradores de documentos y de código. Decidimos registrar cada uso en `ia.md` con su finalidad, qué se aceptó o cambió y cómo se verificó, y no incorporar código que no entendiéramos ni hubiéramos probado. Alternativa descartada: usar la herramienta sin registro, que haría pasar como propio material generado e impediría al docente distinguir la autoría. Consecuencia: cada artefacto generado tiene una verificación asociada (pruebas automatizadas o revisión entre integrantes).

Complemento sobre datos: el motor no recoge ni guarda información del lector (no hay cuentas ni guardado entre ejecuciones), por lo que no maneja datos personales.

---

## Unidad 3: agilidad

### Backlog y tablero

Tablero Kanban en GitHub Projects ("Tablero kanban Last transmition") con columnas Backlog, Ready, In progress, In review y Done, y un responsable por tarjeta. Capturas iniciales: `docs/tablero/imagen1 inicial.jpeg` e `imagen 2 inicial.jpeg`. Captura final: `docs/tablero/[nombre].png`. Tras la solicitud de la hora 6 se agregó la tarjeta "RF20: deshacer la última decisión".

### Dos prácticas ágiles aplicadas

| Práctica | Cómo la aplicamos | Por qué |
|---|---|---|
| Tablero Kanban con límite de trabajo en curso | Máximo 2 tarjetas en curso por persona; una tarjeta pasa a Done solo si cumple la definición de terminado. | Hace visible el avance de la pareja sin reuniones y permitió absorber el cambio de la hora 6 como una tarjeta más. |
| Pruebas automatizadas en cada incremento | Cada incremento (carga, motor, consola, validación, deshacer) llega con sus pruebas; la suite se ejecuta antes de cada commit. | Permitió incorporar el deshacer comprobando que nada de lo anterior se rompía (74 pruebas). |

### Alternativa descartada

**Estimación con planning poker y sprints.** Se descartó porque con 12 horas y dos personas la sesión de estimación consume tiempo sin cambiar las decisiones, y porque el tablero de flujo continuo no necesita un compromiso de capacidad por sprint. Por eso el campo de estimación del tablero quedó en 0.

### Definición de terminado

Una tarjeta pasa a Done solo si:

1. El código está en `main` y el programa se ejecuta con el comando del README.
2. Tiene pruebas automatizadas que pasan, y la suite completa sigue pasando.
3. Los requisitos afectados tienen criterio de aceptación y aparecen en la matriz de trazabilidad.
4. Los modelos y la documentación afectados (informe, README, guía de formato) están actualizados.
5. El otro integrante lo revisó.

### Aprendizaje y acción de mejora

**Aprendizaje:** varias tarjetas se movieron a Done sin cumplir la definición de terminado (por ejemplo, la de modelado y arquitectura estaba en Done sin diagramas, y la de la segunda historia en revisión con el README vacío). El tablero mostraba más avance del real.

**Acción de mejora:** antes de mover una tarjeta a Done, el otro integrante revisa la lista de la definición de terminado y deja en la tarjeta la ruta del archivo o la prueba que la demuestra.

---

## Unidad 6: arquitectura

Diagrama de componentes: anexo, D6.

### Responsabilidades

| Componente | Responsabilidad | Depende de |
|---|---|---|
| `dominio` | Datos inmutables (`Historia`, `Escena`, `Opcion`) y errores propios | Nada |
| `contenido` | Leer el JSON, validar los 9 defectos y construir la `Historia` | `dominio` |
| `motor` | Evaluar condiciones y efectos (`reglas`) y llevar el estado de la partida (`Sesion`) | `dominio` |
| `interfaz` | Mostrar escenas y traducir la entrada del lector a IDs de opción | `motor`, `dominio` |
| `__main__` | Unir las piezas: cargar, informar errores o iniciar la consola | Todos |

Regla de dependencias: `motor` no conoce `contenido` ni `interfaz`, y nada del código conoce los IDs de una historia concreta.

### Decisión DA1: monolito modular

- **Contexto:** proyecto pequeño, 12 horas, una pareja, ejecución local sin red.
- **Alternativas:** (a) arquitectura en capas con despliegue separado (por ejemplo, una API del motor y un cliente); (b) un solo script sin módulos; (c) un monolito modular.
- **Elección:** (c), un solo programa Python con paquetes separados por responsabilidad.
- **Consecuencias:** no hay infraestructura ni comunicación entre procesos que mantener. La separación en paquetes sigue aislando contenido, reglas e interfaz (RNF01, riesgo R1). Cambiar a una interfaz web solo exigiría reemplazar `interfaz`. Desventaja: los límites entre módulos dependen de la disciplina del equipo, no de una barrera técnica, y por eso se comprueban con `test_motor_sin_ids_de_historia`.

### Decisión DA2: validar todo el archivo antes de crear la partida

- **Contexto:** la escritora no sabe programar y la coordinadora no acepta cierres inesperados (N06, RNF02, RNF03).
- **Alternativas:** (a) detectar errores durante la partida, cuando el lector llega a ellos; (b) detenerse en el primer error encontrado; (c) validar el archivo completo antes de jugar e informar todos los errores juntos.
- **Elección:** (c). `contenido/validador.py` devuelve una lista con todos los problemas; `cargar_historia` lanza `ErrorContenido` con esa lista y `__main__` la muestra sin crear la `Sesion`.
- **Consecuencias:** el motor puede suponer que la historia es válida y queda más simple; la escritora corrige varios errores en una sola pasada; ningún lector ve un archivo roto (CA03). Desventaja: un error de sintaxis JSON solo se informa uno a la vez, porque el lector de JSON se detiene en el primero.

### (Opcional) Decisión DA3: deshacer con una instantánea de un nivel

- **Contexto:** solicitud de cambio de la hora 6 (RF20).
- **Alternativas:** (a) patrón Command con operación inversa por efecto; (b) pila de estados; (c) guardar una sola instantánea (escena y copia de variables) antes de cada elección válida.
- **Elección:** (c), porque se exige un solo nivel y no se exige rehacer.
- **Consecuencias:** el cambio quedó en `Sesion` y en la consola, sin tocar reglas, contenido ni formato. Si en el futuro se pidieran varios niveles, bastaría cambiar la instantánea por una pila.

### Separación entre contenido, reglas e interfaz demostrada

La segunda historia (`historias/historia2.json`, "El faro sin luz", 4 escenas, una condición y un efecto, IDs distintos de E1 a E6) se carga y juega con el mismo motor sin modificar código: ver `evidencias/rnf01.txt` y `tests/test_integracion.py::test_i1_segunda_historia_funciona_sin_tocar_el_motor`.

---

## Unidad 7: implementación

### Decisión de diseño detallado: reglas puras y consola con entrada y salida inyectadas

`motor/reglas.py` contiene funciones puras (`esta_habilitada`, `aplicar_efectos`) que no guardan estado ni conocen la sesión: reciben una opción y las variables y devuelven un resultado. `Sesion` es la única clase con estado mutable y es la que decide cuándo guardar la instantánea para deshacer. La consola recibe las funciones `leer` y `escribir` como parámetros (por defecto `input` y `print`) y solo usa la interfaz pública de `Sesion` (`titulo`, `escena`, `opciones_habilitadas`, `elegir`, `deshacer`, `reiniciar`).

Consecuencias: las reglas se prueban sin construir una sesión; la consola se prueba con entradas simuladas (I1, RNF02) sin teclado; y cambiar la interfaz no obliga a tocar el motor. Durante la revisión se encontró que la consola leía el atributo privado `sesion._historia.titulo`; se agregó la propiedad `Sesion.titulo` para eliminar ese acoplamiento.

### Bibliotecas y licencias

| Biblioteca | Versión | Uso | Licencia |
|---|---|---|---|
| Python (biblioteca estándar: `json`, `dataclasses`, `pathlib`, `typing`, `subprocess`) | 3.14 | Motor, lectura de archivos y pruebas | PSF License |
| pytest | 9.1.1 | Pruebas automatizadas | MIT |
| pluggy | 1.6.0 | Dependencia de pytest | MIT |
| iniconfig | 2.3.0 | Dependencia de pytest | MIT |
| packaging | 26.0 | Dependencia de pytest | Apache-2.0 o BSD-2-Clause |
| Pygments | 2.19.2 | Dependencia de pytest (salida coloreada) | BSD-2-Clause |
| colorama | 0.4.6 | Dependencia de pytest en Windows | BSD-3-Clause |

El programa en ejecución solo usa la biblioteca estándar; las demás se usan únicamente para correr las pruebas.

---

## Declaración de aportes

Datos del historial de Git (`evidencias/git_historial.txt`): Luis Eduardo Mendoza hizo el commit inicial (`482aade`); Josh Ortega hizo los commits de la versión de la hora 6 y de la implementación, las pruebas y la guía (`6eb8b14` a `6e031d5`). Completen con el trabajo que no se refleja en commits (informe, tablero, revisión cruzada, video):

| Integrante | Aportes | Evidencia |
|---|---|---|
| Josh Robinson Ortega Castellón | [ ] | Commits `6eb8b14`, `ee4cf43`, `d63c602`, `647eaed`, `31c0e92`, `6e031d5`; [ ] |
| Luis Eduardo Mendoza Angulo | [ ] | Commit `482aade`; [ ] |
