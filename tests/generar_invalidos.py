"""Genera los archivos defectuosos de tests/datos/invalidos/ (una sola vez).
Cada archivo es una historia mínima válida con UN defecto."""
import copy
import json
from pathlib import Path

DESTINO = Path(__file__).parent / "datos" / "invalidos"

BASE = {
    "titulo": "Prueba",
    "inicio": "A",
    "variables": {"x": False},
    "escenas": [
        {"id": "A", "texto": "Escena A", "final": False,
         "opciones": [{"id": "o", "texto": "Ir", "destino": "B",
                       "condiciones": {}, "efectos": {}}]},
        {"id": "B", "texto": "Escena B", "final": True, "opciones": []},
    ],
}


def nueva():
    return copy.deepcopy(BASE)


def guardar(nombre, datos):
    DESTINO.mkdir(parents=True, exist_ok=True)
    texto = datos if isinstance(datos, str) else json.dumps(datos, indent=2, ensure_ascii=False)
    (DESTINO / f"{nombre}.json").write_text(texto, encoding="utf-8")


guardar("ilegible", "{ esto no es un JSON válido")
guardar("raiz_lista", [])

d = nueva(); del d["inicio"]
guardar("sin_inicio", d)

d = nueva(); d["inicio"] = "Z"
guardar("inicio_inexistente", d)

d = nueva(); d["escenas"].append(copy.deepcopy(d["escenas"][1]))
guardar("escena_duplicada", d)

d = nueva(); d["escenas"][0]["opciones"].append(copy.deepcopy(d["escenas"][0]["opciones"][0]))
guardar("opcion_duplicada", d)

d = nueva(); d["escenas"][0]["opciones"][0]["destino"] = "E99"
guardar("destino_inexistente", d)

d = nueva(); d["escenas"][0]["opciones"][0]["efectos"] = {"y": True}
guardar("variable_no_declarada", d)

d = nueva(); d["escenas"][0]["opciones"][0]["condiciones"] = {"x": "si"}
guardar("valor_no_booleano", d)

d = nueva(); d["escenas"][1]["opciones"] = copy.deepcopy(d["escenas"][0]["opciones"])
guardar("final_con_opciones", d)

d = nueva(); d["escenas"][0]["opciones"] = []
guardar("no_final_sin_opciones", d)

print("Archivos generados en", DESTINO)