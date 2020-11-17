import win32api, win32con , win32gui
from win32api import GetSystemMetrics
import asyncio
import json
import logging
import websockets
import datetime




logging.basicConfig()
position = []
size = []
avarageX = []
avarageY = [] 
sizeTreshholdX = []
sizeTreshholdY = []
mousePosition = (0,0)
lastMousePosition = (0,0)
avarageX = []
avarageY = [] 
mouseCanvas = (300,200,250,260)
screenRatio = (GetSystemMetrics(0)/mouseCanvas[0],GetSystemMetrics(1)/mouseCanvas[1])
clicked = False

move = []
click = []
USERS = set()                               

    

def clickLeft(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def clickRight(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

async def register(websocket):
    await websocket.send('{"action" : "who"}')
    USERS.add(websocket)
    print(USERS)
    

async def unregister(websocket):
    USERS.remove(websocket)


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
async def click(sizeX,sizeY):
    global clicked
    print(sizeX/sizeY)
    if  sizeX/sizeY < 1.5 and clicked == False:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,win32gui.GetCursorInfo()[0],win32gui.GetCursorInfo()[1],0,0)
        print("clicked left")
        clicked = True
    elif sizeX/sizeY > 1.5 and clicked == True:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,win32gui.GetCursorInfo()[0],win32gui.GetCursorInfo()[1],0,0)
        print("uncliked")
        clicked = False
 


async def counter(websocket, path):
    
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            #print(message)
            if data["action"] == "who":
                if data["im"] == "click":
                    click.append(websocket)
                    print("clicking active")
                if data["im"] == "move":
                    move.append(websocket)
                    print("moving active")
            if data["action"] == "position":
                 
                 position = [int(x.split(".",1)[0]) for x in data["predictions"].split(",")]
                 #print(position[0],position[1])
                 if position[0] > 450 - mouseCanvas[2]  and position[0] < 450 - mouseCanvas[2] + mouseCanvas[0] and position[1] > 320 - mouseCanvas[3] and position[1] < 320 - mouseCanvas[3] + mouseCanvas[1]:    
                    await smooth(position[0],position[1])
                 if position[0] > 0  and position[0] < 170 - mouseCanvas[2] + mouseCanvas[0] and position[1] > 0 - mouseCanvas[3] and position[1] < 150:
                    await click(position[3],position[2])
    finally:
        await unregister(websocket)
        print("disconnected")

start_server = websockets.serve(counter, "localhost", 6788)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()