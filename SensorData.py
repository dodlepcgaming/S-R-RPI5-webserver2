from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import serial_asyncio
import asyncio
import json

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        reader, _ = await serial_asyncio.open_serial_connection(url='/dev/ttyAMA0', baudrate=115200)
        
        while True:
            line = await reader.readline()
            data = line.decode().strip()
            await websocket.send_json({"sensor": data})
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        await websocket.close()