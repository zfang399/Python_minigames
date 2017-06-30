import pygame
from pygame.locals import *
from sys import exit

chara_name='tux.jpg'

pygame.init()

screen=pygame.display.set_mode((640,480),0,32)

sprite=pygame.image.load(chara_name)

x=0

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()

	screen.blit(sprite,(x,100))
	x+=5

	if x>640:
		x=0

	pygame.display.update()