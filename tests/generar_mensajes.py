"""Genera docs/mensajes_error.md con los mensajes reales de cada defecto."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from transmision.contenido.cargador import cargar_historia  # noqa: E402
from transmision.dominio.errores import ErrorContenido  # noqa: E402

lineas = ["# Catálogo de mensajes de error", "",
          "| Archivo defectuoso | Mensaje que ve la escritora | ¿Sabría qué corregir? (sí/no) |",
          "|---|---|---|"]
for archivo in sorted((RAIZ / "tests" / "datos" / "invalidos").glob("*.json")):
    try:
        cargar_historia(archivo)
        mensaje = "(sin error)"
    except ErrorContenido as e:
        mensaje = " / ".join(e.mensajes)
    lineas.append(f"| `{archivo.name}` | {mensaje} | |")

destino = RAIZ / "docs" / "mensajes_error.md"
destino.parent.mkdir(exist_ok=True)
destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
print("Generado", destino)