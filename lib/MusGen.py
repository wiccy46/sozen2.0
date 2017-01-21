import cv2
import numpy as np

class MusGen:
    def __init__(self, keyponts, zones):
        self.kp = keyponts
        self.zones = zones
        self.baseNote = -1

    def printNote(self):
        print self.zones

    def play(self):
        self.baseNote = np.argmax(self.zones)
        print self.baseNote



