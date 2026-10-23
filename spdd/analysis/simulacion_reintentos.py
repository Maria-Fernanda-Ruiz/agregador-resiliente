"""
simulacion_reintentos.py — Modelo de GET /v1/sensores con el diseño de reintentos.

No es código del agregador ni mide el servicio real: es una simulación de eventos
discretos que se usó para decidir la ronda 5 (D17, D18 y D19 del README). Modela:

- servicio_inestable.py: sorteo 429 → 503 → éxito, respuestas lentas que duermen
  antes de responder, y el bloqueo por IP tras un 429 (que la compuerta evita);
- el agregador: páginas en serie, 4 lecturas a la vez (D14), compuerta compartida de
  Retry-After, backoff exponencial con jitter completo (D12), timeout por intento y
  plazo por petición.

Supone que una respuesta normal tarda 20 ms y que la red no suma tiempo. La semilla
es fija, así que cada corrida da las mismas tablas que cita el análisis.

Uso (D16):
    docker run --rm -v "$PWD":/app:ro -w /app python:3.12-slim \\
      python spdd/analysis/simulacion_reintentos.py
"""

import heapq
import random
import statistics

RAPIDA = 0.02               # segundos de una respuesta normal
BASE, TOPE = 0.5, 8.0       # backoff de D12
PAGINAS = [5, 5, 5, 5, 3]   # 23 sensores, 5 por página
CONCURRENCIA = 4            # D14
CORRIDAS = 4000
SEMILLA = 1

SERVICIO = {
    "defecto": dict(tasa_429=.10, tasa_fallos=.30, tasa_lentitud=.20, latencia=4.0, retry_after=2),
    "enunciado": dict(tasa_429=.10, tasa_fallos=.40, tasa_lentitud=.20, latencia=5.0, retry_after=2),
}


def simular(servicio, timeouts, maximo, plazo, rng):
    """Una petición a GET /v1/sensores. Devuelve qué se obtuvo y cuánto tardó."""
    compuerta = 0.0
    intentos = 0
    limite = plazo or float("inf")

    def intento(t, n):
        nonlocal compuerta, intentos
        intentos += 1
        timeout = min(timeouts[min(n, len(timeouts) - 1)], limite - t)
        sorteo = rng.random()
        if sorteo < servicio["tasa_429"]:
            compuerta = max(compuerta, t + RAPIDA + servicio["retry_after"])
            return t + RAPIDA, False, True
        if sorteo < servicio["tasa_429"] + servicio["tasa_fallos"]:
            return t + RAPIDA, False, False
        lenta = rng.random() < servicio["tasa_lentitud"]
        duracion = servicio["latencia"] if lenta else RAPIDA
        if duracion >= timeout:  # el servicio duerme antes de mandar nada: se corta
            return t + timeout, False, False
        return t + duracion, True, False

    def espera(n, fue_429):
        azar = rng.uniform(0, min(TOPE, BASE * 2 ** n))
        return max(servicio["retry_after"], azar) if fue_429 else azar

    def paso(t, n):
        """Intento n listo para salir en t → (resultado, instante)."""
        if t < compuerta:
            if compuerta >= limite:
                return "fallo", t
            return "esperar", compuerta
        if t >= limite:
            return "fallo", t
        fin, ok, fue_429 = intento(t, n)
        if ok:
            return "ok", fin
        if n + 1 >= maximo:
            return "fallo", fin
        siguiente = fin + espera(n, fue_429)
        if siguiente >= limite:
            return "fallo", fin
        return "reintento", siguiente

    # Páginas una tras otra: sin el cursor de una no se puede pedir la siguiente.
    t, sensores, paginas_ok = 0.0, 0, 0
    for tam in PAGINAS:
        n = 0
        while True:
            resultado, t = paso(t, n)
            if resultado == "reintento":
                n += 1
            elif resultado != "esperar":
                break
        if resultado != "ok":
            break
        paginas_ok += 1
        sensores += tam

    # Lecturas, varias a la vez, con la misma compuerta.
    pendientes = list(range(sensores))
    cola = [(t, w, pendientes.pop(), 0) for w in range(min(CONCURRENCIA, sensores))]
    heapq.heapify(cola)
    lecturas_ok, fin = 0, t
    while cola:
        t_w, w, sensor, n = heapq.heappop(cola)
        resultado, t_r = paso(t_w, n)
        if resultado == "esperar":
            heapq.heappush(cola, (t_r, w, sensor, n))
        elif resultado == "reintento":
            heapq.heappush(cola, (t_r, w, sensor, n + 1))
        else:
            lecturas_ok += resultado == "ok"
            fin = max(fin, t_r)
            if pendientes:
                heapq.heappush(cola, (t_r, w, pendientes.pop(), 0))

    return {
        "duracion": fin,
        "completa": paginas_ok == len(PAGINAS) and lecturas_ok == sum(PAGINAS),
        "lista_completa": paginas_ok == len(PAGINAS),
        "sin_datos": lecturas_ok == 0,  # D21: ni sensores ni lecturas → 502/504
        "intentos": intentos,
    }


def fila(etiqueta, servicio, timeouts, maximo, plazo):
    rng = random.Random(SEMILLA)
    rs = [simular(SERVICIO[servicio], timeouts, maximo, plazo, rng) for _ in range(CORRIDAS)]
    d = sorted(r["duracion"] for r in rs)
    pct = lambda clave: f"{100 * sum(r[clave] for r in rs) / CORRIDAS:.1f} %".replace(".", ",")
    return (f"| {etiqueta} | {servicio} | {pct('completa')} | {pct('lista_completa')} "
            f"| {pct('sin_datos')} | {d[len(d) // 2]:.0f} s | {d[int(len(d) * .95)]:.0f} s "
            f"| {d[-1]:.0f} s | {statistics.mean(r['intentos'] for r in rs):.0f} |")


def tabla(titulo, columna, casos):
    print(f"\n{titulo}\n")
    print(f"| {columna} | Servicio | Completa | Lista completa | Sin datos | Mediana | p95 | Máx. | Intentos |")
    print("|---|---|---|---|---|---|---|---|---|")
    for etiqueta, timeouts, maximo, plazo in casos:
        for servicio in SERVICIO:
            print(fila(etiqueta, servicio, timeouts, maximo, plazo))


if __name__ == "__main__":
    tabla("Tabla 1 · P08: intentos por llamada (timeouts 3 → 6 → 8 s, sin plazo)",
          "Intentos", [(str(n), (3, 6, 8), n, None) for n in (3, 4, 5, 6)])
    tabla("Tabla 2 · P08: plazo por petición (6 intentos, timeouts 3 → 6 → 8 s)",
          "Plazo", [("sin plazo", (3, 6, 8), 6, None), ("30 s", (3, 6, 8), 6, 30.0),
                    ("45 s", (3, 6, 8), 6, 45.0)])
    tabla("Tabla 3 · D13: timeouts por intento (6 intentos, plazo 45 s)",
          "Timeouts", [("3 → 5 → 8 s", (3, 5, 8), 6, 45.0), ("3 → 6 → 8 s", (3, 6, 8), 6, 45.0),
                       ("6 → 8 → 8 s", (6, 8, 8), 6, 45.0)])
