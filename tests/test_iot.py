from iot.streamer import TelemetryAggregator

def test_iot():
    a = TelemetryAggregator()
    a.record("sensor-1", 20.0)
    a.record("sensor-1", 24.0)
    res = a.aggregate("sensor-1")
    assert res["avg_temp"] == 22.0
