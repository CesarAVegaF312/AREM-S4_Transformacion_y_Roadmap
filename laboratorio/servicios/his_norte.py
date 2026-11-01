"""Simulador de HIS-NORTE, el sistema asistencial de las seis sedes adquiridas.

Registra admisiones y entrega sus datos a quien los pida. Lleva la cuenta de quién lo usa
(cabecera X-Cliente): antes de apagar un sistema hay que saber quién depende de él.

  POST /admisiones            {"sede": "N1", "paciente": "N1-0001", "procedimiento": "PN-03"}
  GET  /exportar?sede=N1      pacientes de una sede (o sede=todas)
  GET  /accesos?ventana=60    quién lo usó en los últimos N segundos
  POST /admin?caido=1         apagado (1) o encendido (0)
"""
import random
import threading
import time
from collections import Counter

from comun import entero, env, log, servir
from datos import PROCEDIMIENTOS_NORTE, SEDES, pacientes

PACIENTES = {sede: set(pacientes(sede)) for sede in SEDES}
LATENCIA_MS = entero(env("LATENCIA_MS", "120"), 120)
ESTADO = {"caido": False}
ACCESOS = []                 # (momento, cliente, atendido)
CANDADO = threading.Lock()


def registrar_acceso(h, atendido):
    with CANDADO:
        ahora = time.time()
        ACCESOS.append((ahora, h.headers.get("X-Cliente", "desconocido"), atendido))
        while ACCESOS and ACCESOS[0][0] < ahora - 600:
            ACCESOS.pop(0)


def admision(h, cuerpo, query):
    if ESTADO["caido"]:
        registrar_acceso(h, False)
        return h.responder(503, {"error": "HIS-NORTE está apagado"})
    registrar_acceso(h, True)
    time.sleep(max(0, random.gauss(LATENCIA_MS, LATENCIA_MS * 0.15)) / 1000)
    sede, paciente, codigo = cuerpo.get("sede"), cuerpo.get("paciente"), cuerpo.get("procedimiento")
    if paciente not in PACIENTES.get(sede, ()):
        return h.responder(404, {"error": f"El paciente {paciente} no existe en HIS-NORTE"})
    if codigo not in PROCEDIMIENTOS_NORTE:
        return h.responder(422, {"error": f"Procedimiento desconocido: {codigo}"})
    h.responder(201, {"sistema": "HIS-NORTE", "sede": sede, "paciente": paciente,
                      "procedimiento": codigo, "tarifa": PROCEDIMIENTOS_NORTE[codigo]})


def exportar(h, cuerpo, query):
    if ESTADO["caido"]:
        registrar_acceso(h, False)
        return h.responder(503, {"error": "HIS-NORTE está apagado"})
    registrar_acceso(h, True)
    sedes = list(SEDES) if query.get("sede", "todas") == "todas" else [query["sede"]]
    h.responder(200, {"pacientes": {s: sorted(PACIENTES.get(s, ())) for s in sedes}})


def accesos(h, cuerpo, query):
    desde = time.time() - entero(query.get("ventana"), 60)
    with CANDADO:
        recientes = [(c, ok) for t, c, ok in ACCESOS if t >= desde]
    h.responder(200, {
        "ventana_s": entero(query.get("ventana"), 60),
        "atendidos": dict(Counter(c for c, ok in recientes if ok)),
        "rechazados": dict(Counter(c for c, ok in recientes if not ok)),
    })


def admin(h, cuerpo, query):
    if "caido" in query:
        ESTADO["caido"] = query["caido"] == "1"
        log("his-norte", "APAGADO" if ESTADO["caido"] else "encendido")
    if query.get("reiniciar") == "1":
        with CANDADO:
            ACCESOS.clear()
    h.responder(200, ESTADO)


if __name__ == "__main__":
    servir("his-norte", {
        ("POST", "/admisiones"): admision,
        ("GET", "/exportar"): exportar,
        ("GET", "/accesos"): accesos,
        ("GET", "/admin"): admin,
        ("POST", "/admin"): admin,
    }, entero(env("PUERTO", "8083"), 8083))
