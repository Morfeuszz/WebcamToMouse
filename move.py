import asyncio
import websockets
import json
import win32api, win32con , win32gui
from win32api import GetSystemMetrics


mouseCanvas = (300,200,250,260)
screenRatio = (GetSystemMetrics(0)/mouseCanvas[0],GetSystemMetrics(1)/mouseCanvas[1])
mousePosition = (0,0)
lastMousePosition = (0,0)
avarageX = []
avarageY = [] 

async def smooth(x,y):
    x = x - (450 - mouseCanvas[2])
    y = y - (320 - mouseCanvas[3])
    if len(avarageX) < 3:
        avarageX.append(x*screenRatio[0])
        avarageY.append(y*screenRatio[1])
    else:
        avarageX.pop(0)
        avarageY.pop(0)
        avarageX.append(x*screenRatio[0])
        avarageY.append(y*screenRatio[1])
    await moveMouse(int(sum(avarageX)/len(avarageX)),int(sum(avarageY)/len(avarageY)))

async def moveMouse(x,y):
    global lastMousePosition
    global mousePosition
    mousePosition = (x,y)
    if abs(lastMousePosition[0] - mousePosition[0]) > 2 or  abs(lastMousePosition[1] - mousePosition[1]) > 2:
        win32api.SetCursorPos((x,y))
        lastMousePosition = mousePosition[:]
        #print(x,y)

async def connect():
    uri = "ws://localhost:6788"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "who":
                await websocket.send('{"action" : "who", "im" : "move"}')
            if data["action"] == "move":
                print(data["x"],data["y"])
                await smooth(int(data["x"]),int(data["y"]))



asyncio.get_event_loop().run_until_complete(connect())