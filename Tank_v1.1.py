#Tank Battle
#Game Imports
import pygame
from pygame.locals import *
import sys
import random
import time
from gameobjects.vector2 import Vector2

pygame.mixer.pre_init(44100,-16,2,1024*4)
pygame.init()
pygame.mixer.set_num_channels(8)

#Play surface Intialization
screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption('Tank Battle')

#FPS Controller
clock=pygame.time.Clock()

#Load sound files 
fire_sound=pygame.mixer.Sound("blip.wav")
hit_sound=pygame.mixer.Sound("gameover.wav")
bgm_sound=pygame.mixer.Sound("bgm.wav")

#Game Instructions function
def GameIns():
	lastbgm=pygame.time.get_ticks()-bgm_sound.get_length()*1000
	while True:
		if pygame.time.get_ticks()-lastbgm>bgm_sound.get_length()*1000:
			lastbgm=pygame.time.get_ticks()
			bgm_sound.play()
		#check if quit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		#show game title
		screen.fill((255,255,255))
		title_font=pygame.font.SysFont('arial',72)
		gametitle_surface=title_font.render('TANK BATTLE',True,(54,168,196))
		gametitle_rect=gametitle_surface.get_rect()
		gametitle_rect.midtop=(320,120)
		screen.blit(gametitle_surface,gametitle_rect)

		#show start game instructions
		text_font=pygame.font.SysFont('arial',60)

		single_surface=text_font.render('1P --- Press 1',True,(244,131,66))
		single_rect=single_surface.get_rect()
		single_rect.midtop=(320,240)
		screen.blit(single_surface,single_rect)

		multi_surface=text_font.render('2P --- Press 2',True,(244,131,66))
		multi_rect=multi_surface.get_rect()
		multi_rect.midtop=(320,280)
		screen.blit(multi_surface,multi_rect)
		pygame.display.update()

		#choose game mode
		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_2]:
			GameMulti()
		elif pressed_keys[K_1]:
			GameSingle()
		elif pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))

#Show health function
def PrintLife(ahealth=0,bhealth=0,multi=True):
	text_font=pygame.font.SysFont('arial',32)

	if multi:
		alife_surface=text_font.render('Player A',True,(249,175,47))
		alife_rect=alife_surface.get_rect()
		alife_rect.midtop=(50,15)
		screen.blit(alife_surface,alife_rect)
		blife_surface=text_font.render('Player B',True,(47,206,249))
		blife_rect=blife_surface.get_rect()
		blife_rect.midtop=(590,15)
		screen.blit(blife_surface,blife_rect)
	else:
		alife_surface=text_font.render('Player',True,(249,175,47))
		alife_rect=alife_surface.get_rect()
		alife_rect.midtop=(50,15)
		screen.blit(alife_surface,alife_rect)
		blife_surface=text_font.render('Computer',True,(47,206,249))
		blife_rect=blife_surface.get_rect()
		blife_rect.midtop=(590,15)
		screen.blit(blife_surface,blife_rect)

	#show Tank A health
	ap=0
	yy=50
	while ap<ahealth:
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(5+15*ap,yy,15,10))
		ap+=1

	#show Tank B health
	bp=0
	yy=50
	while bp<bhealth:
		pygame.draw.rect(screen,(255,0,0),pygame.Rect(620-15*bp,yy,15,10))
		bp+=1

