"""La fachada: el punto único por el que las sedes registran admisiones.

Es la pieza del patrón Strangler Fig. Las sedes siempre le hablan a la fachada; la fachada
decide, sede por sede, a cuál HIS va cada admisión. Cambiar esa decisión no requiere tocar
las sedes, y deshacerla toma un segundo.

Modos por sede:
  norte     todo va a HIS-NORTE (estado inicial)
  sombra    responde HIS-NORTE y, por detrás, la misma admisión se manda a HIS-CORE para
            comparar las dos respuestas. El usuario no ve a HIS-CORE.
  canario   un porcentaje de las admisiones lo atiende HIS-CORE; el resto, HIS-NORTE.
  core      todo va a HIS-CORE

  POST /admisiones                              lo que usan las sedes
  POST /ruta?sede=N1&modo=canario&porcentaje=20 cambia la ruta de una sede (sede=todas: todas)
  GET  /ruta                                    las rutas vigentes
  GET  /comparaciones                           resultado de las comparaciones en sombra
  POST /reiniciar                               todas las sedes a norte y contadores en cero
"""
import json
import random
import threading
import urllib.error
import urllib.request
from collections import Counter

from comun import env, entero, log, servir
from datos import SEDES

HIS = {"norte": env("HIS_NORTE_URL", "http://his-norte:8083"), "core": env("HIS_CORE_URL", "http://his-core:8084")}
MODOS = {"norte", "sombra", "canario", "core"}
CANDADO = threading.Lock()
RUTAS = {}
COMPARACIONES = {}


def reiniciar_estado():
    with CANDADO:
        RUTAS.clear()
        RUTAS.update({s: {"modo": "norte", "porcentaje": 0} for s in SEDES})
        COMPARACIONES.clear()
        COMPARACIONES.update({s: Counter() for s in SEDES})


def reenviar(destino, cuerpo):
    peticion = urllib.request.Request(
        f"{HIS[destino]}/admisiones", data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Cliente": "FACHADA"}, method="POST")
    try:
        with urllib.request.urlopen(peticion, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {"error": f"HTTP {e.code}"}
    except Exception as e:
        return 502, {"error": f"{destino} no respondió: {e.__class__.__name__}"}


def comparar_en_sombra(sede, cuerpo, codigo_norte, respuesta_norte):
    codigo_core, respuesta_core = reenviar("core", cuerpo)
    if codigo_core != 201:
        tipo = f"HIS-CORE respondió {codigo_core}"
        if codigo_core == 422:
            tipo = "procedimiento sin homologar"
        elif codigo_core == 404:
            tipo = "paciente no existe en HIS-CORE"
    elif codigo_norte == 201 and respuesta_core.get("tarifa") != respuesta_norte.get("tarifa"):
        tipo = "tarifa distinta"
    else:
        tipo = "igual"
    with CANDADO:
        COMPARACIONES[sede][tipo] += 1


def admision(h, cuerpo, query):
    sede = cuerpo.get("sede")
    if sede not in SEDES:
        return h.responder(400, {"error": f"Sede desconocida: {sede}"})
    with CANDADO:
        ruta = dict(RUTAS[sede])
    modo = ruta["modo"]
    if modo == "core" or (modo == "canario" and random.random() * 100 < ruta["porcentaje"]):
        destino = "core"
    else:
        destino = "norte"
    codigo, respuesta = reenviar(destino, cuerpo)
    if modo == "sombra":
        threading.Thread(target=comparar_en_sombra, args=(sede, cuerpo, codigo, respuesta), daemon=True).start()
    respuesta["atendido_por"] = "HIS-CORE" if destino == "core" else "HIS-NORTE"
    h.responder(codigo, respuesta)


def ruta(h, cuerpo, query):
    if "modo" in query:
        modo = query["modo"]
        if modo not in MODOS:
            return h.responder(400, {"error": f"Modo desconocido: {modo}. Use {sorted(MODOS)}"})
        sedes = list(SEDES) if query.get("sede") == "todas" else [query.get("sede")]
        if any(s not in SEDES for s in sedes):
            return h.responder(400, {"error": f"Sede desconocida: {query.get('sede')}"})
        porcentaje = max(0, min(100, entero(query.get("porcentaje"), 0)))
        with CANDADO:
            for s in sedes:
                RUTAS[s] = {"modo": modo, "porcentaje": porcentaje if modo == "canario" else 0}
                COMPARACIONES[s] = Counter()
        log("fachada", f"{', '.join(sedes)} -> {modo}" + (f" {porcentaje} %" if modo == "canario" else ""))
    with CANDADO:
        h.responder(200, RUTAS)


def comparaciones(h, cuerpo, query):
    with CANDADO:
        h.responder(200, {s: dict(c) for s, c in COMPARACIONES.items()})


def reiniciar(h, cuerpo, query):
    reiniciar_estado()
    h.responder(200, {"resultado": "todas las sedes a HIS-NORTE"})


if __name__ == "__main__":
    reiniciar_estado()
    servir("fachada", {
        ("POST", "/admisiones"): admision,
        ("GET", "/ruta"): ruta,
        ("POST", "/ruta"): ruta,
        ("GET", "/comparaciones"): comparaciones,
        ("POST", "/reiniciar"): reiniciar,
    }, entero(env("PUERTO", "8080"), 8080))
