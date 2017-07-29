import pygame, os, time
os.chdir('./audio/sine') # load image. 
pygame.mixer.init()
pygame.mixer.music.load("n3.wav")
pygame.mixer.music.play()
time.sleep(2) # This is important
