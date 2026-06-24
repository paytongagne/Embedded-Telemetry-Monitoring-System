const API_BASE = "http://127.0.0.1:8000";

const elements = {
  status: document.querySelector("#connection-status"),
  totalDevices: document.querySelector("#total-devices"),
  warningDevices: document.querySelector("#warning-devices"),
  criticalDevices: document.querySelector("#critical-devices"),
  activeAlerts: document.querySelector("#active-alerts"),
  readingsStored: document.querySelector("#readings-stored"),
  devicesBody: document.querySelector("#devices-body"),
  readingsBody: document.querySelector("#readings-body"),
  alertsBody: document.querySelector("#alerts-body"),
};

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) throw new Error(`Request failed: ${path}`);
  return response.json();
}

async function loadDashboard() {
  try {
    const [summary, devices, readings, alerts] = await Promise.all([
      fetchJson("/api/v1/summary"),
      fetchJson("/api/v1/devices"),
      fetchJson("/api/v1/telemetry/latest?limit=12"),
      fetchJson("/api/v1/alerts?limit=12"),
    ]);

    renderSummary(summary);
    renderDevices(devices);
    renderReadings(readings);
    renderAlerts(alerts);
    elements.status.textContent = "Connected to local telemetry API";
    elements.status.classList.add("ok");
  } catch (error) {
    elements.status.textContent = "API not connected. Start FastAPI, then refresh this dashboard.";
    elements.status.classList.add("error");
  }
}

function renderSummary(summary) {
  elements.totalDevices.textContent = summary.total_devices ?? "--";
  elements.warningDevices.textContent = summary.warning_devices ?? "--";
  elements.criticalDevices.textContent = summary.critical_devices ?? "--";
  elements.activeAlerts.textContent = summary.active_alerts ?? "--";
  elements.readingsStored.textContent = summary.readings_stored ?? "--";
}

function renderDevices(devices) {
  if (!devices.length) {
    elements.devicesBody.innerHTML = `<tr><td colspan="5">No devices stored yet.</td></tr>`;
    return;
  }
  elements.devicesBody.innerHTML = devices.map((device) => `
    <tr>
      <td>${device.device_id}</td>
      <td><span class="badge ${statusClass(device.status)}">${device.status}</span></td>
      <td>${device.latest_health_score ?? "--"}</td>
      <td>${device.active_alerts}</td>
      <td>${formatDate(device.last_seen_at)}</td>
    </tr>
  `).join("");
}

function renderReadings(readings) {
  if (!readings.length) {
    elements.readingsBody.innerHTML = `<tr><td colspan="6">No readings stored yet.</td></tr>`;
    return;
  }
  elements.readingsBody.innerHTML = readings.map((reading) => `
    <tr>
      <td>${reading.device_id}</td>
      <td>${reading.subsystem}</td>
      <td><span class="badge ${statusClass(reading.status)}">${reading.status}</span></td>
      <td>${reading.health_score}</td>
      <td>${Number(reading.battery_percent).toFixed(1)}%</td>
      <td>${Number(reading.signal_dbm).toFixed(1)} dBm</td>
    </tr>
  `).join("");
}

function renderAlerts(alerts) {
  if (!alerts.length) {
    elements.alertsBody.innerHTML = `<tr><td colspan="5">No active alerts.</td></tr>`;
    return;
  }
  elements.alertsBody.innerHTML = alerts.map((alert) => `
    <tr>
      <td><span class="badge ${statusClass(alert.severity)}">${alert.severity}</span></td>
      <td>${alert.device_id}</td>
      <td>${alert.metric}</td>
      <td>${alert.message}</td>
      <td>${formatDate(alert.created_at)}</td>
    </tr>
  `).join("");
}

function statusClass(status) {
  return String(status || "").toLowerCase();
}

function formatDate(value) {
  if (!value) return "--";
  return new Date(value).toLocaleString();
}

loadDashboard();
setInterval(loadDashboard, 15000);
