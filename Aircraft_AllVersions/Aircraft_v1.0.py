#Aircraft
#Game Imports
import pygame
from pygame.locals import *
import sys
import random
import time
from gameobjects.vector2 import Vector2
from random import randint

pygame.mixer.pre_init(44100,-16,2,1024*4)
pygame.init()
pygame.mixer.set_num_channels(8)

#Play surface
screen = pygame.display.set_mode((480, 640), 0, 32)
pygame.display.set_caption('AirCraft')

#FPS controller
clock = pygame.time.Clock()

#Load sound files 
fire_sound=pygame.mixer.Sound("blip.wav")
hit_sound=pygame.mixer.Sound("gameover.wav")
bgm_sound=pygame.mixer.Sound("bgm.wav")

#Game Instructions function
def GameIns():
	bgm_sound.stop()
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
		gametitle_surface=title_font.render('AIRCRAFT',True,(54,168,196))
		gametitle_rect=gametitle_surface.get_rect()
		gametitle_rect.midtop=(240,240)
		screen.blit(gametitle_surface,gametitle_rect)

		#show start game instructions
		text_font=pygame.font.SysFont('arial',60)

		single_surface=text_font.render('1P --- Press 1',True,(244,131,66))
		single_rect=single_surface.get_rect()
		single_rect.midtop=(240,320)
		screen.blit(single_surface,single_rect)

		multi_surface=text_font.render('2P --- Press 2',True,(244,131,66))
		multi_rect=multi_surface.get_rect()
		multi_rect.midtop=(240,365)
		screen.blit(multi_surface,multi_rect)
		pygame.display.update()

		#choose game mode
		pressed_keys=pygame.key.get_pressed()
		if pressed_keys[K_2]:
			fire_sound.play()
			GameMulti()
		elif pressed_keys[K_1]:
			fire_sound.play()
			GameSingle()
		elif pressed_keys[K_ESCAPE]:
			fire_sound.play()
			pygame.event.post(pygame.event.Event(pygame.QUIT))

def PrintLife(ahealth=0,bhealth=0,multi=True):
	text_font=pygame.font.SysFont('arial',32)

	if multi:
		alife_surface=text_font.render('Player 1',True,(0,255,0))
		alife_rect=alife_surface.get_rect()
		alife_rect.midtop=(350,15)
		screen.blit(alife_surface,alife_rect)
		blife_surface=text_font.render('Player 2',True,(0,255,0))
		blife_rect=blife_surface.get_rect()
		blife_rect.midtop=(350,35)
		screen.blit(blife_surface,blife_rect)

		#show Plane A health
		ap=0
		yy=20
		while ap<ahealth:
			pygame.draw.rect(screen,(0,255,0),pygame.Rect(400+15*ap,yy,15,10))
			ap+=1

		#show Plane B health
		bp=0
		yy=40
		while bp<bhealth:
			pygame.draw.rect(screen,(0,255,0),pygame.Rect(400+15*bp,yy,15,10))
			bp+=1
	else:
		alife_surface=text_font.render('Life',True,(0,255,0))
		alife_rect=alife_surface.get_rect()
		alife_rect.midtop=(370,15)
		screen.blit(alife_surface,alife_rect)

		#show player's health
		ap=0
		yy=20
		while ap<ahealth:
			pygame.draw.rect(screen,(0,255,0),pygame.Rect(400+15*ap,yy,15,10))
			ap+=1

