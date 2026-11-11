import pytest
from fastapi.testclient import TestClient

from iot.api import app
from iot.streamer import TelemetryAggregator

client = TestClient(app)


def test_iot() -> None:
    a = TelemetryAggregator()
    a.record("sensor-1", 20.0)
    a.record("sensor-1", 24.0)
    res = a.aggregate("sensor-1")
    assert res["avg_temp"] == 22.0
    assert res["min_temp"] == 20.0
    assert res["max_temp"] == 24.0


def test_iot_validation_and_bounded_window() -> None:
    a = TelemetryAggregator(max_readings_per_device=2)
    a.record("dev-1", 10.0)
    a.record("dev-1", 20.0)
    a.record("dev-1", 30.0)
    res = a.aggregate("dev-1")
    assert res["readings_count"] == 2
    assert res["avg_temp"] == 25.0

    with pytest.raises(ValueError, match="empty"):
        a.record("   ", 21.0)
    with pytest.raises(ValueError, match="finite"):
        a.record("dev-1", float("nan"))


def test_iot_api_endpoints() -> None:
    assert client.get("/health").json() == {"status": "ok"}

    missing = client.get("/api/v1/telemetry/unknown-device")
    assert missing.status_code == 404

    post_resp = client.post(
        "/api/v1/telemetry",
        json={"device_id": "edge-gw-9", "temperature": 31.5},
    )
    assert post_resp.status_code == 200
    assert post_resp.json()["avg_temp"] == 31.5

    get_resp = client.get("/api/v1/telemetry/edge-gw-9")
    assert get_resp.status_code == 200
    assert get_resp.json()["readings_count"] == 1

    blank_resp = client.post(
        "/api/v1/telemetry",
        json={"device_id": "   ", "temperature": 20.0},
    )
    assert blank_resp.status_code == 400
