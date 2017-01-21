import cv2
import numpy as np
import threading, sys, time

class MusGen(threading.Thread):
    def __init__(self, keyponts, zones):
        threading.Thread.__init__(self)
        self.kp = keyponts
        self.zones = zones
        self.baseNote = -1
        self._stop = threading.Event()

    def run(self):
        # I should put the generative modal here.
        # Next step is try to play a sample note and see if it works. ..
        for i in range(10):
            self.baseNote = np.argmax(self.zones)
            print self.zones
            time.sleep(1)

    def stop(self):
        self._stop.set()






