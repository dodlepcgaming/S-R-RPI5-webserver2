import asyncio
import websockets
from gpiozero import Servo
from gpiozero.pins.lgpio import LGPIOFactory
import json

pin_factory = LGPIOFactory()
Y_servo = Servo(13, pin_factory=pin_factory, min_pulse_width=1/1000, max_pulse_width=2/1000)
X_servo = Servo(19, pin_factory=pin_factory, min_pulse_width=1/1000, max_pulse_width=2/1000)

async def handle_websocket(websocket):
    print("Client connected to Pi 5 on port 8002")
    async for message in websocket:
        try:
            data = json.loads(message)
            cmd = str(data.get("command", "")).strip()
        except json.JSONDecodeError:
            cmd = str(message).strip()
        
        if cmd == '5':     # UP
            Y_servo.value = 1.0
        elif cmd == '6':   # DOWN
            Y_servo.value = -1.0
        elif cmd == '7':   # LEFT
            X_servo.value = 1.0
        elif cmd == '8':   # RIGHT
            X_servo.value = -1.0
        else:              # STOP
            Y_servo.value, X_servo.value = None, None
            
        print(f"Executing: {cmd}")

async def main():
    async with websockets.serve(handle_websocket, "0.0.0.0", 8002):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Y_servo.value = X_servo.value = None