def GameSingle():
	bgm_sound.fadeout(1500)

	#stage settings
	stage_now=1
	last_stage_time=pygame.time.get_ticks()

	#Background settings
	bg_color=(255,255,255)
	bg_pos=[]
	bg_num=100
	for i in range(100):
		bg_pos.append([randint(0,479),randint(0,639)])

	#Plane settings
	a_color=pygame.Color(249,175,47)
	a_hm=0
	a_vm=0
	amove=False
	a_speed=5
	a_cpos=[240,590]
	a_vert1=12
	a_vert2=8
	a_hori1=8
	a_hori2=4
	a_thick=4
	ahealth=5
	ahealth_max=5
	ainvi=False
	ainvi_start=0

	#Plane bullet settings 
	abul_speed=10
	abul_pos=[]
	abul_side=4
	a_cd=400
	abul_color=pygame.Color(244,128,66)
	a_last=pygame.time.get_ticks()

	#Items settings
	#score items
	scg_last=a_last
	scg_cd=2000
	scg_color=pygame.Color(0,255,0)
	scg_pos=[]
	scg_side=[]

	#good items
	ordi_last=a_last
	ordi_cd=10*1000
	ordi_color=pygame.Color(0,0,255)
	ordi_pos=[]
	ordi_side=6
	#options: rand(1-100)
		#restore health by 1             1-33
		#faster bullet speed             34-68
		#reduces bullet firing interval  69-100
		#increase maximum health         49,50,51
		#increse moving speed            1,11,21,31,41
		#invincible for 6 secs           100,99,98

	#dangers
	dang_last=a_last
	dang_cd=3000
	dang_color=pygame.Color(255,0,0)
	dang_pos=[]
	dang_side=[]

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

		now_time=pygame.time.get_ticks()

		#update stage
		if now_time - last_stage_time>50000:
			stage_now+=1
			last_stage_time=now_time

		#update invicinble state
		if now_time - ainvi_start>6:
			ainvi=False

		#update background
		for b in bg_pos:
			b[1]+=stage_now*10
			if b[1]>640:
				bg_pos.remove(b)
				bg_num-=1

		while bg_num<100:
			bg_pos.append([randint(0,479),randint(0,5)])
			bg_num+=1

		#update items
		updated_g=False
		updated_b=False
		#update green
		if now_time - scg_last > scg_cd:
			updated_g=True
			scg_last=now_time
			scg_side.append(randint(10,20))
			scg_pos.append([randint(0,479-scg_side[-1]),-scg_side[-1]])

		#update blue
		if now_time - ordi_last > ordi_cd:
			updated_b=True
			ordi_last=now_time
			if updated_g:
				while True:
					ordi_pos.append([randint(0,479-ordi_side),-ordi_side])
					if ordi_pos[-1][0]<=scg_pos[-1][0]:
						if scg_pos[-1][0]-ordi_pos[-1][0]<ordi_side:
							ordi_pos.remove(ordi_pos[-1])
						else:
							break
					else:
						if ordi_pos[-1][0]-scg_pos[-1][0]<scg_side[-1]:
							ordi_pos.remove(ordi_pos[-1])
						else:
							break
			else:
				ordi_pos.append([randint(0,479-ordi_side),-ordi_side])

		#update red
		if now_time - dang_last > dang_cd:
			dang_last=now_time
			dang_side.append(randint(10,stage_now*10))
			if updated_g and updated_b:
				proper=False
				while not proper:
					dang_pos.append([randint(0,479-dang_side[-1]),-dang_side[-1]])
					if dang_pos[-1][0]<=ordi_pos[-1][0]:
						if ordi_pos[-1][0]-dang_pos[-1][0]<dang_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
					else:
						if dang_pos[-1][0]-ordi_pos[-1][0]<ordi_side:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
					if dang_pos[-1][0]<=scg_pos[-1][0]:
						if scg_pos[-1][0]-dang_pos[-1][0]<dang_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
					else:
						if dang_pos[-1][0]-scg_pos[-1][0]<scg_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
			elif updated_g:
				proper=False
				while not proper:
					dang_pos.append([randint(0,479-dang_side[-1]),-dang_side[-1]])
					if dang_pos[-1][0]<=scg_pos[-1][0]:
						if scg_pos[-1][0]-dang_pos[-1][0]<dang_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
					else:
						if dang_pos[-1][0]-scg_pos[-1][0]<scg_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
			elif updated_b:
				proper=False
				while not proper:
					dang_pos.append([randint(0,479-dang_side[-1]),-dang_side[-1]])
					if dang_pos[-1][0]<=ordi_pos[-1][0]:
						if ordi_pos[-1][0]-dang_pos[-1][0]<dang_side[-1]:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
					else:
						if dang_pos[-1][0]-ordi_pos[-1][0]<ordi_side:
							dang_pos.remove(dang_pos[-1])
							proper=False
							continue
						else:
							proper=True
			else:
				dang_pos.append([randint(0,479-dang_side[-1]),-dang_side[-1]])

		#update items' positions
		count=0
		while count<len(scg_pos):
			scg_pos[count][1]+=stage_now*10
			if scg_pos[count][1]>640:
				scg_pos.remove(scg_pos[count])
				scg_side.remove(scg_side[count])
			count+=1

		count=0
		while count<len(dang_pos):
			dang_pos[count][1]+=stage_now*10
			if dang_pos[count][1]>640:
				dang_pos.remove(dang_pos[count])
				dang_side.remove(dang_side[count])
			count+=1

		count=0
		while count<len(ordi_pos):
			ordi_pos[count][1]+=stage_now*10
			if ordi_pos[count][1]>640:
				ordi_pos.remove(ordi_pos[count])
			count+=1

		#update plane position
		a_hm=0
		a_vm=0
		if pressed_keys[K_LEFT] or pressed_keys[K_a]:
			a_hm-=a_speed
		if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
			a_hm+=a_speed
		if pressed_keys[K_UP] or pressed_keys[K_w]:
			a_vm-=a_speed
		if pressed_keys[K_DOWN] or pressed_keys[K_s]:
			a_vm+=a_speed

		a_cpos[0]+=a_hm
		a_cpos[1]+=a_vm
		#check if the plane is out of the panel, if so, move it back
		if a_cpos[0]<a_hori1+(a_thick/2):
			a_cpos[0]=a_hori1+(a_thick/2)
		elif a_cpos[0]>480-(a_thick/2)-a_hori1:
			a_cpos[0]=480-(a_thick/2)-a_hori1

		if a_cpos[1]<a_vert1+(a_thick/2):
			a_cpos[1]=a_vert1+(a_thick/2)
		elif a_cpos[1]>640-a_vert2-(a_thick/2):
			a_cpos[1]=640-a_vert2-(a_thick/2)

		#update bullets position
		if now_time-a_last>a_cd:
			a_last=now_time
			abul_pos.append([a_cpos[0]-(a_thick/2),a_cpos[1]-a_vert1+2])
		for bul in abul_pos:
			bul[1]-=abul_speed
			if bul[1]<0:
				abul_pos.remove(bul)
			else:
				count=0
				while count<len(scg_pos):
					if bul[1]+abul_speed>scg_pos[count][1] and bul[1]<scg_pos[count][1]+10*stage_now:
						if bul[0]<=scg_pos[count][0]:
							if scg_pos[count][0]-bul[0]<abul_side:
								hit_sound.play()
								scg_pos.remove(scg_pos[count])
								scg_side.remove(scg_side[count])
								abul_pos.remove(bul)
								break
						else:
							if bul[0]-scg_pos[count][0]<scg_side[count]:
								hit_sound.play()
								scg_pos.remove(scg_pos[count])
								scg_side.remove(scg_side[count])
								abul_pos.remove(bul)
								break
					count+=1

		#check if the plane eats the item
		for b in ordi_pos:
			if a_cpos[0]-a_hori1-(a_thick/2)<b[0] and a_cpos[0]+a_hori1+(a_thick/2)>b[0]:
				if b[1]-stage_now*10<a_cpos[1]+a_vert2 and b[1]>a_cpos[1]:
					ordi_pos.remove(b)
					fire_sound.play()
					choice=randint(1,100)
					if choice==49 or choice==50 or choice==51:
						#increase maximum health         49,50,51
						ahealth_max+=1
						ahealth+=1
					elif choice==100 or choice==99 or choice==98:
						#invincible for 6 secs           100,99,98
						ainvi=True
						ainvi_start=now_time
					elif choice==1 or choice==11 or choice==21 or choice==31 or choice==41:
						#increse moving speed            1,11,21,31,41
						a_speed=a_speed*1.1
					elif choice>1 and choice<=33:
						#restore health by 1             1-33
						if ahealth<ahealth_max:
							ahealth+=1
					elif choice>=34 and choice<=68:
						#faster bullet speed             34-68
						abul_speed+=2
					else:
						#reduces bullet firing interval  69-100
						a_cd-=20

		#Draw all the elements
		screen.fill((0,0,0))

		#Draw the background
		for b in bg_pos:
			screen.set_at((b[0],b[1]),(255,255,255))

		#Draw Player's plane
		if ainvi==True:
			a_color=pygame.Color(255,0,255)
		else:
			a_color=pygame.Color(249,175,47)
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_thick/2),a_cpos[1]-a_vert1,a_thick,a_vert1))
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-a_hori1-(a_thick/2),a_cpos[1],a_hori1,a_thick))
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]+(a_thick/2),a_cpos[1],a_hori1,a_thick))
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-(a_thick/2),a_cpos[1],a_thick,a_vert2+a_thick))
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]-a_hori2-(a_thick/2),a_cpos[1]+a_vert2,a_hori2,a_thick))
		pygame.draw.rect(screen,a_color,pygame.Rect(a_cpos[0]+(a_thick/2),a_cpos[1]+a_vert2,a_hori2,a_thick))

        #Draw Player's bullets
		for bul in abul_pos:
			pygame.draw.rect(screen,abul_color,pygame.Rect(bul[0],bul[1],abul_side,abul_side))

		#Draw items
		#draw green
		count=0
		while count<len(scg_pos):
			if scg_pos[count][1]+scg_side[count]>640:
				pygame.draw.rect(screen,scg_color,pygame.Rect(scg_pos[count][0],scg_pos[count][1],scg_side[count],640-scg_pos[count][1]))
			else:
				pygame.draw.rect(screen,scg_color,pygame.Rect(scg_pos[count][0],scg_pos[count][1],scg_side[count],scg_side[count]))
			count+=1

		#draw blue
		count=0
		while count<len(ordi_pos):
			if ordi_pos[count][1]+ordi_side>640:
				pygame.draw.rect(screen,ordi_color,pygame.Rect(ordi_pos[count][0],ordi_pos[count][1],ordi_side,640-ordi_side))
			else:
				pygame.draw.rect(screen,ordi_color,pygame.Rect(ordi_pos[count][0],ordi_pos[count][1],ordi_side,ordi_side))
			count+=1

		#draw red
		count=0
		while count<len(dang_pos):
			if dang_pos[count][1]+dang_side[count]>640:
				pygame.draw.rect(screen,dang_color,pygame.Rect(dang_pos[count][0],dang_pos[count][1],dang_side[count],640-dang_pos[count][1]))
			else:
				pygame.draw.rect(screen,dang_color,pygame.Rect(dang_pos[count][0],dang_pos[count][1],dang_side[count],10))
			count+=1

		#Draw score
		PrintLife(ahealth,0,False)

		pygame.display.update()

GameIns()
