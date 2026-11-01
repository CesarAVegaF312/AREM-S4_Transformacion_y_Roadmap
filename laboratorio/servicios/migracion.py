"""Herramienta del laboratorio de la consolidación por estrangulamiento.

  python migracion.py admisiones [--sede N1] [--peticiones 300] [--concurrencia 10]
  python migracion.py ruta --sede N1 --modo norte|sombra|canario|core [--porcentaje 20]
  python migracion.py migrar-datos --sede N1          (o --sede todas)
  python migracion.py homologar
  python migracion.py estado
  python migracion.py apagar-norte [--forzar]
  python migracion.py reiniciar

Cada corrida de 'admisiones' guarda su resumen en resultados/ como JSON, con las rutas
vigentes en ese momento.
"""
import argparse
import json
import os
import random
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

from datos import PROCEDIMIENTOS_NORTE, SEDES, pacientes

FACHADA = os.environ.get("FACHADA_URL", "http://fachada:8080")
HIS_NORTE = os.environ.get("HIS_NORTE_URL", "http://his-norte:8083")
HIS_CORE = os.environ.get("HIS_CORE_URL", "http://his-core:8084")
RESULTADOS = os.environ.get("RESULTADOS", "/resultados")


def llamar(metodo, url, cuerpo=None, cliente="MIGRACION", timeout=30):
    datos = json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None
    peticion = urllib.request.Request(url, data=datos, method=metodo,
                                      headers={"Content-Type": "application/json", "X-Cliente": cliente})
    try:
        with urllib.request.urlopen(peticion, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {}
    except Exception as e:
        return None, {"error": f"No responde ({e.__class__.__name__}). Si acaba de levantar el laboratorio, "
                               "esperen unos segundos y repitan."}


def percentil(valores, p):
    if len(valores) < 2:
        return valores[0] if valores else 0.0
    return statistics.quantiles(valores, n=100, method="inclusive")[p - 1]


def una_admision(sede):
    cuerpo = {"sede": sede, "paciente": random.choice(pacientes(sede)),
              "procedimiento": random.choice(sorted(PROCEDIMIENTOS_NORTE))}
    inicio = time.perf_counter()
    codigo, respuesta = llamar("POST", f"{FACHADA}/admisiones", cuerpo, cliente="SEDE")
    return sede, codigo, respuesta.get("atendido_por", "-"), time.perf_counter() - inicio


def admisiones(args):
    sedes = list(SEDES) if args.sede == "todas" else [args.sede]
    _, rutas = llamar("GET", f"{FACHADA}/ruta")
    print(f"{args.peticiones} admisiones desde {', '.join(sedes)}, {args.concurrencia} a la vez...\n")
    with ThreadPoolExecutor(max_workers=args.concurrencia) as hilos:
        resultados = list(hilos.map(lambda i: una_admision(sedes[i % len(sedes)]), range(args.peticiones)))

    por_sede = defaultdict(list)
    for sede, codigo, atendido, t in resultados:
        por_sede[sede].append((codigo, atendido, t))
    resumen = {"fecha": time.strftime("%Y-%m-%d %H:%M:%S"), "etiqueta": args.etiqueta,
               "rutas": rutas, "por_sede": {}}
    print(f"  {'Sede':<5} {'Ruta':<14} {'Admisiones':>10} {'Éxito':>8} {'p95':>8}  Atendidas por / errores")
    for sede in sedes:
        filas = por_sede[sede]
        exitos = sum(1 for c, _, _ in filas if c == 201)
        atendidas = Counter(a for c, a, _ in filas if c == 201)
        errores = Counter(str(c) for c, _, _ in filas if c != 201)
        ruta = rutas.get(sede, {})
        texto_ruta = ruta.get("modo", "?") + (f" {ruta.get('porcentaje')} %" if ruta.get("modo") == "canario" else "")
        p95 = round(percentil(sorted(t for _, _, t in filas), 95), 3)
        partes = [", ".join(f"{k} {v}" for k, v in atendidas.items())] if atendidas else []
        if errores:
            partes.append("errores " + ", ".join(f"{k}: {v}" for k, v in errores.items()))
        detalle = " · ".join(partes)
        print(f"  {sede:<5} {texto_ruta:<14} {len(filas):>10} {100 * exitos / len(filas):>7.1f}% {p95:>7}s  {detalle}")
        resumen["por_sede"][sede] = {"ruta": ruta, "admisiones": len(filas),
                                     "exito_pct": round(100 * exitos / len(filas), 1),
                                     "atendidas_por": dict(atendidas), "errores": dict(errores), "p95_s": p95}

    if any(r.get("modo") == "sombra" for r in rutas.values()):
        print("\n  Hay sedes en sombra: la comparación con HIS-CORE está en 'estado'.")
    os.makedirs(RESULTADOS, exist_ok=True)
    nombre = time.strftime("%Y%m%d-%H%M%S") + "-admisiones" + (f"-{args.etiqueta}" if args.etiqueta else "")
    with open(os.path.join(RESULTADOS, nombre + ".json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print(f"\n  Guardado en resultados/{nombre}.json")


def ruta(args):
    query = f"sede={args.sede}&modo={args.modo}" + (f"&porcentaje={args.porcentaje}" if args.modo == "canario" else "")
    codigo, rutas = llamar("POST", f"{FACHADA}/ruta?{query}")
    if codigo != 200:
        print(f"  No se cambió la ruta: {rutas.get('error')}")
        return
    print("  Rutas vigentes: " + " · ".join(
        f"{s} {r['modo']}" + (f" {r['porcentaje']} %" if r["modo"] == "canario" else "") for s, r in rutas.items()))


def migrar_datos(args):
    sedes = list(SEDES) if args.sede == "todas" else [args.sede]
    for sede in sedes:
        inicio = time.perf_counter()
        codigo, exportado = llamar("GET", f"{HIS_NORTE}/exportar?sede={sede}")
        if codigo != 200:
            print(f"  {sede}: no se pudo leer HIS-NORTE ({exportado.get('error', codigo)})")
            continue
        lista = exportado["pacientes"][sede]
        codigo, respuesta = llamar("POST", f"{HIS_CORE}/importar", {"sede": sede, "pacientes": lista})
        print(f"  {sede}: {respuesta.get('importados', 0)} pacientes migrados a HIS-CORE "
              f"en {time.perf_counter() - inicio:.1f} s")


def homologar(args):
    _, respuesta = llamar("POST", f"{HIS_CORE}/homologar")
    hechos = respuesta.get("homologados_ahora", [])
    print("  Códigos homologados ahora: " + (", ".join(hechos) if hechos else "ninguno; ya estaban todos"))


def estado(args):
    _, rutas = llamar("GET", f"{FACHADA}/ruta")
    _, comparaciones = llamar("GET", f"{FACHADA}/comparaciones")
    _, core = llamar("GET", f"{HIS_CORE}/estado")
    _, accesos = llamar("GET", f"{HIS_NORTE}/accesos?ventana=60")
    if "error" in rutas:
        print(f"  {rutas['error']}")
        return
    print(f"  {'Sede':<5} {'Ruta':<14} {'Pacientes en HIS-CORE':>22}   Comparación en sombra")
    for sede in SEDES:
        r = rutas[sede]
        texto_ruta = r["modo"] + (f" {r['porcentaje']} %" if r["modo"] == "canario" else "")
        c = comparaciones.get(sede, {})
        total = sum(c.values())
        if total:
            sombra = f"{total} comparadas, {100 * c.get('igual', 0) / total:.1f} % iguales"
            difs = ", ".join(f"{k}: {v}" for k, v in c.items() if k != "igual")
            sombra += f" · {difs}" if difs else ""
        else:
            sombra = "-"
        print(f"  {sede:<5} {texto_ruta:<14} {core.get('pacientes_por_sede', {}).get(sede, '?'):>22}   {sombra}")
    print(f"\n  Códigos de HIS-NORTE homologados en HIS-CORE: {core.get('codigos_homologados_pct', '?')} %"
          + (f" (faltan {', '.join(core['sin_homologar'])})" if core.get("sin_homologar") else ""))
    print("  Quién usó HIS-NORTE en el último minuto: "
          + (", ".join(f"{k} {v}" for k, v in accesos.get("atendidos", {}).items()) or "nadie"))
    if accesos.get("rechazados"):
        print("  Rechazados por HIS-NORTE apagado: " + ", ".join(f"{k} {v}" for k, v in accesos["rechazados"].items()))


def apagar_norte(args):
    _, rutas = llamar("GET", f"{FACHADA}/ruta")
    _, accesos = llamar("GET", f"{HIS_NORTE}/accesos?ventana=60")
    pendientes = [s for s, r in rutas.items() if r["modo"] != "core"]
    otros = {k: v for k, v in accesos.get("atendidos", {}).items() if k not in ("FACHADA", "MIGRACION")}
    print("  Verificación antes de apagar HIS-NORTE")
    print(f"  1. Todas las sedes van a HIS-CORE por la fachada: "
          f"{'sí' if not pendientes else 'no, faltan ' + ', '.join(pendientes)}")
    print(f"  2. Nadie más lo usa por fuera de la fachada: "
          f"{'sí' if not otros else 'no: ' + ', '.join(f'{k} (accesos directos en el último minuto: {v})' for k, v in otros.items())}")
    listo = not pendientes and not otros
    if args.forzar:
        llamar("POST", f"{HIS_NORTE}/admin?caido=1")
        print("\n  HIS-NORTE APAGADO" + ("." if listo else ", aunque la verificación no pasó. Miren 'estado' en un minuto."))
    elif listo:
        print("\n  Se puede apagar. Para hacerlo: apagar-norte --forzar")
    else:
        print("\n  Todavía no se puede apagar.")


def reiniciar(args):
    pasos = [("Rutas: todas las sedes a HIS-NORTE", llamar("POST", f"{FACHADA}/reiniciar")[0]),
             ("HIS-CORE sin pacientes de las sedes del norte", llamar("DELETE", f"{HIS_CORE}/datos")[0]),
             ("HIS-NORTE encendido y sin registro de accesos", llamar("POST", f"{HIS_NORTE}/admin?caido=0&reiniciar=1")[0])]
    for descripcion, codigo in pasos:
        print(f"  {descripcion:<48} {codigo}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Consolidación de las sedes del norte por estrangulamiento")
    sub = p.add_subparsers(dest="comando", required=True)
    sedes = list(SEDES) + ["todas"]
    a = sub.add_parser("admisiones", help="las sedes registran admisiones a través de la fachada")
    a.add_argument("--sede", choices=sedes, default="todas")
    a.add_argument("--peticiones", type=int, default=300)
    a.add_argument("--concurrencia", type=int, default=10)
    a.add_argument("--etiqueta", default="")
    a.set_defaults(funcion=admisiones)
    r = sub.add_parser("ruta", help="cambia a qué HIS va una sede")
    r.add_argument("--sede", choices=sedes, required=True)
    r.add_argument("--modo", choices=["norte", "sombra", "canario", "core"], required=True)
    r.add_argument("--porcentaje", type=int, default=10, help="solo para canario")
    r.set_defaults(funcion=ruta)
    m = sub.add_parser("migrar-datos", help="lleva los pacientes de una sede de HIS-NORTE a HIS-CORE")
    m.add_argument("--sede", choices=sedes, required=True)
    m.set_defaults(funcion=migrar_datos)
    sub.add_parser("homologar", help="completa la homologación de procedimientos").set_defaults(funcion=homologar)
    sub.add_parser("estado", help="rutas, datos migrados, comparación en sombra y accesos").set_defaults(funcion=estado)
    g = sub.add_parser("apagar-norte", help="verifica si HIS-NORTE se puede apagar")
    g.add_argument("--forzar", action="store_true", help="lo apaga aunque la verificación no pase")
    g.set_defaults(funcion=apagar_norte)
    sub.add_parser("reiniciar", help="vuelve al estado inicial").set_defaults(funcion=reiniciar)
    args = p.parse_args()
    args.funcion(args)
