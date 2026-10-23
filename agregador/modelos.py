"""Modelos Pydantic de la API propia (Entities del canvas).

Son el contrato que muestra /docs (Parte B del enunciado). Los de cada ruta se agregan
con su tarea; aquí están los de la base común.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Salud(BaseModel):
    estado: Literal["ok"]


class CuerpoErrorDependencia(BaseModel):
    """Cuerpo de los 502 y 504 cuando falla una dependencia (D20)."""

    detalle: str = Field(examples=["El servicio inestable no respondió dentro del plazo de la petición"])
    dependencia: Literal["servicio_inestable", "open_meteo"]
    causa: str = Field(
        description="timeout, plazo, conexion, respuesta_invalida, o el código que respondió (503, 429, 500…)",
        examples=["plazo"],
    )
    intentos: int = Field(description="Intentos enviados antes de rendirse", examples=[6])


class MetricasDependencia(BaseModel):
    llamadas: int = Field(description="Llamadas lógicas: cada una puede llevar varios intentos")
    intentos: int
    reintentos: int = Field(description="Intentos de más sobre la primera de cada llamada")
    por_resultado: dict[str, int] = Field(
        description="Intentos por resultado: el código («200», «503», «429»…) o la causa (timeout, conexion, plazo)",
        examples=[{"200": 230, "429": 38, "503": 121, "timeout": 21}],
    )
    respuestas_502: int
    respuestas_504: int
    compuerta_cerrada_hasta: datetime | None = Field(
        default=None, description="Solo el servicio inestable: hasta cuándo frena la compuerta de Retry-After (D14)"
    )


class MetricasCache(BaseModel):
    aciertos: int
    fallos: int


class LatenciaRuta(BaseModel):
    peticiones: int = Field(description="Peticiones en la ventana (las últimas 100)")
    mediana: float = Field(description="Milisegundos")
    p95: float = Field(description="Milisegundos")


class Metricas(BaseModel):
    """Lo que lee el panel de resiliencia del dashboard (D35). Cuenta desde el arranque."""

    desde: datetime
    dependencias: dict[Literal["servicio_inestable", "open_meteo"], MetricasDependencia]
    cache: MetricasCache
    latencia_ms: dict[str, LatenciaRuta] = Field(description="Por plantilla de ruta, p. ej. /v1/alertas/{id}")
