async function startAudio() {
    const audioWs = new WebSocket("ws://192.168.50.6:8003");
    audioWs.binaryType = 'arraybuffer';

    const audioContext = new AudioContext({ sampleRate: 44100 });
    
    // 1. Load the worklet file
    await audioContext.audioWorklet.addModule('pcm-processor.js');
    
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = audioContext.createMediaStreamSource(stream);
    
    // 2. Create the node
    const pcmWorkerNode = new AudioWorkletNode(audioContext, 'pcm-processor');

    // 3. Receive PCM data from worklet and send to Pi
    pcmWorkerNode.port.onmessage = (event) => {
        if (audioWs.readyState === WebSocket.OPEN) {
            audioWs.send(event.data);
        }
    };

    source.connect(pcmWorkerNode);
    pcmWorkerNode.connect(audioContext.destination);
    
    console.log("Streaming active via AudioWorklet");
}

// Browser requires a user gesture (click) to start audio
window.addEventListener('click', () => {
    startAudio();
    console.log("Audio Context Started");
}, { once: true });
