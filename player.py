
import random

from physics import *
from info import *

import pygame
from pygame.locals import *

class Stats:
	def __init__(self):
		self.font = pygame.font.Font("gfx/visitor2.ttf", 28)
		self.image = [None, None]
	
	def getImage(self, string):
		if self.image[0] != string:
			self.image[0] = string
			try:
				tmp = self.font.render(string, False, (0,0,0))
			except pygame.error:
				#some versions of SDL_ttf
				tmp = self.font.render(string, True, (0,0,0))
			self.image[1] = pygame.transform.scale(tmp, (tmp.get_width()*2, tmp.get_height()*2))
		return self.image[1]
	
	def draw(self):
		string = "".join(("HP: ", str(Player.player.hp)))
		pygame.display.get_surface().blit(self.getImage(string), (0,0))

class Player (PhysicsObject, DisplaySprite) :
	player = None
	group = Group()
	def __init__(self):
		PhysicsObject.__init__(self, (0, 192))
		DisplaySprite.__init__(self, "player.bmp")
		
		self.add(Player.group)
		self.hp = 5
		self.inventory = []
		self.primary = None
		self.secondary = None
		
		self.state = 0
		
		self.invincibility = 0
		
		Player.player = self
		
		PhysicsObject.update(self, 0)
		
	def changeState(self, state):
		"""
		Changes the player's state:
		
		0: chilling
		1: walking
		2: primarying
		3: secondarying
		4: somethingelseing?
		5...
		"""
		
		self.state = state
		self.count = 0
		
	def equip(self, thing, prim=True):
		if thing in self.inventory:
			if prim:
				self.primary = thing
			else:
				self.secondary = thing
	
	def damage(self):
		if not self.invincibility:
			self.hp -= 1
			self.invincibility = 75
			Info(random.randint(2,5), self.d[:], 10*25, 20*25)
	
	def bounce(self):
		keys = pygame.key.get_pressed()
		if keys[K_SPACE] or keys[K_UP]:
			self.v[1] = -0.237
		else:
			self.v[1] = -0.15
	
	def update(self, t):
		PhysicsObject.update(self, t)
		
		if self.invincibility:
			self.invincibility -= 1
		
		frame = 0
		
		if not self.v[1]:
			frame += 4
			if self.v[0] != 0:
				frame += (self.count/25/10 % 2)*2
		
		frame += self.direction
		
		self.frame = frame
	
	def draw(self, screenx):
		if self.invincibility:
			if (self.count/25/6 % 2):
				self.frame = 0
				return
		DisplaySprite.draw(self, screenx)


