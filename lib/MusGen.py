import numpy as np
import threading, sys, time, random
from lib.OscPart import sc

EP = 1 / 9 # The equal probablity of the 9 grid.


class MusGen(threading.Thread):
    def __init__(self, zones):
        threading.Thread.__init__(self)
        self.zones = zones
        self.baseNote = -1
        self._stop = threading.Event()
        self.notes = np.zeros(9)
        self.play_start = False
        self.bpm = 80

    def stop_play(self):
        self.play_start = False

    def rand_note(self):
        note = random.randint(0, 8)
        vel = random.randint(10, 100) / 100.0
        sc(note, vel)

    def rand_rythm(self):
        return random.randint(100, 2000) / 1000.

    def run(self):
        # I should put the generative modal here.
        # Next step is try to play a sample note and see if it works. ..
        self.play_start = True
        print (self.zones)
        self.baseNote =  np.argmax(self.zones)
        self.notes[self.baseNote] = 0
        if (self.baseNote == 0):
            for i in range (9):
                if i == 0:
                    pass
                else:
                    self.notes[i] = self.notes[i - 1] + 1
        elif (self.baseNote == 8):
            for i in range (8):
                self.notes[8 - i - 1] = self.notes[8 - i] - 1

        else:
            for i in range(0, self.baseNote):
                self.notes[self.baseNote - i - 1] = self.notes[self.baseNote - i ] - 1
            for i in range(self.baseNote + 1, 9):
                self.notes[i] = self.notes[i - 1] + 1
        self.notes = self.notes + 8
        print (self.notes)  # .d.sads
        while(self.play_start):
            print "play"
            print self.play_start
            self.rand_note()
            time.sleep(self.rand_rythm())


    def stopit(self):
        print ("Stop it called. ")
        self._stop.set()

    def stopped(self):
        return self._stopper.is_set()






