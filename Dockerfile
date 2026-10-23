# Una sola imagen para el agregador, el servicio inestable y las pruebas (D28).
# La base va fijada por tag exacto y digest (D29): es la misma imagen byte a byte en
# cualquier máquina. Para actualizarla, cambiar las dos cosas a la vez.
FROM python:3.12.15-slim-trixie@sha256:a0f57064cbdcd6285fa45f51237ab0b35ea8ebaed06a1f5973e89e19dfb86704

# Sin buffer, para que los logs (la evidencia de los reintentos) salgan al instante (C2).
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore --disable-pip-version-check \
        -r requirements.txt

COPY pytest.ini servicio_inestable.py ./
COPY agregador/ agregador/
COPY pruebas/ pruebas/

RUN useradd --create-home --shell /usr/sbin/nologin agregador
USER agregador

EXPOSE 8000 9000

# Forma exec: uvicorn es el PID 1, recibe el SIGTERM y `docker stop` termina limpio (C4).
# Sin access log: la línea de cada petición la escribe el middleware de evidencia (D37).
CMD ["uvicorn", "agregador.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--no-access-log", "--timeout-graceful-shutdown", "5"]
