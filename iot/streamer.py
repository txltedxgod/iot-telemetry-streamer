from __future__ import annotations

import math
import threading
from collections import deque
from typing import Any


class TelemetryAggregator:
    """Thread-safe bounded rolling window aggregator for IoT sensor streams."""

    def __init__(self, max_readings_per_device: int = 1000) -> None:
        self._lock = threading.RLock()
        self._max_readings = max_readings_per_device
        self.metrics: dict[str, deque[float]] = {}

    def record(self, device_id: str, temperature: float) -> None:
        cleaned = device_id.strip()
        if not cleaned:
            raise ValueError("device_id must not be empty")
        if not math.isfinite(temperature):
            raise ValueError("temperature must be a finite number")

        with self._lock:
            if cleaned not in self.metrics:
                self.metrics[cleaned] = deque(maxlen=self._max_readings)
            self.metrics[cleaned].append(float(temperature))

    def aggregate(self, device_id: str) -> dict[str, Any]:
        cleaned = device_id.strip()
        with self._lock:
            vals = list(self.metrics.get(cleaned, ()))
        if not vals:
            return {"count": 0}
        return {
            "device_id": cleaned,
            "readings_count": len(vals),
            "avg_temp": round(sum(vals) / len(vals), 2),
            "max_temp": max(vals),
            "min_temp": min(vals),
        }
