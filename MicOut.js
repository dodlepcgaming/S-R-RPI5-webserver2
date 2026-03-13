const WebSocket = require('ws');
const { spawn } = require('child_process');

const wss = new WebSocket.Server({ port: 8003 });

const aplay = spawn('aplay', [
  '-D', 'plughw:CARD=sndrpigooglevoi,DEV=0',
  '-c', '1',
  '-r', '44100',
  '-f', 'S16_LE'
]);

aplay.stderr.on('data', (data) => {
  console.error(`ALSA/aplay Status: ${data}`);
});

wss.on('connection', (ws) => {
  console.log('Client connected to Rover Speaker');
  
  ws.on('message', (data) => {
    if (aplay.stdin.writable) {
      aplay.stdin.write(data);
    }
  });

  ws.on('close', () => console.log('Client disconnected'));
});

console.log('Rover Audio Out listening on port 8003');

