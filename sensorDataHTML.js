const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  document.getElementById("sensor-data").textContent = `Sensor: ${message.sensor}`;
};

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
};