#Multi-player
def GameMulti():
	#Tank A settings
	a_color=pygame.Color(249,175,47)
	a_dir='r'
	a_length=15
	a_width=15
	a_barrel=6
	a_barrelw=4
	a_cpos=[100,240]
	a_speed=5
	a_cd=500
	ahealth=5

	#Tank B settings
	b_color=pygame.Color(47,206,249)
	b_dir='l'
	b_length=15
	b_width=15
	b_barrel=6
	b_barrelw=4
	b_cpos=[540,240]
	b_speed=5
	b_cd=500
	bhealth=5

	#Tank A bullet settings
	abul_speed=10
	abul_pos=[]
	abul_side=4
	abul_color=pygame.Color(244,128,66)
	a_last=pygame.time.get_ticks()

	#Tank B bullet settings
	bbul_speed=10
	bbul_pos=[]
	bbul_side=4
	bbul_color=pygame.Color(197,66,244)
	b_last=a_last

	#main loop
	while True:
		#check if quit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys=pygame.key.get_pressed()
		#check if quit
		if pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))

		#get Tank A's new direction
		achange=False
		amove=True
		if pressed_keys[K_a] and a_dir!='l':
			a_dir='l'
			achange=True
		elif pressed_keys[K_d] and a_dir!='r':
			a_dir='r'
			achange=True
		elif pressed_keys[K_w] and a_dir!='u':
			a_dir='u'
			achange=True
		elif pressed_keys[K_s] and a_dir!='d':
			a_dir='d'
			achange=True
		if not (pressed_keys[K_a] or pressed_keys[K_d] or pressed_keys[K_w] or pressed_keys[K_s]):
			amove=False

		#get Tank B's new direction
		bchange=False
		bmove=True
		if pressed_keys[K_LEFT] and b_dir!='l':
			b_dir='l'
			bchange=True
		elif pressed_keys[K_RIGHT] and b_dir!='r':
			b_dir='r'
			bchange=True
		elif pressed_keys[K_UP] and b_dir!='u':
			b_dir='u'
			bchange=True
		elif pressed_keys[K_DOWN] and b_dir!='d':
			b_dir='d'
			bchange=True
		if not (pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_UP] or pressed_keys[K_DOWN]):
			bmove=False

		#Tank A position update
		if (not achange) and amove:
			#move if direction hasn't changed
			if a_dir=='l':
				a_cpos[0]-=a_speed
				if a_cpos[0]-(a_length/2)-a_barrel<0:
					a_cpos[0]=(a_length/2)+a_barrel
			elif a_dir=='r':
				a_cpos[0]+=a_speed
				if a_cpos[0]+(a_length/2)+a_barrel>640:
					a_cpos[0]=640-(a_length/2)-a_barrel
			elif a_dir=='u':
				a_cpos[1]-=a_speed
				if a_cpos[1]-(a_length/2)-a_barrel<0:
					a_cpos[1]=(a_length/2)+a_barrel
			elif a_dir=='d':
				a_cpos[1]+=a_speed
				if a_cpos[1]+(a_length/2)+a_barrel>480:
					a_cpos[1]=480-(a_length/2)-a_barrel

		#Tank B position update
		if (not bchange) and bmove:
			#move if direction hasn't changed
			if b_dir=='l':
				b_cpos[0]-=b_speed
				if b_cpos[0]-(b_length/2)-b_barrel<0:
					b_cpos[0]=(b_length/2)+b_barrel
			elif b_dir=='r':
				b_cpos[0]+=b_speed
				if b_cpos[0]+(b_length/2)+b_barrel>640:
					b_cpos[0]=640-(b_length/2)-b_barrel
			elif b_dir=='u':
				b_cpos[1]-=b_speed
				if b_cpos[1]-(b_length/2)-b_barrel<0:
					b_cpos[1]=(b_length/2)+b_barrel
			elif b_dir=='d':
				b_cpos[1]+=b_speed
				if b_cpos[1]+(b_length/2)+b_barrel>480:
					b_cpos[1]=480-(b_length/2)-b_barrel


		#Tank A bullets position update
		for bul in abul_pos:
			if bul[2]=='l':
				bul[0]-=abul_speed
			elif bul[2]=='r':
				bul[0]+=abul_speed
			elif bul[2]=='u':
				bul[1]-=abul_speed
			elif bul[2]=='d':
				bul[1]+=abul_speed
			if bul[0]<0 or bul[0]>640-abul_side or bul[1]<0 or bul[1]>480-abul_side:
				abul_pos.remove(bul)

		#Tank B bullets position update
		for bul in bbul_pos:
			if bul[2]=='l':
				bul[0]-=bbul_speed
			elif bul[2]=='r':
				bul[0]+=bbul_speed
			elif bul[2]=='u':
				bul[1]-=bbul_speed
			elif bul[2]=='d':
				bul[1]+=bbul_speed
			if bul[0]<0 or bul[0]>640-bbul_side or bul[1]<0 or bul[1]>480-bbul_side:
				bbul_pos.remove(bul)

		#check if A shoots new bullet
		now_time=pygame.time.get_ticks()
		if pressed_keys[K_c] and now_time-a_last>a_cd:
			a_last=now_time
			if a_dir=='l':
				abul_pos.append([a_cpos[0]-(a_length/2)-a_barrel-abul_side,a_cpos[1]-(a_barrelw/2),'l'])
			elif a_dir=='r':
				abul_pos.append([a_cpos[0]+(a_length/2)+a_barrel,a_cpos[1]-(a_barrelw/2),'r'])
			elif a_dir=='u':
				abul_pos.append([a_cpos[0]-(a_barrelw/2),a_cpos[1]-a_barrel-(a_length/2)-abul_side,'u'])
			elif a_dir=='d':
				abul_pos.append([a_cpos[0]-(a_barrelw/2),a_cpos[1]+(a_length/2)+a_barrel,'d'])
			if abul_pos[-1][0]<0 or abul_pos[-1][0]>640-abul_side or abul_pos[-1][1]<0 or abul_pos[-1][1]>480-abul_side:
				abul_pos.remove(abul_pos[-1])
			fire_sound.play()

		#check if B shoots new bullet
		if pressed_keys[K_l] and now_time-b_last>b_cd:
			b_last=now_time
			if b_dir=='l':
				bbul_pos.append([b_cpos[0]-(b_length/2)-b_barrel-bbul_side,b_cpos[1]-(b_barrelw/2),'l'])
			elif b_dir=='r':
				bbul_pos.append([b_cpos[0]+(b_length/2)+b_barrel,b_cpos[1]-(b_barrelw/2),'r'])
			elif b_dir=='u':
				bbul_pos.append([b_cpos[0]-(b_barrelw/2),b_cpos[1]-b_barrel-(b_length/2)-bbul_side,'u'])
			elif b_dir=='d':
				bbul_pos.append([b_cpos[0]-(b_barrelw/2),b_cpos[1]+(b_length/2)+b_barrel,'d'])
			if bbul_pos[-1][0]<0 or bbul_pos[-1][0]>640-bbul_side or bbul_pos[-1][1]<0 or bbul_pos[-1][1]>480-bbul_side:
				bbul_pos.remove(bbul_pos[-1])
			fire_sound.play()

		#check if the bullets collide
		for bula in abul_pos:
			for bulb in bbul_pos:
				if bula[0]==bulb[0] and bula[1]-bulb[1]<=10 and bula[1]-bulb[1]>=-10:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()
				elif bula[1]==bulb[1] and bula[0]-bulb[0]<=10 and bula[0]-bulb[0]>=-10:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()
				elif bula[0]-bulb[0]<abul_side and bula[0]-bulb[0]>-abul_side and bula[1]-bulb[1]<abul_side and bula[1]-bulb[1]>-abul_side:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()

		#check if A's bullets hit b
		for bula in abul_pos:
			if b_dir=='l' or b_dir=='r':
				if bula[0]-b_cpos[0]<((b_length+bbul_side)/2) and bula[0]-b_cpos[0]>-((b_length+bbul_side)/2) and bula[1]-b_cpos[1]<((b_width+bbul_side)/2) and bula[1]-b_cpos[1]>-((b_width+bbul_side)/2):
					bhealth-=1
					abul_pos.remove(bula)
					hit_sound.play()
			elif b_dir=='u' or b_dir=='d':
				if bula[0]-b_cpos[0]<((b_width+bbul_side)/2) and bula[0]-b_cpos[0]>-((b_width+bbul_side)/2) and bula[1]-b_cpos[1]<((b_length+bbul_side)/2) and bula[1]-b_cpos[1]>-((b_length+bbul_side)/2):
					bhealth-=1
					abul_pos.remove(bula)
					hit_sound.play()

		#check if B's bullets hit a
		for bulb in bbul_pos:
			if a_dir=='l' or a_dir=='r':
				if bulb[0]-a_cpos[0]<((a_length+abul_side)/2) and bulb[0]-a_cpos[0]>-((a_length+abul_side)/2) and bulb[1]-a_cpos[1]<((a_width+abul_side)/2) and bulb[1]-a_cpos[1]>-((a_width+abul_side)/2):
					ahealth-=1
					bbul_pos.remove(bulb)
					hit_sound.play()
			elif a_dir=='u' or a_dir=='d':
				if bulb[0]-a_cpos[0]<((a_width+abul_side)/2) and bulb[0]-a_cpos[0]>-((a_width+abul_side)/2) and bulb[1]-a_cpos[1]<((a_length+abul_side)/2) and bulb[1]-a_cpos[1]>-((a_length+abul_side)/2):
					ahealth-=1
					bbul_pos.remove(bulb)
					hit_sound.play()

		#Draw all the elements 
		screen.fill((255,255,255))
		#Draw Tank A
		if a_dir=='l':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2),a_cpos[1]-(a_width/2),a_length,a_width))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2)-a_barrel,a_cpos[1]-(a_barrelw/2),a_barrel,a_barrelw))
		elif a_dir=='r':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2),a_cpos[1]-(a_width/2),a_length,a_width))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]+(a_length/2),a_cpos[1]-(a_barrelw/2),a_barrel,a_barrelw))
		elif a_dir=='u':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_width/2),a_cpos[1]-(a_length/2),a_width,a_length))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_barrelw/2),a_cpos[1]-a_barrel-(a_length/2),a_barrelw,a_barrel))
		elif a_dir=='d':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_width/2),a_cpos[1]-(a_length/2),a_width,a_length))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_barrelw/2),a_cpos[1]+(a_length/2),a_barrelw,a_barrel))

		#Draw Tank B
		if b_dir=='l':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2),b_cpos[1]-(b_width/2),b_length,b_width))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2)-b_barrel,b_cpos[1]-(b_barrelw/2),b_barrel,b_barrelw))
		elif b_dir=='r':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2),b_cpos[1]-(b_width/2),b_length,b_width))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]+(b_length/2),b_cpos[1]-(b_barrelw/2),b_barrel,b_barrelw))
		elif b_dir=='u':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_width/2),b_cpos[1]-(b_length/2),b_width,b_length))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_barrelw/2),b_cpos[1]-b_barrel-(b_length/2),b_barrelw,b_barrel))
		elif b_dir=='d':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_width/2),b_cpos[1]-(b_length/2),b_width,b_length))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_barrelw/2),b_cpos[1]+(b_length/2),b_barrelw,b_barrel))

		#Draw Tank A's bullets
		for bu in abul_pos:
			pygame.draw.rect(screen,abul_color,pygame.Rect(bu[0],bu[1],abul_side,abul_side))

		#Draw Tank B's bullets
		for bu in bbul_pos:
			pygame.draw.rect(screen,bbul_color,pygame.Rect(bu[0],bu[1],bbul_side,bbul_side))

		#show remaining life
		PrintLife(ahealth,bhealth,True)

		if ahealth==0 or bhealth==0:
			GameOver(ahealth,bhealth,True)

		pygame.display.update()

