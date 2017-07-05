#Flappy Block
#Game imports
import pygame
from pygame.locals import *
import sys
import random
import time
from gameobjects.vector2 import Vector2

pygame.mixer.pre_init(44100,-16,2,1024*4)
pygame.init()
pygame.mixer.set_num_channels(8)

#Play surface
screen = pygame.display.set_mode((480, 640), 0, 32)
pygame.display.set_caption('Flappy Block')

#FPS controller
clock = pygame.time.Clock()

#Load sound files
score_sound=pygame.mixer.Sound("blip.wav")
gameover_sound=pygame.mixer.Sound("gameover.wav")

#Game instructions function
def gameIns():
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_RETURN]:
			#show game instructions
			screen.fill((255,255,255))
			inst_font=pygame.font.SysFont('arial',48)
			inst_surface=inst_font.render('Press SPACE to jump!',True,(0,0,0))
			inst_rect=inst_surface.get_rect()
			inst_rect.midtop=(240,300)
			screen.blit(inst_surface,inst_rect)
			pygame.display.update()
			time.sleep(1)

			#go to main game
			gamePlay()
		elif pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))

		#show game title
		title_font=pygame.font.SysFont('arial',72)
		gametitle_surface=title_font.render('FLAPPY BLOCK',True,(54,168,196))
		gametitle_rect=gametitle_surface.get_rect()
		gametitle_rect.midtop=(240,200)
		screen.blit(gametitle_surface,gametitle_rect)

		#show start game instructions
		text_font=pygame.font.SysFont('arial',60)
		gameins_surface=text_font.render('Press Enter to start!',True,(244,131,66))
		gameins_rect=gameins_surface.get_rect()
		gameins_rect.midtop=(240,480)
		screen.blit(gameins_surface,gameins_rect)
		pygame.display.update()

#Show score function
def printScore(dead=True, score=0):
	score_font=pygame.font.SysFont('arial',32)
	score_surface=score_font.render('Score : {0}'.format(score), True, (47,224,203))
	score_rect=score_surface.get_rect()
	score_rect.midtop=(240,50)
	screen.blit(score_surface,score_rect)

def gamePlay():

	#Block settings
	block_pos=[200,320]		#height:320,horizontal position:200
	block_side=20
	block_color=pygame.Color(232,214,58)
	block_speed=-8;		#negative means going upward
	block_gravity=33;

	#pipe settings
	pipe_low=random.randrange(160,590);
	pipe_pos=[[pipe_low,pipe_low-100,480,510]]	#[h1,h2,x]
	pipe_color=pygame.Color(139,58,232)
	pipe_speed=5

	#score settings
	now_score=0

	#last time spot when speed is recorded
	last_spot=pygame.time.get_ticks()

	while True:
		#exit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		#draw elements onto screen
		#fill screen with all white again
		screen.fill((255,255,255))

		#draw the pipes
		for ip in pipe_pos:
			pygame.draw.rect(screen,pipe_color,pygame.Rect(ip[2],ip[0],ip[3]-ip[2],640-ip[0]))
			pygame.draw.rect(screen,pipe_color,pygame.Rect(ip[2],0,ip[3]-ip[2],ip[1]))
		
		#draw the block
		if block_pos[1]<0:
			pygame.draw.rect(screen,block_color,pygame.Rect(block_pos[0],0,block_side,block_pos[1]+block_side))
		else:
			pygame.draw.rect(screen,block_color,pygame.Rect(block_pos[0],block_pos[1],block_side,block_side))

		#print the score
		printScore(False,now_score)

		pygame.display.update()

		#check if the block jumps
		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_SPACE]:
			block_speed=-8;
			last_spot=pygame.time.get_ticks()

		#update the block position
		tot_time=pygame.time.get_ticks()-last_spot
		last_spot=pygame.time.get_ticks()
		mid_speed=block_speed+block_gravity*tot_time/1000
		block_speed=mid_speed+block_gravity*tot_time/1000
		block_pos[1]+=mid_speed

		#update the pipes position
		#make all the pipes shift left
		for ip in pipe_pos:
			ip[2]-=pipe_speed
			ip[3]-=pipe_speed
			if ip[3]<0:
				pipe_pos.remove(ip)
			elif ip[3]<30:
					ip[2]=0
			if ip[2]+30>480:
				ip[3]=480
		#add new pipe if passed curent one
		#add score by one
		if pipe_pos[-1][2]+30<block_pos[0]+block_side:
			pipe_low=random.randrange(160,590);
			pipe_pos.append([pipe_low,pipe_low-100,480,510])	#[h1,h2,x]
			now_score+=1
			score_sound.play()

		#check gameover condition
		#condition 1: block too high or too low
		if block_pos[1]>640 or block_pos[1]+block_side<0:
			gameOver(now_score)

		#condition 2: block crushes into the pipe
		for ip in pipe_pos:
			if (block_pos[0]+block_side>ip[2] and block_pos[0]+block_side<ip[3]) or (block_pos[0]>ip[2] and block_pos[0]<ip[3]):
				if not (block_pos[1]+block_side<ip[0] and block_pos[1]>ip[1]):
					gameOver(now_score)


#Game over function
def gameOver(score=0):
	#show "Game Over!" for five seconds
	text_font=pygame.font.SysFont('arial',48)
	gameover_surface=text_font.render('Game Over!',True,(255,0,0))
	gameover_rect=gameover_surface.get_rect()
	gameover_rect.midtop=(240,15)
	screen.blit(gameover_surface,gameover_rect)
	printScore(True,score)
	pygame.display.update()
	gameover_sound.play()

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
		gameover_rect.midtop=(240,15)
		screen.blit(gameover_surface,gameover_rect)
		pygame.display.update()

		#show play gain option
		gamenext_surface=text_font.render('Press Enter to play again!',True,(244,66,113))
		gamenext_rect=gamenext_surface.get_rect()
		gamenext_rect.midtop=(240,320)
		screen.blit(gamenext_surface,gamenext_rect)
		pygame.display.update()

		if pressed_keys[K_RETURN]:
			gamePlay()
		elif pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))

gameIns()