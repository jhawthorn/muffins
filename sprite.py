
import random

import pygame
from pygame.locals import *

from image import *
from vector import *

class Group(pygame.sprite.Group):
	def draw(self, *args):
		for sprite in self.sprites():
			sprite.draw(*args)

class Frames(object):
	def __init__(self, filename, tilesize):
		self.image = loadImage(filename, True)
		colorkey = self.image.get_colorkey()
		
		self.frames = []
		
		for y in xrange(0, self.image.get_height(), tilesize):
			for x in xrange(0, self.image.get_width(), tilesize):
				tmp = pygame.Surface((tilesize, tilesize)).convert()
				tmp.set_colorkey(colorkey)
				tmp.fill((colorkey))
				tmp.blit(self.image, (0,0), (x,y,tilesize,tilesize))
				
				self.frames.append(tmp)
	
	def __getitem__(self, item):
		return self.frames[item]

class Sprite(pygame.sprite.Sprite):
	group = Group()
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(0,0,0,0)
		Sprite.group.add(self)
		
		self.count = random.randint(0, 1000)
	
	def collide(self, sprite):
		return self.rect.colliderect(sprite.rect)
	
	def update(self, t):
		self.count += int(t)
	
	def draw(self, screenx):
		pass
	

class DisplaySprite(Sprite):
	def __init__(self, filename, tilesize=32):
		Sprite.__init__(self)
		self.frames = Frames(filename, tilesize)
		
		self.hitmask = None
		try:
			self.hitmask = pygame.surfarray.array_colorkey(self.frames[0])
		except:
			pass
		
		self.frames[0].unlock()
		self.frames[0].unlock()
		
		self.frame = 0
		self.rect = pygame.Rect(0,0, tilesize, tilesize)
		
	
	def collide(self, sprite):
		if not Sprite.collide(self, sprite):
			return False
		
		if not self.hitmask or not sprite.hitmask:
			return True
		
		rect1, rect2 = self.rect, sprite.rect
		
		rect = rect1.clip(rect2)
		x1, y1, x2, y2 = rect.x-rect1.x, rect.y-rect1.y, rect.x-rect2.x, rect.y-rect2.y
		
		for y in range(rect.height):
			for x in range(rect.width):
				if self.hitmask[x1+x][y1+y] and sprite.hitmask[x2+x][y2+y]:
					return True
		return False
	
	def draw(self, screenx):
		pygame.display.get_surface().blit(self.frames[self.frame], (self.rect[0]-screenx, self.rect[1]))


