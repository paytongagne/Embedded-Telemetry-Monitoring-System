const readingsBody = document.querySelector("#readings-body");
const totalDevices = document.querySelector("#total-devices");
const activeAlerts = document.querySelector("#active-alerts");
const latestHealth = document.querySelector("#latest-health");

async function loadReadings() {
  try {
    const response = await fetch("/api/v1/telemetry/latest?limit=10");
    const readings = await response.json();
    renderReadings(readings);
  } catch (error) {
    readingsBody.innerHTML = `<tr><td colspan="6">API not connected yet. Start FastAPI to load live readings.</td></tr>`;
  }
}

function renderReadings(readings) {
  if (!readings.length) {
    readingsBody.innerHTML = `<tr><td colspan="6">No readings stored yet.</td></tr>`;
    return;
  }

  totalDevices.textContent = new Set(readings.map((reading) => reading.device_id)).size;
  activeAlerts.textContent = readings.filter((reading) => reading.status !== "NORMAL").length;
  latestHealth.textContent = readings[0].health_score ?? "--";

  readingsBody.innerHTML = readings.map((reading) => `
    <tr>
      <td>${reading.device_id}</td>
      <td>${reading.subsystem}</td>
      <td>${reading.status}</td>
      <td>${reading.health_score}</td>
      <td>${Number(reading.battery_percent).toFixed(1)}%</td>
      <td>${Number(reading.signal_dbm).toFixed(1)} dBm</td>
    </tr>
  `).join("");
}

loadReadings();
