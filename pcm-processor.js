class PCMProcessor extends AudioWorkletProcessor {
  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (input.length > 0) {
      const floatData = input[0]; // Channel 0
      const pcmData = new Int16Array(floatData.length);
      
      for (let i = 0; i < floatData.length; i++) {
        let s = Math.max(-1, Math.min(1, floatData[i]));
        pcmData[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
      }
      
      // Send the Int16 buffer back to the main thread
      this.port.postMessage(pcmData.buffer, [pcmData.buffer]);
    }
    return true;
  }
}

registerProcessor('pcm-processor', PCMProcessor);
