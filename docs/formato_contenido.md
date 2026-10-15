# Cómo escribir una historia

Una historia es un archivo de texto con extensión `.json`. Ábrelo con el Bloc de notas o VS Code. Solo editas **textos** y **destinos**; nunca el programa.

## Estructura básica

​```json
{
  "titulo": "Nombre de la historia",
  "inicio": "E1",
  "variables": { "tiene_llave": false },
  "escenas": [
    {
      "id": "E1",
      "texto": "Lo que lee el lector.",
      "final": false,
      "opciones": [
        {
          "id": "tomar",
          "texto": "Tomar la llave",
          "destino": "E2",
          "condiciones": {},
          "efectos": { "tiene_llave": true }
        }
      ]
    },
    { "id": "E2", "texto": "Fin.", "final": true, "opciones": [] }
  ]
}
​```

## Qué significa cada parte

| Campo | Qué es |
|---|---|
| `titulo` | Nombre que se muestra al empezar. |
| `inicio` | `id` de la escena donde empieza la partida. |
| `variables` | Lo que la historia recuerda. Cada una vale `true` (verdadero) o `false` (falso) al empezar. |
| `id` de escena | Nombre único de la escena. Lo usan los `destino`. |
| `final` | `true` si la historia termina ahí; entonces `opciones` va vacía: `[]`. |
| `destino` | `id` de la escena a la que lleva la opción. Debe existir. |
| `condiciones` | La opción solo se muestra si **todas** se cumplen. Vacío `{}` = siempre se muestra. |
| `efectos` | Lo que cambia al elegir la opción. Vacío `{}` = no cambia nada. |

Ejemplo de condición: `"condiciones": { "tiene_llave": true }` muestra la opción solo si el lector tomó la llave.

## Reglas para no equivocarse

1. Escribe `true` o `false` **sin comillas**. `"si"`, `1` o `"true"` no valen.
2. Toda variable usada en `condiciones` o `efectos` debe estar declarada en `variables`.
3. Entre un elemento y el siguiente va una coma; **después del último no**.
4. Los textos van entre comillas dobles `"..."`.
5. Una escena final no tiene opciones. Una escena que no es final tiene al menos una.
6. No repitas `id` de escena. Dentro de una escena, no repitas `id` de opción.
7. Tras deshacer (tecla `d`), el lector puede retroceder solo una decisión.

## Cómo probar tu historia

1. Guarda el archivo en la carpeta `historias/`.
2. Abre la terminal en la carpeta del proyecto y ejecuta (cambia el nombre):
   `python -m transmision historias/mi_historia.json`
3. Si hay errores, el programa los lista antes de jugar. Cada mensaje dice **dónde** (escena y opción) y **qué** corregir. Ejemplo:
   `Escena 'E2', opción 'investigar': el destino 'E99' no existe.`
   Significa: en la escena E2, la opción `investigar` apunta a una escena inexistente. Corrige el `destino` o crea esa escena.
4. Puedes ver ejemplos de archivos con errores en `tests/datos/invalidos/`.

Controles al jugar: número = elegir, `d` = deshacer, `r` = reiniciar, `s` = salir.