#Versus AI
def GameSingle():
	#Tank A settings
	a_color=pygame.Color(249,175,47)
	a_dir='r'
	a_length=15
	a_width=15
	a_barrel=6
	a_barrelw=4
	a_cpos=[100,240]
	a_speed=5
	a_cd=500
	ahealth=5

	#Tank B settings
	b_color=pygame.Color(47,206,249)
	b_dir='l'
	b_length=15
	b_width=15
	b_barrel=6
	b_barrelw=4
	b_cpos=[540,240]
	b_speed=5
	b_cd=550
	bhealth=5
	bmove=True

	#Tank A bullet settings
	abul_speed=10
	abul_pos=[]
	abul_side=4
	abul_color=pygame.Color(244,128,66)
	a_last=pygame.time.get_ticks()

	#Tank B bullet settings
	bbul_speed=10
	bbul_pos=[]
	bbul_side=4
	bbul_color=pygame.Color(197,66,244)
	b_last=a_last

	while True:
		#check if quit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		pressed_keys=pygame.key.get_pressed()
		#check if quit
		if pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))

		#get Tank A's new direction
		achange=False
		amove=True
		if pressed_keys[K_a] and a_dir!='l':
			a_dir='l'
			achange=True
		elif pressed_keys[K_d] and a_dir!='r':
			a_dir='r'
			achange=True
		elif pressed_keys[K_w] and a_dir!='u':
			a_dir='u'
			achange=True
		elif pressed_keys[K_s] and a_dir!='d':
			a_dir='d'
			achange=True
		if not (pressed_keys[K_a] or pressed_keys[K_d] or pressed_keys[K_w] or pressed_keys[K_s]):
			amove=False

		#Tank A position update
		if (not achange) and amove:
			#move if direction hasn't changed
			if a_dir=='l':
				a_cpos[0]-=a_speed
				if a_cpos[0]-(a_length/2)-a_barrel<0:
					a_cpos[0]=(a_length/2)+a_barrel
			elif a_dir=='r':
				a_cpos[0]+=a_speed
				if a_cpos[0]+(a_length/2)+a_barrel>640:
					a_cpos[0]=640-(a_length/2)-a_barrel
			elif a_dir=='u':
				a_cpos[1]-=a_speed
				if a_cpos[1]-(a_length/2)-a_barrel<0:
					a_cpos[1]=(a_length/2)+a_barrel
			elif a_dir=='d':
				a_cpos[1]+=a_speed
				if a_cpos[1]+(a_length/2)+a_barrel>480:
					a_cpos[1]=480-(a_length/2)-a_barrel

		#Tank B position update
		if bmove:
			if b_dir=='l':
				b_cpos[0]-=b_speed
				if b_cpos[0]-(b_length/2)-b_barrel<0:
					b_cpos[0]=(b_length/2)+b_barrel
			elif b_dir=='r':
				b_cpos[0]+=b_speed
				if b_cpos[0]+(b_length/2)+b_barrel>640:
					b_cpos[0]=640-(b_length/2)-b_barrel
			elif b_dir=='u':
				b_cpos[1]-=b_speed
				if b_cpos[1]-(b_length/2)-b_barrel<0:
					b_cpos[1]=(b_length/2)+b_barrel
			elif b_dir=='d':
				b_cpos[1]+=b_speed
				if b_cpos[1]+(b_length/2)+b_barrel>480:
					b_cpos[1]=480-(b_length/2)-b_barrel

		#Tank A bullets position update
		for bul in abul_pos:
			if bul[2]=='l':
				bul[0]-=abul_speed
			elif bul[2]=='r':
				bul[0]+=abul_speed
			elif bul[2]=='u':
				bul[1]-=abul_speed
			elif bul[2]=='d':
				bul[1]+=abul_speed
			if bul[0]<0 or bul[0]>640-abul_side or bul[1]<0 or bul[1]>480-abul_side:
				abul_pos.remove(bul)

		#Tank B bullets position update
		for bul in bbul_pos:
			if bul[2]=='l':
				bul[0]-=bbul_speed
			elif bul[2]=='r':
				bul[0]+=bbul_speed
			elif bul[2]=='u':
				bul[1]-=bbul_speed
			elif bul[2]=='d':
				bul[1]+=bbul_speed
			if bul[0]<0 or bul[0]>640-bbul_side or bul[1]<0 or bul[1]>480-bbul_side:
				bbul_pos.remove(bul)

		#check if the bullets collide
		for bula in abul_pos:
			for bulb in bbul_pos:
				if bula[0]==bulb[0] and bula[1]-bulb[1]<=10 and bula[1]-bulb[1]>=-10:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()
				elif bula[1]==bulb[1] and bula[0]-bulb[0]<=10 and bula[0]-bulb[0]>=-10:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()
				elif bula[0]-bulb[0]<abul_side and bula[0]-bulb[0]>-abul_side and bula[1]-bulb[1]<abul_side and bula[1]-bulb[1]>-abul_side:
					abul_pos.remove(bula)
					bbul_pos.remove(bulb)
					hit_sound.play()

		#check if A's bullets hit b
		for bula in abul_pos:
			if b_dir=='l' or b_dir=='r':
				if bula[0]-b_cpos[0]<((b_length+bbul_side)/2) and bula[0]-b_cpos[0]>-((b_length+bbul_side)/2) and bula[1]-b_cpos[1]<((b_width+bbul_side)/2) and bula[1]-b_cpos[1]>-((b_width+bbul_side)/2):
					bhealth-=1
					abul_pos.remove(bula)
					hit_sound.play()
			elif b_dir=='u' or b_dir=='d':
				if bula[0]-b_cpos[0]<((b_width+bbul_side)/2) and bula[0]-b_cpos[0]>-((b_width+bbul_side)/2) and bula[1]-b_cpos[1]<((b_length+bbul_side)/2) and bula[1]-b_cpos[1]>-((b_length+bbul_side)/2):
					bhealth-=1
					abul_pos.remove(bula)
					hit_sound.play()

		#check if B's bullets hit a
		for bulb in bbul_pos:
			if a_dir=='l' or a_dir=='r':
				if bulb[0]-a_cpos[0]<((a_length+abul_side)/2) and bulb[0]-a_cpos[0]>-((a_length+abul_side)/2) and bulb[1]-a_cpos[1]<((a_width+abul_side)/2) and bulb[1]-a_cpos[1]>-((a_width+abul_side)/2):
					ahealth-=1
					bbul_pos.remove(bulb)
					hit_sound.play()
			elif a_dir=='u' or a_dir=='d':
				if bulb[0]-a_cpos[0]<((a_width+abul_side)/2) and bulb[0]-a_cpos[0]>-((a_width+abul_side)/2) and bulb[1]-a_cpos[1]<((a_length+abul_side)/2) and bulb[1]-a_cpos[1]>-((a_length+abul_side)/2):
					ahealth-=1
					bbul_pos.remove(bulb)
					hit_sound.play()

		#check if A shoots new bullet
		now_time=pygame.time.get_ticks()
		if pressed_keys[K_c] and now_time-a_last>a_cd:
			a_last=now_time
			if a_dir=='l':
				abul_pos.append([a_cpos[0]-(a_length/2)-a_barrel-abul_side,a_cpos[1]-(a_barrelw/2),'l'])
			elif a_dir=='r':
				abul_pos.append([a_cpos[0]+(a_length/2)+a_barrel,a_cpos[1]-(a_barrelw/2),'r'])
			elif a_dir=='u':
				abul_pos.append([a_cpos[0]-(a_barrelw/2),a_cpos[1]-a_barrel-(a_length/2)-abul_side,'u'])
			elif a_dir=='d':
				abul_pos.append([a_cpos[0]-(a_barrelw/2),a_cpos[1]+(a_length/2)+a_barrel,'d'])
			if abul_pos[-1][0]<0 or abul_pos[-1][0]>640-abul_side or abul_pos[-1][1]<0 or abul_pos[-1][1]>480-abul_side:
				abul_pos.remove(abul_pos[-1])
			fire_sound.play()

		#check if B shoots new bullet
		if now_time-b_last>b_cd:
			b_last=now_time
			if b_dir=='l':
				bbul_pos.append([b_cpos[0]-(b_length/2)-b_barrel-bbul_side,b_cpos[1]-(b_barrelw/2),'l'])
			elif b_dir=='r':
				bbul_pos.append([b_cpos[0]+(b_length/2)+b_barrel,b_cpos[1]-(b_barrelw/2),'r'])
			elif b_dir=='u':
				bbul_pos.append([b_cpos[0]-(b_barrelw/2),b_cpos[1]-b_barrel-(b_length/2)-bbul_side,'u'])
			elif b_dir=='d':
				bbul_pos.append([b_cpos[0]-(b_barrelw/2),b_cpos[1]+(b_length/2)+b_barrel,'d'])
			if bbul_pos[-1][0]<0 or bbul_pos[-1][0]>640-bbul_side or bbul_pos[-1][1]<0 or bbul_pos[-1][1]>480-bbul_side:
				bbul_pos.remove(bbul_pos[-1])
			fire_sound.play()

		#Draw all the elements 
		screen.fill((255,255,255))
		#Draw Tank A
		if a_dir=='l':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2),a_cpos[1]-(a_width/2),a_length,a_width))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2)-a_barrel,a_cpos[1]-(a_barrelw/2),a_barrel,a_barrelw))
		elif a_dir=='r':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_length/2),a_cpos[1]-(a_width/2),a_length,a_width))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]+(a_length/2),a_cpos[1]-(a_barrelw/2),a_barrel,a_barrelw))
		elif a_dir=='u':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_width/2),a_cpos[1]-(a_length/2),a_width,a_length))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_barrelw/2),a_cpos[1]-a_barrel-(a_length/2),a_barrelw,a_barrel))
		elif a_dir=='d':
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_width/2),a_cpos[1]-(a_length/2),a_width,a_length))
			pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_barrelw/2),a_cpos[1]+(a_length/2),a_barrelw,a_barrel))

		#Draw Tank B
		if b_dir=='l':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2),b_cpos[1]-(b_width/2),b_length,b_width))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2)-b_barrel,b_cpos[1]-(b_barrelw/2),b_barrel,b_barrelw))
		elif b_dir=='r':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_length/2),b_cpos[1]-(b_width/2),b_length,b_width))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]+(b_length/2),b_cpos[1]-(b_barrelw/2),b_barrel,b_barrelw))
		elif b_dir=='u':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_width/2),b_cpos[1]-(b_length/2),b_width,b_length))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_barrelw/2),b_cpos[1]-b_barrel-(b_length/2),b_barrelw,b_barrel))
		elif b_dir=='d':
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_width/2),b_cpos[1]-(b_length/2),b_width,b_length))
			pygame.draw.rect(screen,b_color,pygame.Rect(b_cpos[0]-(b_barrelw/2),b_cpos[1]+(b_length/2),b_barrelw,b_barrel))

		#Draw Tank A's bullets
		for bu in abul_pos:
			pygame.draw.rect(screen,abul_color,pygame.Rect(bu[0],bu[1],abul_side,abul_side))

		#Draw Tank B's bullets
		for bu in bbul_pos:
			pygame.draw.rect(screen,bbul_color,pygame.Rect(bu[0],bu[1],bbul_side,bbul_side))

		#show remaining life
		PrintLife(ahealth,bhealth,False)

		if ahealth==0 or bhealth==0:
			GameOver(ahealth,bhealth,False)

		pygame.display.update()

		if a_cpos[0]<b_cpos[0] and a_cpos[1]<b_cpos[1]:
			if b_cpos[0]-a_cpos[0]>b_cpos[1]-a_cpos[1]:
				b_dir='u'
			else:
				b_dir='l'
			bmove=True
		elif a_cpos[0]>b_cpos[0] and a_cpos[1]<b_cpos[1]:
			if a_cpos[0]-b_cpos[0]>b_cpos[1]-a_cpos[1]:
				b_dir='u'
			else:
				b_dir='r'
			bmove=True
		elif a_cpos[0]<b_cpos[0] and a_cpos[1]>b_cpos[1]:
			if b_cpos[0]-a_cpos[0]>a_cpos[1]-b_cpos[1]:
				b_dir='d'
			else:
				b_dir='l'
			bmove=True
		elif a_cpos[0]>b_cpos[0] and a_cpos[1]>b_cpos[1]:
			if a_cpos[0]-b_cpos[0]>a_cpos[1]-b_cpos[1]:
				b_dir='d'
			else:
				b_dir='r'
			bmove=True
		else:
			if a_cpos[0]==b_cpos[0] and a_cpos[1]==b_cpos[1]:
				bmove=True
			elif a_cpos[0]==b_cpos[0]:
				bmove=False
				if a_cpos[1]>b_cpos[1]:
					b_dir='d'
				else:
					b_dir='u'
			else:
				bmove=False
				if a_cpos[0]>b_cpos[0]:
					b_dir='r'
				else:
					b_dir='l'

