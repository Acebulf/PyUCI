"""
This is the base class for io with Chess Engines.

2014-07-29 -- Patrick Poitras (acebulf at gmail dot com)
View LICENSE file in the github repo for license.
"""

import subprocess
from threading import Thread
from Queue import Queue, Empty
import fcntl #Non-blocking io
import os

class Engine:
    def __init__(self, _filepath, **kwargs):
        self.filepath = _filepath
        self.engineInst = subprocess.Popen(self.filepath,
                                           universal_newlines=True,
                                           stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
        
        # Setting up non-blocking stdout, will raise an exception instead
        # of blocking (unix only).
        fcntl.fcntl(self.engineInst.stdout.fileno(), fcntl.F_SETFL,
                    os.O_NONBLOCK)
    
    def write(self, message):
        self.engineInst.stdin.write(message)

    def read(self):
        try:
            return self.engineInst.stdout.readline()
        except IOError:
            return None
            
    def readAll(self):
        while True:
            message = self.read()
            if message is None:
                break
            else:
                yield message

    def close(self):
        self.engineInst.terminate()
