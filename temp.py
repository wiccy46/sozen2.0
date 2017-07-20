from pyo import *
import time
filename = "n0.wav"
s = Server().boot()
s.start()
path = "./audio/sine/" + filename


fifo = FIFOPlayer(maxsize = 100, mul = [0.9, 0.9]).out()

fifo.put(path)
#
# sf = SfPlayer(path, speed = [1, 1], loop = False,mul = 0.9 ).out()

# s.gui(locals())