#Game over
def GameOver(ahealth=0,bhealth=0,multi=True):
	text_font=pygame.font.SysFont('arial',48)
	gameover_surface=text_font.render('Game Over!',True,(255,0,0))
	gameover_rect=gameover_surface.get_rect()
	gameover_rect.midtop=(320,15)
	screen.blit(gameover_surface,gameover_rect)

	if multi:
	#multi-player case
		if ahealth==0 and bhealth==0:
			result_surface=text_font.render('Draw!',True,(131,18,183))
		elif ahealth==0:
			result_surface=text_font.render('Player 2 Won!',True,(47,206,249))
		else:
			result_surface=text_font.render('Player 1 Won!',True,(249,175,47))

	else:
	#single-player case 
		if ahealth==0 and bhealth==0:
			result_surface=text_font.render('Draw!',True,(131,18,183))
		elif ahealth==0:
			result_surface=text_font.render('You Lost...',True,(131,18,183))
		else:
			result_surface=text_font.render('You Won!',True,(131,18,183))

	#update result
	result_rect=result_surface.get_rect()
	result_rect.midtop=(320,50)
	screen.blit(result_surface,result_rect)
	pygame.display.update()

	#wait for 2 seconds
	time.sleep(2)

	#play again or quit?
	while True:
		#check if quit
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()

		#show play again/return to menu option
		stext_font=pygame.font.SysFont('arial',40)
		gamenext_surface=stext_font.render('Press Enter to play again!',True,(244,66,113))
		gamenext_rect=gamenext_surface.get_rect()
		gamenext_rect.midtop=(320,320)
		screen.blit(gamenext_surface,gamenext_rect)
		pygame.display.update()

		gameback_surface=stext_font.render('Press Space to return to main menu',True,(244,66,113))
		gameback_rect=gameback_surface.get_rect()
		gameback_rect.midtop=(320,360)
		screen.blit(gameback_surface,gameback_rect)
		pygame.display.update()

		#check if play again
		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_RETURN]:
			if multi:
				GameMulti()
			else:
				GameSingle()
		elif pressed_keys[K_ESCAPE]:
			pygame.event.post(pygame.event.Event(pygame.QUIT))
		elif pressed_keys[K_SPACE]:
			GameIns()

GameIns()