
import websockets
import asyncio
import ssl

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri

    async def connect(self):
        ssl_context = ssl._create_unverified_context() 

        async with websockets.connect(self.uri, ssl=ssl_context) as websocket:
            await self.send_message(websocket, "Hello, WebSocket!")
            await self.receive_message(websocket)

    async def send_message(self, websocket, message):
        await websocket.send(message)
        print(f"Sent: {message}")

    async def receive_message(self, websocket):
        response = await websocket.recv()
        print(f"Received: {response}")
    async def close_connection(self, websocket):
        await websocket.close()

client = WebSocketClient("wss://ws.postman-echo.com/raw")
asyncio.run(client.connect())