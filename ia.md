# Registro de uso de IA

**Herramienta:** Claude (Anthropic), chat web.
**Regla del equipo:** no se incorpora código que no entendamos ni hayamos probado. Cada uso indica finalidad y cómo se verificó.

| # | Fecha | Artefacto | Finalidad | Qué se aceptó / cambió | Verificación |
|---|---|---|---|---|---|
| 1 | 2026-10-15 | Unidad 1 (informe) | Borrador de problema, actores, alcance, riesgos, priorización y decisión de responsabilidad profesional | Se adaptó a nuestro caso (Python, monolito modular, `ia.md`) | [ ] Revisión conjunta de ambos integrantes |
| 2 | 2026-10-15 | Unidad 4 (RF y RNF) | Borrador de 15 RF, 3 RNF medibles, matriz de cobertura, supuestos | Se simplificó de 36 a 15 RF a pedido nuestro | [ ] Revisión cruzada entre integrantes contra N01 a N06 |
| 3 | 2026-10-15 | Unidad 2 (procesos) | Comparación Kanban incremental frente a Scrum; reglas del tablero | Se cambió cascada por Scrum como alternativa; arquitectura a monolito modular | [ ] Revisión conjunta |
| 4 | 2026-10-15 | Estructura de carpetas | Propuesta de árbol del repositorio y regla de dependencias | Se usó tal cual | [x] Carpetas creadas y paquetes importables |
| 5 | 2026-10-15 | `historias/historia2.json` | Segunda historia (4 escenas, 1 condición, 1 efecto, IDs distintos a E1 a E6) | Se usó tal cual | [ ] Cargarla con `cargar_historia` y recorrer sus dos finales |
| 6 | 2026-10-15 | `dominio/modelos.py`, `dominio/errores.py` | Dataclasses inmutables y excepciones propias | Se usó tal cual | [x] Importación sin errores (`print('ok')`). Se corrigió un error de nombre de carpeta propio |
| 7 | 2026-10-15 | `contenido/validador.py`, `contenido/cargador.py` | Validación de los 9 defectos de RF13 y mensajes de RF14 | Se usó el formato `Escena 'E2', opción 'investigar': ...` | [ ] Carga de la historia de referencia (6 escenas) y prueba con destino E99 |
| 8 | 2026-10-15 | `motor/reglas.py`, `motor/sesion.py` | Evaluación de condiciones, efectos, sesión y deshacer de un nivel (RF20) | Se usó tal cual | [ ] Script de comprobación del ejemplo de la solicitud de cambio |
| 9 | 2026-10-15 | `interfaz/consola.py`, `__main__.py` | Interfaz de consola con comandos `d`, `r`, `s` | Pendiente de revisar | [ ] Recorrer los tres finales y probar entradas inválidas |
| 10 | 2026-10-15 | `README.md`, `evidencias/`, `docs/informe/cambio_hora6.md`, `docs/informe/borrador_unidades.md`, prueba de bloqueo, propiedad `Sesion.titulo` | Revisión del repositorio contra el enunciado y el anexo de la hora 6; README, evidencias de RNF01 y RNF03, análisis de impacto, matriz de trazabilidad y borradores de las unidades 3, 6 y 7 (Claude Code) | [ ] Pendiente de revisar y ajustar los borradores | [x] Suite completa (74 pruebas) y comandos del README ejecutados en PowerShell y Bash |

## Pendiente de registrar
- Diagramas D1 a D6 hechos en Lucidchart con Claude Code (ver `docs/anexo/diagramas.md`); pendiente revisarlos contra el informe final.

## Cómo verificamos
- Ejecución local de cada módulo con scripts de comprobación.
- Pruebas automatizadas con pytest (resultados en `evidencias/pytest_ultima_ejecucion.txt`).
- Revisión cruzada entre integrantes antes de pasar una tarjeta a Hecho.