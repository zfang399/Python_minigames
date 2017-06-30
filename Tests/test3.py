import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen=pygame.display.set_mode((640,480),DOUBLEBUF|0,32)

keyboard_image_filename='tux.jpg'
keyboard=pygame.image.load(keyboard_image_filename).convert()

x,y=0,0
move_x,move_y=0,0
Fullscreen=False

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()
		if event.type==KEYDOWN:
			if event.key==K_LEFT:
				move_x= -1
			elif event.key==K_RIGHT:
				move_x= 1
			elif event.key==K_UP:
				move_y= -1
			elif event.key==K_DOWN:
				move_y= 1
			elif event.key==K_f:
				Fullscreen=not Fullscreen
				if Fullscreen:
					screen=pygame.display.set_mode((640,480),DOUBLEBUF|FULLSCREEN,32)
				else:
					screen=pygame.display.set_mode((640,480),DOUBLEBUF|0,32)
		elif event.type==KEYUP:
			move_x=0
			move_y=0

	x+=move_x
	y+=move_y
	screen.fill((0,0,0))
	screen.blit(keyboard,(x,y))
	pygame.display.flip()