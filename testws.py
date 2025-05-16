import asyncio
import websockets

async def listen():
    uri = "ws://192.168.1.4:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        while True:
            data = await websocket.recv()
            print(f"Received: {data}")

asyncio.run(listen())
