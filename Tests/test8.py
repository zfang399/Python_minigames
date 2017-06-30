import pygame
from pygame.locals import *
from sys import exit

chara_name='tux.jpg'

pygame.init()

screen=pygame.display.set_mode((640,480),0,32)

sprite=pygame.image.load(chara_name)

x=0
y=0
vx=5
vy=5

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()

	screen.fill((0,0,0))
	screen.blit(sprite,(x,y))
	x+=vx
	y+=vy

	if x+256>640:
		x=640-256
		vx=-vx

	if x<0:
		x=0
		vx=-vx

	if y+256>480:
		y=480-256
		vy=-vy

	if y<0:
		y=0
		vy=-vy
	pygame.display.update()