import asyncio
import websockets
import json
import win32api, win32con , win32gui
from win32api import GetSystemMetrics
async def hello():
    uri = "ws://localhost:6788"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())