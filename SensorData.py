import asyncio
import websockets
import serial
import json
import time

# Pi 5 GPIO Serial Port
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)

async def handle_websocket(websocket):
    print("Web client connected")
    last_heartbeat = 0
    
    while True:
        try:
            # 1. Listen for User Input (WASD/Gamepad) from the browser
            try:
                # Use wait_for to prevent blocking the heartbeat/sensor loop
                message = await asyncio.wait_for(websocket.recv(), timeout=0.01)
                data = json.loads(message)
                if "command" in data:
                    ser.write(data["command"].encode()) # Sends '1', '2', etc.
            except asyncio.TimeoutError:
                pass

            # 2. Send Heartbeat 'C' every 2 seconds
            if time.time() - last_heartbeat > 2:
                ser.write(b'C')
                last_heartbeat = time.time()

            # 3. Request and Read Sensor Data
            if ser.in_waiting >= 2:
                raw = ser.read(2)
                # Reassemble as an unsigned 16-bit integer
                distance = (raw[0] << 8) | raw[1]
                
                # Filter out garbage values (anything over 3 meters is likely an error)
                if distance > 3000:
                    distance = 0
                    
                await websocket.send(json.dumps({"sensor": f"{distance} mm"}))

            await asyncio.sleep(0.05) # 20Hz refresh rate
        except websockets.exceptions.ConnectionClosed:
            break

async def main():
    # This starts the server on all local network interfaces at port 8000
    async with websockets.serve(handle_websocket, "0.0.0.0", 8001):
        print("WebSocket Server started on port 8001")
        await asyncio.Future()  # This keeps the script running forever

if __name__ == "__main__":
    asyncio.run(main())