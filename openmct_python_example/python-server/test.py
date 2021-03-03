import queue, threading, time

hist = queue.Queue()
real = queue.Queue()

def putData():
    histStart = 0
    realStart = 0
    while True:
        time.sleep(1)
        hist.put(histStart)
        real.put(realStart)

        histStart = histStart - 1
        realStart = realStart + 1

def getHist():
    while True:
        while not hist.empty():
            print(hist.get())

def getReal():
    while True:
        while not real.empty():
            print(real.get())

if __name__ == "__main__":
    threading.Thread(target=putData).start()
    threading.Thread(target=getHist).start()
    threading.Thread(target=getReal).start()
    while True:
        pass