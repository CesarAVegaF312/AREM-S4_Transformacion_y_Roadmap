"""Datos de referencia del laboratorio, iguales en todos los servicios.

Las seis sedes adquiridas a Centro Médico del Norte, sus pacientes y los catálogos de
procedimientos de los dos HIS. Los pacientes y las tarifas son inventados; la situación es la
del dossier: modelos de datos distintos y codificación de procedimientos no homologada.
"""
import random

SEDES = {f"N{i}": f"Sede Norte {i}" for i in range(1, 7)}
PACIENTES_POR_SEDE = 200

# Catálogo de HIS-NORTE: código propio y tarifa en pesos.
_azar = random.Random(2024)
PROCEDIMIENTOS_NORTE = {f"PN-{i:02d}": _azar.randrange(40, 400) * 1000 for i in range(1, 21)}

# Homologación al catálogo de HIS-CORE. Dos códigos no tienen equivalente todavía.
SIN_HOMOLOGAR = {"PN-07", "PN-16"}
HOMOLOGACION = {codigo: f"PC-{100 + i}" for i, codigo in enumerate(sorted(PROCEDIMIENTOS_NORTE), start=1)
                if codigo not in SIN_HOMOLOGAR}

# Tarifas de HIS-CORE. Un procedimiento quedó con otra tarifa en el contrato de la red.
TARIFA_DISTINTA = "PN-05"
TARIFAS_CORE = {HOMOLOGACION[c]: (round(t * 1.08, -3) if c == TARIFA_DISTINTA else t)
                for c, t in PROCEDIMIENTOS_NORTE.items() if c in HOMOLOGACION}


def pacientes(sede):
    return [f"{sede}-{n:04d}" for n in range(1, PACIENTES_POR_SEDE + 1)]
