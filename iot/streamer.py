from typing import Dict, Any, List

class TelemetryAggregator:
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}

    def record(self, device_id: str, temperature: float):
        if device_id not in self.metrics:
            self.metrics[device_id] = []
        self.metrics[device_id].append(temperature)

    def aggregate(self, device_id: str) -> Dict[str, Any]:
        vals = self.metrics.get(device_id, [])
        if not vals:
            return {"count": 0}
        return {
            "device_id": device_id,
            "readings_count": len(vals),
            "avg_temp": round(sum(vals) / len(vals), 2),
            "max_temp": max(vals),
            "min_temp": min(vals)
        }
