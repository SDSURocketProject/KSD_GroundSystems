import asyncio
import websockets
import urllib.request
import time

async def getRealTimeData(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("subscribe prop.fuel")
        await websocket.send("subscribe pwr.temp")
        await websocket.send("subscribe pwr.c")
        await websocket.send("subscribe pwr.v")
        while True:
            data = await websocket.recv()
            print(data)

async def getHistoricalData():
    data = urllib.request.urlopen(f'http://localhost:8090/history/pwr.c?start={int(time.time()*1000 - 900*1000)}&end={int(time.time()*1000)}').read()
    print(data.decode('utf-8'))
    



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        getHistoricalData())
