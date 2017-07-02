#SNAKE GAME
#Game imports
import pygame
from pygame.locals import *
import sys
import random
import time
from gameobjects.vector2 import Vector2

pygame.init()

#Play surface
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Snake Game')

#FPS controller
clock = pygame.time.Clock()

#Game instructions function
def gameIns():
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_RETURN]:
			gamePlay()
		text_font=pygame.font.SysFont('arial',60)
		gameins_surface=text_font.render('Press Enter to start!',True,(244,131,66))
		gameins_rect=gameins_surface.get_rect()
		gameins_rect.midtop=(320,240)
		screen.blit(gameins_surface,gameins_rect)
		pygame.display.update()

def gamePlay():
	last_time=0

	#Snake settings
	snake_pos=[250,240]												#head position
	snake_body=[[250,240],[240,240],[230,240]]						#body
	snake_speed=10;
	snake_color=pygame.Color(66,170,244) 

	#food settings
	food_pos=[[random.randrange(1,63)*10,random.randrange(1,47)*10]]	#food position
	food_exist=True
	food_color=pygame.Color(244,212,66)
	food_generate_time=5000

	now_direction='r'
	to_direction=now_direction
	#Main loop
	while True:
		#exit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		#get the new position, if any
		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_LEFT] or pressed_keys[K_a]:
			to_direction='l'
		elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
			to_direction='r'
		elif pressed_keys[K_UP] or pressed_keys[K_w]:
			to_direction='u'
		elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
			to_direction='d'
		elif pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(QUIT))

		#make sure the directions do not contradict
		if to_direction=='l' and not now_direction=='r':
			now_direction=to_direction
		if to_direction=='r' and not now_direction=='l':
			now_direction=to_direction
		if to_direction=='u' and not now_direction=='d':
			now_direction=to_direction
		if to_direction=='d' and not now_direction=='u':
			now_direction=to_direction

		#update snake head position
		if now_direction=='l':
			snake_pos[0]-=snake_speed
		elif now_direction=='r':
			snake_pos[0]+=snake_speed
		elif now_direction=='u':
			snake_pos[1]-=snake_speed
		elif now_direction=='d':
			snake_pos[1]+=snake_speed

		snake_pos[0]=(snake_pos[0]+640)%640
		snake_pos[1]=(snake_pos[1]+480)%480

		#update snake body position
		reached_food=False
		snake_body.insert(0,list(snake_pos))
		for food in food_pos:
			if snake_pos[0]==food[0] and snake_pos[1]==food[1]:
				reached_food=True
				food_pos.remove([food[0],food[1]])
		if not reached_food:
			snake_body.pop()

		#check game over condition
		for ip in snake_body[3:]:
			if ip[0]==snake_pos[0] and ip[1]==snake_pos[1]:
				gameOver()

		#create a new food
		#condition 1: enough time has passed to generate a new food
		if pygame.time.get_ticks()-last_time>food_generate_time:
			last_time=pygame.time.get_ticks()
			food_pos.append([random.randrange(1,63)*10,random.randrange(1,47)*10])
		#condition 2: there is no food present
		if len(food_pos)==0:
			food_pos.append([random.randrange(1,63)*10,random.randrange(1,47)*10])
			last_time=pygame.time.get_ticks()

		screen.fill((255,255,255))
		for ip in snake_body:
			pygame.draw.rect(screen,snake_color,pygame.Rect(ip[0],ip[1],10,10))

		for food in food_pos:
			pygame.draw.rect(screen,food_color,pygame.Rect(food[0],food[1],10,10))
		pygame.display.update()


#Game over function
def gameOver():
	#show "Game Over!" for five seconds
	text_font=pygame.font.SysFont('arial',48)
	gameover_surface=text_font.render('Game Over!',True,(255,0,0))
	gameover_rect=gameover_surface.get_rect()
	gameover_rect.midtop=(320,15)
	screen.blit(gameover_surface,gameover_rect)
	pygame.display.update()

	#wait for 2 seconds
	time.sleep(2)

	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys=pygame.key.get_pressed()

		text_font=pygame.font.SysFont('arial',48)
		gameover_surface=text_font.render('Game Over!',True,(255,0,0))
		gameover_rect=gameover_surface.get_rect()
		gameover_rect.midtop=(320,15)
		screen.blit(gameover_surface,gameover_rect)
		pygame.display.update()

		#show play gain option
		gamenext_surface=text_font.render('Press Enter to play again!',True,(244,66,113))
		gamenext_rect=gamenext_surface.get_rect()
		gamenext_rect.midtop=(320,320)
		screen.blit(gamenext_surface,gamenext_rect)
		pygame.display.update()

		if pressed_keys[K_RETURN]:
			gamePlay()

gameIns()