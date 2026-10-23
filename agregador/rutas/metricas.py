"""GET /v1/metricas: los contadores del panel de resiliencia (D35)."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Request

from agregador.modelos import Metricas

router = APIRouter(prefix="/v1", tags=["métricas"])


@router.get("/metricas", summary="Contadores de reintentos, caché y latencia desde el arranque")
async def obtener_metricas(request: Request) -> Metricas:
    estado = request.app.state
    falta = estado.compuerta.falta()
    cerrada_hasta = datetime.now(timezone.utc) + timedelta(seconds=falta) if falta > 0 else None
    return Metricas.model_validate(estado.metricas.instantanea(cerrada_hasta))
