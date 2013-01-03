
import random

from player import *
from physics import *

def frange(start, stop=None, step=None):
	"""Like xrange(), but returns list of floats instead

	All numbers are generated on-demand using generators
	"""

	if stop is None:
		stop = float(start)
		start = 0.0

	if step is None:
		step = 1.0

	cur = float(start)

	while cur < stop:
		yield cur
		cur += step


class Patrticle(PhysicsObject):
	def __init__(self, pos, v, colour=(0,0,0)):
		PhysicsObject.__init__(self)
		Sprite.__init__(self)
		
		self.rect = pygame.Rect(0,0,2,2)
		
		self.colour = colour
		
		self.d[:] = pos
		self.v = v
	
	def draw(self, screenx):
		pygame.display.get_surface().fill(self.colour, pygame.Rect(self.rect[0]-screenx, self.rect[1], 2, 2))
	
	def update(self, t):
		PhysicsObject.update(self, t)
		
		if(self.onGround()):
			self.kill()

class PatrticleExplosion(object):
	def __init__(self, pos=(0,0), mag=10.0, colour=(0,0,0)):
		for h in frange(-3, 1, 0.25/mag):
			v = random.randint(10,30) * .001 * mag
			Patrticle(pos, Vector(v, h), colour)

class Explosion(Sprite):
	def __init__(self, pos=(0,0), mag=10.0):
		dist = 10*10
		d = Vector()
		d[:] = pos
		d[1] += 4
		
		self.rect = pygame.rect.Rect((pos[0]-dist)*2, (pos[1]-dist)*2, dist*4, dist*4)
		
		for sprite in pygame.sprite.spritecollide(self, Sprite.group, False):
			dist = sprite.d - d
			sprite.impulse(Vector(20/dist.mag(), dist.heading()))
		
		PatrticleExplosion(d, mag)
		
		#for h in frange(-3, 1, .05):
		#	v = random.randint(10,30) * .01
		#	Patrticle(d[:], Vector(v, h))


class Bomb(PhysicsObject, DisplaySprite):
	def __init__(self, filename, pos=(0,0)):
		DisplaySprite.__init__(self, filename)
		PhysicsObject.__init__(self, pos)
		PhysicsObject.update(self, 0)
	
	def update(self, t):
		PhysicsObject.update(self, t)
		
		if self.onGround():
			self.kill()
			Explosion(self.d[:])
