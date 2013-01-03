
import random

from sprite import *
from vector import *

class PhysicsObject(Sprite):
	def __init__(self, pos=(0,0), mass=0, ground=True):
		self.mass = mass
		self.d = Vector()
		self.v = Vector()
		self.a = Vector()

		self.d[:] = pos

		self.ground = ground

		self.a[1] = 0.0005

		self.direction = 0

	def onGround(self):
		#return self.d[1]+(self.rect[3]/2) >= 208 and self.ground
		#print (self.rect[3]/2), 16
		return self.ground and self.d[1]+(self.rect[3]/2) >= 208

	def impulse(self, p):
		if p.mag() > 0.3:
			self.damage()
			if p.mag() > 0.5:
				self.v += Vector(0.5, p.heading())
			else:
				self.v += p
		else:
			self.v += p

	def damage(self):
		pass

	def update(self, t):
		Sprite.update(self, t)
		self.d += self.v*t + (self.a * t*t) *  0.5
		self.v += self.a*t

		#cap speed
		#if self.v[0] > 0.05:
		#	self.v[0] = 0.05
		#elif self.v[0] < -0.05:
		#	self.v[0] = -0.05

		#determine direction
		if self.v[0] < 0:
			self.direction = 1
		elif self.v[0] > 0:
			self.direction = 0

		#ground
		if self.onGround():
			self.d[1] = 208-(self.rect[3]/2)
			self.v[0] = 0
			self.v[1] = 0

		self.rect = pygame.Rect(int(self.d[0])*2, int(self.d[1])*2, self.rect[2], self.rect[3])

