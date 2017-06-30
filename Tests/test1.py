background_image_filename='dispersions.png'
mouse_image_filename='IMG_2985.jpg'

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen=pygame.display.set_mode((640,480),RESIZABLE,32)
pygame.display.set_caption("Hellow, World!")

background=pygame.image.load(background_image_filename).convert_alpha()
mouse_cursor=pygame.image.load(mouse_image_filename).convert()

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()

	screen.blit(background,(0,0))

	x,y=pygame.mouse.get_pos()

	x-=mouse_cursor.get_width()/2
	y-=mouse_cursor.get_width()/2

	screen.blit(mouse_cursor,(x,y))

	pygame.display.update()