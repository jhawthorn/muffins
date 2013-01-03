
import math

from player import *
from physics import *
from bullet import *

class Enemy(PhysicsObject, DisplaySprite):
	group = Group()
	def __init__(self, filename, pos=(0,0)):
		PhysicsObject.__init__(self)
		DisplaySprite.__init__(self, filename)
		self.add(Enemy.group)
		
		self.direction = 0
		
		self.d[:] = pos
		
		PhysicsObject.update(self, 0)
	
	def damage(self):
		PatrticleExplosion(self.d[:], 3, (255,0,0))
		self.kill()
	
	def update(self, t):
		PhysicsObject.update(self, t)
		
		if self.collide(Player.player):
			if abs((Player.player.d - self.d).heading()-(pi/2.0)) > 2:
				if Player.player.v[1] > 0:
					self.damage()
					Player.player.bounce()
			else:
				Player.player.damage()
		

class Muncher(Enemy):
	def __init__(self, pos=(0,0)):
		Enemy.__init__(self, "muncher.bmp", pos)
		PhysicsObject.update(self, 0)
		
	def update(self, t):
		if self.onGround() and (Player.player.d-self.d).mag() < 100 and not Player.player.invincibility:
			try:
				self.v = Vector(3/(Player.player.d-self.d).mag(), (Player.player.d-self.d).heading())
				if self.v[0] > 0:
					self.v[0] = min(self.v[0], 0.1)
				elif self.v[0] < 0:
					self.v[0] = max(self.v[0], -0.1)
				self.v[1] = 0
			except ZeroDivisionError:
				pass
		else:
			if self.v[0] > 0:
				self.v[0] = min(self.v[0], 0.025)
			elif self.v[0] < 0:
				self.v[0] = max(self.v[0], -0.025)
		
		if (Player.player.d - self.d).mag() < 50 and not Player.player.invincibility:
			self.frame = (self.count/40/8) % 2 + 4
		else:
			self.frame = (self.count/40/16) % 2
		
		if self.direction:
			self.frame += 2
		
		Enemy.update(self, t)

class Cruncher(Enemy):
	def __init__(self, pos=(0,0)):
		Enemy.__init__(self, "cruncher.bmp", pos)
		PhysicsObject.__init__(self, pos, ground=False)
		self.a[1] = 0
		
		self.count = 0
		self.droptime = 0
		
		PhysicsObject.update(self, 0)
		
	
	def drop(self):
		if not self.droptime:
			self.droptime = 50*25
	
	def update(self, t):
		self.v[0] = .05
		self.v[1] = math.sin(self.count / 40 / 15)/30.0
		Enemy.update(self, t)
		
		self.frame = (self.count/40/8) % 2
		if self.direction:
			self.frame += 2
		
		if self.droptime:
			self.droptime -= t
			self.frame += 4
			if not self.droptime:
				Bomb("crunchbomb.bmp", self.d[:])
		
		if -100 < (Player.player.d[0] - self.d[0])/self.v[0] - 50*25 < 100:
			self.drop()
		
		
		
