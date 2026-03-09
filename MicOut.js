const WebSocket = require('ws');
const Speaker = require('speaker');

const wss = new WebSocket.Server({ port: 8080 });
const speaker = new Speaker({
  channels: 1,
  bitDepth: 16,
  sampleRate: 44100
});

wss.on('connection', (ws) => {
  console.log('Client connected');
  ws.on('message', (data) => {
    speaker.write(data);
  });
});

