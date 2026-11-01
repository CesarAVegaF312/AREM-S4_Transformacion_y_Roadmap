"""El consumidor que nadie ve desde la fachada: FACT-SALUD leyendo HIS-NORTE.

El dossier (sección 7) documenta la integración HIS-NORTE → FACT-SALUD como una carga manual
asistida. Para el laboratorio se reduce a esto: cada cierto tiempo, alguien de facturación
saca los datos de HIS-NORTE directamente, sin pasar por la fachada.
"""
import time
import urllib.request

from comun import env, log

HIS_NORTE_URL = env("HIS_NORTE_URL", "http://his-norte:8083")
INTERVALO_S = float(env("INTERVALO_S", "15"))

if __name__ == "__main__":
    log("fact-salud", f"extrae datos de HIS-NORTE cada {INTERVALO_S:g} s")
    while True:
        peticion = urllib.request.Request(f"{HIS_NORTE_URL}/exportar?sede=todas",
                                          headers={"X-Cliente": "FACT-SALUD"})
        try:
            with urllib.request.urlopen(peticion, timeout=10) as r:
                r.read()
        except Exception as e:
            log("fact-salud", f"la extracción falló ({e.__class__.__name__}): hoy no se factura a tiempo")
        time.sleep(INTERVALO_S)
