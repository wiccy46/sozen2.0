import pygame, os

os.chdir('./audio/sine') # load image. 
pygame.mixer.init()
pygame.mixer.music.load("n3.wav")
pygame.mixer.music.play()
print "finished Play"