from fastapi import FastAPI, WebSocket
import serial_asyncio
import asyncio

app = FastAPI()

@app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accet()

        reader, _ = await serial_asyncio.open_serial_connection(url= '/dev/ttyAMA0', baudrate 115200)

        while True:
            line = await reader.readline()
            data = line.decode().strip()