import pygame, os, time
os.chdir('./audio/sine') # load image. 
print "before init"
pygame.mixer.init()
print "before load"
a= pygame.mixer.Sound("n3.wav")
a.play()
a_length = a.get_length()
# pygame.mixer.music.load("n3.wav")
# pygame.mixer.music.play()
time.sleep(a_length) # This is important
