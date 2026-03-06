import asyncio
import websockets
import serial
import json
import time

try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)
    print("Serial port /dev/ttyAMA0 opened successfully.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

async def handle_websocket(websocket):
    print("Web client connected to Pi 5")
    last_heartbeat = 0
    
    while True:
        try:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.01)
                data = json.loads(message)
                
                if "command" in data:
                    raw_cmd = str(data["command"])
                    filtered_cmd = "".join([c for c in raw_cmd if c in '01234'])

                    if filtered_cmd:
                        ser.write(filtered_cmd.encode()) 
                #print(f"PI UART SEND -> ESP32: {cmd}") 
            except asyncio.TimeoutError:
                pass

            if time.time() - last_heartbeat > 2:
                ser.write(b'C')
                last_heartbeat = time.time()

            ser.reset_input_buffer()
            ser.write(b'L')
            
            await asyncio.sleep(0.01) 
            
            if ser.in_waiting >= 2:
                raw = ser.read(2)
                distance = (raw[0] << 8) | raw[1]
                
                if distance > 8192 or distance == 0:
                    pass 
                else:
                    await websocket.send(json.dumps({"sensor": f"{distance} mm"}))

            await asyncio.sleep(0.05)

        except websockets.exceptions.ConnectionClosed:
            print("Web client disconnected")
            break
        except Exception as e:
            print(f"Loop Error: {e}")
            break

async def main():
    async with websockets.serve(handle_websocket, "0.0.0.0", 8001):
        print("WebSocket Server started on port 8001")
        await asyncio.Future() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Server...")
        ser.close()