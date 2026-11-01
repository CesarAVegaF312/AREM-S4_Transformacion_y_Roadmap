"""Simulador de HIS-CORE, el sistema al que se consolidan las seis sedes.

Solo conoce a los pacientes de una sede cuando sus datos se migran, y solo entiende los
procedimientos que tienen código homologado.

  POST /importar     {"sede": "N1", "pacientes": [...]}     carga los pacientes de una sede
  POST /admisiones   {"sede": "N1", "paciente": "N1-0001", "procedimiento": "PN-03"}
  POST /homologar    completa la homologación de los códigos que faltan
  GET  /estado       pacientes por sede y códigos sin homologar
  DELETE /datos      vuelve al estado inicial
"""
import random
import threading
import time

from comun import entero, env, log, servir
from datos import HOMOLOGACION, PROCEDIMIENTOS_NORTE, SEDES, TARIFAS_CORE

LATENCIA_MS = entero(env("LATENCIA_MS", "60"), 60)
CANDADO = threading.Lock()
PACIENTES = {}
HOMOLOGADOS = {}
TARIFAS = {}


def estado_inicial():
    with CANDADO:
        PACIENTES.clear()
        PACIENTES.update({sede: set() for sede in SEDES})
        HOMOLOGADOS.clear()
        HOMOLOGADOS.update(HOMOLOGACION)
        TARIFAS.clear()
        TARIFAS.update(TARIFAS_CORE)


def importar(h, cuerpo, query):
    sede, lista = cuerpo.get("sede"), cuerpo.get("pacientes") or []
    if sede not in SEDES:
        return h.responder(400, {"error": f"Sede desconocida: {sede}"})
    time.sleep(len(lista) * 0.005)      # la migración no es instantánea
    with CANDADO:
        PACIENTES[sede].update(lista)
    log("his-core", f"{len(lista)} pacientes de {sede} importados")
    h.responder(201, {"sede": sede, "importados": len(lista)})


def admision(h, cuerpo, query):
    time.sleep(max(0, random.gauss(LATENCIA_MS, LATENCIA_MS * 0.15)) / 1000)
    sede, paciente, codigo = cuerpo.get("sede"), cuerpo.get("paciente"), cuerpo.get("procedimiento")
    with CANDADO:
        existe = paciente in PACIENTES.get(sede, ())
        codigo_core = HOMOLOGADOS.get(codigo)
        tarifa = TARIFAS.get(codigo_core)
    if not existe:
        return h.responder(404, {"error": f"El paciente {paciente} no existe en HIS-CORE"})
    if codigo_core is None:
        return h.responder(422, {"error": f"Procedimiento sin homologar: {codigo}"})
    h.responder(201, {"sistema": "HIS-CORE", "sede": sede, "paciente": paciente,
                      "procedimiento": codigo_core, "procedimiento_origen": codigo, "tarifa": tarifa})


def homologar(h, cuerpo, query):
    with CANDADO:
        faltantes = sorted(set(PROCEDIMIENTOS_NORTE) - set(HOMOLOGADOS))
        for i, codigo in enumerate(faltantes, start=1):
            HOMOLOGADOS[codigo] = f"PC-{900 + i}"
            TARIFAS[f"PC-{900 + i}"] = PROCEDIMIENTOS_NORTE[codigo]
    log("his-core", f"homologados: {faltantes}")
    h.responder(200, {"homologados_ahora": faltantes})


def estado(h, cuerpo, query):
    with CANDADO:
        h.responder(200, {
            "pacientes_por_sede": {s: len(p) for s, p in PACIENTES.items()},
            "codigos_homologados_pct": round(100 * len(HOMOLOGADOS) / len(PROCEDIMIENTOS_NORTE), 1),
            "sin_homologar": sorted(set(PROCEDIMIENTOS_NORTE) - set(HOMOLOGADOS)),
        })


def borrar(h, cuerpo, query):
    estado_inicial()
    h.responder(200, {"resultado": "HIS-CORE en su estado inicial"})


if __name__ == "__main__":
    estado_inicial()
    servir("his-core", {
        ("POST", "/importar"): importar,
        ("POST", "/admisiones"): admision,
        ("POST", "/homologar"): homologar,
        ("GET", "/estado"): estado,
        ("DELETE", "/datos"): borrar,
    }, entero(env("PUERTO", "8084"), 8084))
