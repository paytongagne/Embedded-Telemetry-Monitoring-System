from telemetry_monitor.models.telemetry import ClassifiedTelemetry, TelemetryReading


def classify_reading(reading: TelemetryReading) -> ClassifiedTelemetry:
    score = 100
    alerts: list[str] = []

    def add_alert(message: str, penalty: int) -> None:
        nonlocal score
        alerts.append(message)
        score -= penalty

    if reading.temperature_c > 85:
        add_alert("temperature is above critical band", 35)
    elif reading.temperature_c > 70:
        add_alert("temperature is above warning band", 15)

    if reading.voltage_v < 3.1 or reading.voltage_v > 4.7:
        add_alert("voltage is outside critical band", 35)
    elif reading.voltage_v < 3.4 or reading.voltage_v > 4.4:
        add_alert("voltage is outside warning band", 15)

    if reading.battery_percent < 10:
        add_alert("battery is below critical band", 30)
    elif reading.battery_percent < 25:
        add_alert("battery is below warning band", 12)

    if reading.signal_dbm < -100:
        add_alert("signal strength is below critical band", 25)
    elif reading.signal_dbm < -85:
        add_alert("signal strength is below warning band", 10)

    if reading.memory_usage_percent > 92:
        add_alert("memory usage is above critical band", 20)
    elif reading.memory_usage_percent > 80:
        add_alert("memory usage is above warning band", 8)

    score = max(score, 0)
    status = "NORMAL"
    if score < 50:
        status = "CRITICAL"
    elif score < 80:
        status = "WARNING"

    return ClassifiedTelemetry(**reading.model_dump(), status=status, health_score=score, active_alerts=alerts)
