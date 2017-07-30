# soundscape mode 

import threading, sys, time, random, os
import pyaudio, wave

BUFFER_SIZE = 1024



class SoundscapeGen(threading.Thread):
	def __init__(self, chn = 2):  # By default stereo\
		threading.Thread.__init__(self)
		filename = "./audio/soundscape/env/forest.wav"
		self.wf = wave.open(filename, 'rb')
		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True)
		self.data = self.wf.readframes(BUFFER_SIZE)

	def run(self):
		print "play audio"
		while self.data != '':
			try:
				self.stream.write(self.data)
				self.data = self.wf.readframes(BUFFER_SIZE)
			except IOError:
				print "Soundscape: Stream is stopped. "
				break
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()



	def stopit(self):
		print ("Soundscape: Stop stream")
		self.stream.stop_stream()

		# self.stream.close()
		# self.p.terminate()
		self._stop.set()


	def stopped(self):			
		return self._stopper.is_set()


