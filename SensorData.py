import asyncio
import websockets
import serial
import json
import time

# --- Configuration ---
# Pi 5 UART setup. Ensure /dev/ttyAMA0 is enabled in raspi-config
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
            # 1. Listen for User Input (WASD/Gamepad) from UserInputs.js
            try:
                # wait_for prevents blocking the rest of the loop
                message = await asyncio.wait_for(websocket.recv(), timeout=0.01)
                data = json.loads(message)
                
                if "command" in data:
                    cmd = str(data["command"])
                    ser.write(cmd.encode()) 
                    # print(f"Sent Command to ESP32: {cmd}") # Debug
                #print(f"PI UART SEND -> ESP32: {cmd}") 
            except asyncio.TimeoutError:
                pass

            # 2. Send Heartbeat 'C' every 2 seconds
            # This resets the ESP32 failsafe timer
            if time.time() - last_heartbeat > 2:
                ser.write(b'C')
                last_heartbeat = time.time()

            # 3. REQUEST and Read Sensor Data
            # We send 'L' to trigger the ESP32's distance read logic
            ser.reset_input_buffer() # Clear old bytes to ensure sync
            ser.write(b'L')
            
            # Wait a tiny bit for the ESP32 to respond with 2 bytes
            await asyncio.sleep(0.01) 
            
            if ser.in_waiting >= 2:
                raw = ser.read(2)
                # Reassemble 2 bytes into a 16-bit integer
                distance = (raw[0] << 8) | raw[1]
                
                # Filter out overflow/garbage values (over 3 meters)
                if distance > 8192 or distance == 0:
                    # Keep last good distance or show out of range
                    pass 
                else:
                    await websocket.send(json.dumps({"sensor": f"{distance} mm"}))

            # Maintain a 20Hz loop for smooth responsiveness
            await asyncio.sleep(0.05)

        except websockets.exceptions.ConnectionClosed:
            print("Web client disconnected")
            break
        except Exception as e:
            print(f"Loop Error: {e}")
            break

async def main():
    # Binds to all network interfaces on port 8001
    async with websockets.serve(handle_websocket, "0.0.0.0", 8001):
        print("WebSocket Server started on port 8001")
        # Keeps the server running indefinitely
        await asyncio.Future() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping Server...")
        ser.close()