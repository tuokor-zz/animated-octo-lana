from multiprocessing import Process, Manager
from multiprocessing.managers import SyncManager
import time
import signal

def mgr_init():
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    print("initialized manager")

running = True
def up(que):
    def stop(val,val2):
        global running
        print("stop called {0}".format(running))
        running = False
        print("running={0}".format(running))

    signal.signal(signal.SIGINT, stop)
    print('datauploader started')
    while running or not que.empty():
        print("state:{0} que={1}".format(running, que.empty()))
        item = que.get(True)
        print("got item={0}".format(item))
        que.task_done()
        time.sleep(2)
    print("datauploader process terminating...")


if __name__ == '__main__':
    manager = SyncManager()
    manager.start(mgr_init)
    que = manager.Queue()
    p = Process(target=up, args=(que,))
    p.start()
    val = 0
    try:
        while True:
            val = val+1
            print("adding new item to que={0}".format(val))
            que.put("item {0}".format(val))
            if val % 2 == 0:
                print("main thread will sleep now for 3 seconds")
                time.sleep(3)
    except KeyboardInterrupt:
        print("shutting down waiting que")
        que.join()
        print("exiting process")
        p.terminate()

