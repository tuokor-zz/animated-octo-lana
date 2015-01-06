from multiprocessing import Process, Manager
from multiprocessing.managers import SyncManager
import time
import signal

class DataSender:


    def __init__(self):
        self.phant = dict()
        self.running = True
        self._manager = SyncManager()
        self._manager.start(self._mgr_init)
        self._que = self._manager.Queue()
        self._process = Process(target=self.up, args=(self._que,))
        self._process.start()

    def _mgr_init(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        print("initialized manager")

    def up(self,que):
        
        def stop(val,val2):
            print "process SIGINT stopping"
            self.running = False

        signal.signal(signal.SIGINT, stop)
        print('datauploader started')
        while self.running or not que.empty():
            print("running:{0} que={1}".format(self.running, que.empty()))
            item = que.get(True)
            print("got item={0}".format(item))
            que.task_done()
            time.sleep(2)
        print("datauploader process terminating...")

    def send(self, data):
        self._que.put(data)

    def httpsend(self, data):
        postdata = urllib.urlencode(data)
        headers = {'Phant-Private-Key': phant['privateKey'] }
        req = urllib2.Request(phant['inputUrl'], postdata, headers)
        res = urllib2.urlopen(req)
        content = resp.read()
        print("response: {0}".format(content))
    
    def stop(self):
        print("shutting down sender")
        self.running = False
        self._que.join()
        self._process.terminate()

if __name__ == '__main__':
    sender = DataSender()
    val = 0
    try:
        while val < 30:
            val = val+1
            print("adding new item to que={0}".format(val))
            sender.send("item {0}".format(val))
            if val % 2 == 0:
                print("main thread will sleep now for 3 seconds")
                time.sleep(3)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        sender.stop()
