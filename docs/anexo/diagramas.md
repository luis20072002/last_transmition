# Índice de diagramas del anexo

Fuente editable en Lucidchart, carpeta "Parcial - La última transmisión". Las imágenes exportadas están en `docs/anexo/diagramas/`. Los nombres D1 a D6 son los que usa la matriz de trazabilidad (`docs/informe/cambio_hora6.md`).

| ID | Diagrama | Unidad | Imagen | Requisitos que modela |
|---|---|---|---|---|
| D1 | Contexto | 5 | `diagramas/D1_contexto.png` | RF01, RF13 a RF15; actores y alcance |
| D2 | Casos de uso | 5 | `diagramas/D2_casos_de_uso.png` | RF01 a RF15, RF20 (cada caso de uso indica sus RF) |
| D3 | Clases del dominio | 5 | `diagramas/D3_clases_dominio.png` | RF02, RF04 a RF08, RF14, RF20 |
| D4 | Secuencia: elegir una opción | 5 | `diagramas/D4_secuencia_elegir_opcion.png` | RF04 a RF08, RF20 |
| D5 | Estados de una sesión | 5 | `diagramas/D5_estados_sesion.png` | RF09 a RF12, RF15, RF20 |
| D6 | Componentes (monolito modular) | 6 | `diagramas/D6_componentes.png` | RNF01 a RNF03; separación entre contenido, motor e interfaz |

## Coherencia con el código entregado

- D3 usa los nombres reales de `src/transmision/dominio/modelos.py` y `motor/sesion.py`, incluido `_anterior`, `puede_deshacer` y `deshacer()` del cambio de la hora 6.
- D4 sigue el flujo de `interfaz/consola.py` → `Sesion.elegir` → `reglas.aplicar_efectos`, con el guardado de la instantánea antes de aplicar los efectos.
- D5 incluye las transiciones de deshacer desde Final y Bloqueada y la regla de un solo nivel.
- D6 refleja las dependencias reales entre paquetes: `motor` no importa `contenido` ni `interfaz`.

## Enlaces de Lucidchart

| ID | Enlace (requiere acceso a la cuenta o compartir el documento) |
|---|---|
| D1 | https://lucid.app/lucidchart/771a846a-aa4b-4f58-a560-752982470294/edit |
| D2 | https://lucid.app/lucidchart/317d87e7-d64f-4dc2-9996-15f0c7ae48a4/edit |
| D3 | https://lucid.app/lucidchart/b7d467d2-7619-4f23-b84f-43836b2a133d/edit |
| D4 | https://lucid.app/lucidchart/8a471297-6677-433a-8dda-cd7141153088/edit |
| D5 | https://lucid.app/lucidchart/a3dcd86a-f0d0-4d9c-aea4-b9be2f316d6b/edit |
| D6 | https://lucid.app/lucidchart/1564ca0f-fd6a-462a-b821-752449f739c4/edit |
