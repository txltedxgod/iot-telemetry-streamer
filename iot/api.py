from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from iot.streamer import TelemetryAggregator

app = FastAPI(title="IoT Telemetry Streamer", version="0.1.0")
agg = TelemetryAggregator()


class TelemetryReq(BaseModel):
    device_id: str = Field(..., min_length=1)
    temperature: float


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/telemetry")
def record(req: TelemetryReq) -> dict:
    try:
        agg.record(req.device_id, req.temperature)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return agg.aggregate(req.device_id)


@app.get("/api/v1/telemetry/{device_id}")
def get_device_stats(device_id: str) -> dict:
    summary = agg.aggregate(device_id)
    if summary.get("count") == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device telemetry not found",
        )
    return summary
