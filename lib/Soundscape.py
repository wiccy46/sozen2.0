# soundscape mode 

import threading, sys, time, random, os
import pyaudio, wave

BUFFER_SIZE = 1024

"""
It needs a clear soundfile management system. 
"""

OBJECT = []
OBJECT_folders = []
for (path, dirnames, filenames) in os.walk('./audio/soundscape/object/'):
    OBJECT_folders.extend(os.path.join(path, name) for name in dirnames)
    OBJECT.extend(os.path.join(path, name) for name in filenames)


ENV = []
ENV_folders = []
for (path, dirnames, filenames) in os.walk('./audio/soundscape/env/'):
    ENV_folders.extend(os.path.join(path, name) for name in dirnames)
    ENV.extend(os.path.join(path, name) for name in filenames)


# Do a string search based on : birds, winds and so on. Need to rename the folders.

class SoundscapeGen(threading.Thread):
	def __init__(self, chn = 2):  # By default stereo\
		threading.Thread.__init__(self)
		self.filename = OBJECT[0]
		self.wf = wave.open(self.filename, 'rb')
		self.p = pyaudio.PyAudio()
		self.stop_flag = False

		# self.stream = update_stream()


	def update_stream(self):

		def callback(in_data, frame_count, time_info, status):
			data = self.wf.readframes(frame_count)
			return(data, pyaudio.paContinue)
		return self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback = callback)


	def run(self):
		print "play audio"
		# self.stream.start_stream()
		# wait for stream to finish (5)
		for i in range(len(OBJECT)):
			if not self.stop_flag:  # USe stop_flag to prevent loop still going on even though stop button is pushed.  
				self.filename = OBJECT[i]
				self.wf = wave.open(self.filename, 'rb')
				self.stream = self.update_stream()
				self.stream.start_stream()
				while self.stream.is_active():
					time.sleep(0.1)
				i = i + 1
				print "next sound"
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()



	def stopit(self):
		print ("Soundscape: Stop stream")
		self.stop_flag = True
		self.stream.stop_stream()

		# self.stream.close()
		# self.p.terminate()
		self._stop.set()


	def stopped(self):			
		return self._stopper.is_set()




# class SoundscapeGen(threading.Thread):
# 	def __init__(self, chn = 2):  # By default stereo\
# 		threading.Thread.__init__(self)
# 		self.filename = OBJECT[0]
# 		self.wf = wave.open(self.filename, 'rb')
# 		self.p = pyaudio.PyAudio()
# 		self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
#                 channels=self.wf.getnchannels(),
#                 rate=self.wf.getframerate(),
#                 output=True)
# 		self.data = self.wf.readframes(BUFFER_SIZE)
# 	def run(self):
# 		print "play audio"
# 		while self.data != '':
# 			try:
# 				self.stream.write(self.data)
# 				self.data = self.wf.readframes(BUFFER_SIZE)
# 			except IOError:
# 				print "Soundscape: Stream is stopped. "
# 				break
# 		self.stream.stop_stream()
# 		self.stream.close()
# 		self.p.terminate()
# 	def stopit(self):
# 		print ("Soundscape: Stop stream")
# 		self.stream.stop_stream()

# 		# self.stream.close()
# 		# self.p.terminate()
# 		self._stop.set()


# 	def stopped(self):			
# 		return self._stopper.is_set()