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
        self.notes = np.zeros(9)

    def run(self):
        # I should put the generative modal here.
        # Next step is try to play a sample note and see if it works. ..
        self.baseNote =  np.argmax(self.zones)
        self.notes[self.baseNote] = 0
        if (self.baseNote == 0):
            for i in range (9):
                if i == 0:
                    pass
                else:
                    self.notes[i] = self.notes[i - 1] + 1
        elif (self.baseNote == 8):
            for i in range (9, 0):
                if i == 8:
                    pass
                else:
                    self.note[i] = self.note[i + 1] - 1
        else:
            for i in range(self.baseNote -1, 0):
                self.notes[i] = self.notes[i + 1] - 1
            for i in range(self.baseNote + 1, 8):
                self.notes[i] = self.notes[i - 1] + 1
        print (self.notes)


    def stopit(self):
        self._stop.set()

    def stopped(self):
        return self._stopper.is_set()






