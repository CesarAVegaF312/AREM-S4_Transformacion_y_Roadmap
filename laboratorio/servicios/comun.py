"""Utilidades HTTP compartidas por los servicios del laboratorio.

Solo biblioteca estandar: el objetivo del laboratorio es la costura de
integracion, no un framework web.
"""
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


def log(servicio, mensaje):
    print(f"{time.strftime('%H:%M:%S')} [{servicio}] {mensaje}", flush=True)


class Manejador(BaseHTTPRequestHandler):
    """Despacha a self.rutas[(metodo, ruta)] -> funcion(manejador, cuerpo, query)."""

    rutas = {}
    protocol_version = "HTTP/1.1"

    def _atender(self, metodo):
        url = urlparse(self.path)
        query = {k: v[-1] for k, v in parse_qs(url.query).items()}
        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = {}
        if largo:
            try:
                cuerpo = json.loads(self.rfile.read(largo) or b"{}")
            except json.JSONDecodeError:
                return self.responder(400, {"error": "El cuerpo no es JSON valido"})
        funcion = self.rutas.get((metodo, url.path))
        if funcion is None:
            return self.responder(404, {"error": f"No existe {metodo} {url.path}"})
        try:
            funcion(self, cuerpo, query)
        except Exception as e:  # el laboratorio no debe tumbarse por una peticion
            self.responder(500, {"error": str(e)})

    def do_GET(self):
        self._atender("GET")

    def do_POST(self):
        self._atender("POST")

    def do_DELETE(self):
        self._atender("DELETE")

    def responder(self, estado, datos):
        cuerpo = json.dumps(datos, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, formato, *args):
        pass  # el ruido de cada peticion tapa lo que importa en los logs


def servir(nombre, rutas, puerto):
    clase = type("ManejadorDe" + nombre, (Manejador,), {"rutas": rutas})
    servidor = ThreadingHTTPServer(("0.0.0.0", puerto), clase)
    servidor.daemon_threads = True
    log(nombre, f"escuchando en el puerto {puerto}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


def entero(valor, defecto):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return defecto


def env(nombre, defecto):
    return os.environ.get(nombre, defecto)
