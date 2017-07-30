import pygame, os, time
os.chdir('./audio/sine') # load image. 
print "before init"
pygame.mixer.init(frequency = 44100, )
print "before load"
a= pygame.mixer.Sound("n3.wav")
print"after load"

print "Number of Channels: "
print pygame.mixer.get_num_channels()

a.play()
a_length = a.get_length()
# pygame.mixer.music.load("n3.wav")
# pygame.mixer.music.play()
time.sleep(a_length) # This is important
