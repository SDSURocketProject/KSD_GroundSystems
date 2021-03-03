import asyncio
import websockets
import json
import math
import time
import threading
import collections
import random
import copy
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler

toHistorical = collections.deque()
toRealTime = collections.deque()

dataRecordLock = threading.Lock()
dataRecord = {
    "prop.fuel":[],
    "prop.thrusters":[],
    "comms.recd":[],
    "comms.sent":[],
    "pwr.temp":[],
    "pwr.c":[],
    "Generator.Voltage":[],
}

def recordData():
    while True:
        while toHistorical:
            datum = toHistorical.popleft()
            with dataRecordLock:
                dataRecord[datum['id']].append(datum)
        time.sleep(.05)

def getData(value, start, end):
    data = []
    # Only show up to 15 minutes worth of data
    if end - start > 899*1000:
        start = end - 899*1000

    with dataRecordLock:
        for datum in dataRecord[value]:
            if datum['timestamp'] > start and datum['timestamp'] < end:
                data.append(datum)
    
    return json.dumps(data)

class serverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        urlParams = urlparse(self.path)
        if urlParams[2].find('history') != 1:
            self.end_headers()
            self.wfile.write(b'Unrecognized request :(')
            return
        # Split the query part of the url into the key value pairs
        query = dict(x.split('=') for x in urlParams[4].split('&'))
        if "start" not in query:
            self.end_headers()
            self.wfile.write(b'Missing start in query :(')
            return
        if "end" not in query:
            self.end_headers()
            self.wfile.write(b'Missing end in query :(')
            return
        
        self.end_headers()
        data = getData(urlParams[2].split('/')[2], int(query['start']), int(query['end']))
        self.wfile.write(data.encode('utf-8'))
    
    def end_headers(self):
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header("Access-Control-Allow-Origin", "*")
        BaseHTTPRequestHandler.end_headers(self)

async def webSockServer(websocket, path):
    print("start of webSockServer")
    subs = []

    toRealTime.clear()
    while True:
        try:
            while True:
                receiveMessage = await asyncio.wait_for(websocket.recv(), 0.001)
                if receiveMessage != "":
                    receiveMessage = receiveMessage.split(' ')
                    if receiveMessage[0] == "subscribe":
                        subs.append(receiveMessage[1])
                    elif receiveMessage[0] == "unsubscribe":
                        subs.remove(receiveMessage[1])
                    else:
                        print(f"Unrecognized command received {receiveMessage[0]}")
        except asyncio.TimeoutError:
            #print("No commands received")
            pass
        except Exception as e:
            print(f"Error in getting commands from client - {e}")

        while toRealTime:
            newData = toRealTime.popleft()
            if newData['id'] in subs:
                await websocket.send(json.dumps(newData))

        time.sleep(1)

def dataProducer():
    print("Starting data producer")
    fuelDefault = 99
    fuel = fuelDefault
    thrustersDefault = "ON"
    recdDefault = 1
    sentDefault = 1
    tempDefault = 100
    currentDefault = 10
    voltageDefault = 28

    while True:
        time.sleep(1)

        datum = {}
        datum['timestamp'] = int(time.time()*1000)

        # Fuel can decrease at most by 2% per second
        fuel = random.uniform(fuel*.98, fuel)
        datum['value'] = fuel
        datum['id'] = "prop.fuel"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

        datum['value'] = thrustersDefault
        datum['id'] = "prop.thrusters"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

        datum['value'] = recdDefault
        datum['id'] = "comms.recd"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

        datum['value'] = sentDefault
        datum['id'] = "comms.sent"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))
        
        temp = random.uniform(tempDefault*.9, tempDefault*1.1)
        datum['value'] = temp
        datum['id'] = "pwr.temp"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

        current = random.uniform(currentDefault*.9, currentDefault*1.05)
        datum['value'] = current
        datum['id'] = "pwr.c"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

        voltage = random.uniform(voltageDefault*.95, voltageDefault*1.05)
        datum['value'] = voltage
        datum['id'] = "Generator.Voltage"
        toHistorical.append(copy.deepcopy(datum))
        toRealTime.append(copy.deepcopy(datum))

def main():
    global toHistorical
    global toRealTime
    global dataRecord

    httpPort = 8090
    webSocketPort = 8091

    server = HTTPServer(('localhost', httpPort), serverHandler)
    threading.Thread(target=server.serve_forever).start()
    threading.Thread(target=recordData).start()
    threading.Thread(target=dataProducer).start()

    websocketServer = websockets.serve(webSockServer, 'localhost', webSocketPort)
    print("Created websocket server")
    asyncio.get_event_loop().run_until_complete(websocketServer)
    asyncio.get_event_loop().run_forever()
    #asyncio.get_event_loop().close()

if __name__ == "__main__":
    main()
