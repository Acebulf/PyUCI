"""
This is the base class for io with Chess Engines.

2014-08-07 -- Version 0.2 with non-blocking IO supporting non-unix machines.
2014-07-29 -- Patrick Poitras (acebulf at gmail dot com)

View LICENSE file in the github repo for license.
"""

import subprocess
from threading import Thread
from Queue import Queue,Empty

class Engine:
    def __init__(self, _filepath, **kwargs):
        self.score = 0 # Score in centipawns
        self.filepath = _filepath
        self.engineInst = subprocess.Popen(self.filepath,
                                           universal_newlines=True,
                                           stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
        self.queue = Queue()
        self.stdout_thread = Thread(target = self.enqueue)
        self.stdout_thread.daemon = True
        self.stdout_thread.start()

    def enqueue(self):
        while True:
            line = self.engineInst.stdout.readline()
            self.queue.put(line)

    def write(self, message):
        self.engineInst.stdin.write(message)

    def read(self):
        try:
            return self.queue.get_nowait()
        except Empty:
            return None

    def readAll(self):
        while True:
            message = self.read()
            if message is None:
                break
            else:
                if "score cp" in message:
                    try:
                        ind = message.split('score cp ')[1]
                        self.score = int(ind[0:ind.index(' ')])
                        #print message
                    except IndexError:
                        pass
                yield message

    def close(self):
        self.engineInst.terminate()
