import asyncio
import websockets
import serial
import json

# Setup Serial - Update to /dev/ttyUSB0 if using USB
ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)

async def handle_websocket(websocket):
    print("Web client connected to overlay")
    while True:
        try:
            # 1. Ask ESP32 for data
            ser.write(b"LSRSD\n")
            
            # 2. Wait for 2-byte response
            if ser.in_waiting >= 2:
                raw = ser.read(2)
                distance = (raw[0] << 8) | raw[1]
                
                # 3. Create JSON packet for your JS
                payload = json.dumps({"sensor": f"{distance} mm"})
                await websocket.send(payload)
            
            await asyncio.sleep(0.1) # 10Hz Refresh rate
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

start_server = websockets.serve(handle_websocket, "0.0.0.0", 8000)

print("WebSocket Server started on port 8000")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()