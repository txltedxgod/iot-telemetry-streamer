from fastapi import FastAPI
from pydantic import BaseModel
from iot.streamer import TelemetryAggregator

app = FastAPI(title="IoT Telemetry Streamer", version="0.1.0")
agg = TelemetryAggregator()

class TelemetryReq(BaseModel):
    device_id: str
    temperature: float

@app.post("/api/v1/telemetry")
def record(req: TelemetryReq):
    agg.record(req.device_id, req.temperature)
    return agg.aggregate(req.device_id)
