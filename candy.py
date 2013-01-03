
from player import *
from physics import *
from info import *

class Candy(PhysicsObject):
	def __init__(self):
		PhysicsObject.__init__(self)

class Health(Candy, DisplaySprite):
	def __init__(self, pos=(0,0), single=True):
		Candy.__init__(self)
		if single:
			DisplaySprite.__init__(self, "health1.bmp")
		else:
			DisplaySprite.__init__(self, "health5.bmp")

		self.d[:] = pos

		self.amount = 1 if single else 5
		self.icon = 0 if single else 1

		PhysicsObject.update(self, 0)

	def update(self, t):
		PhysicsObject.update(self, t)

		a = (self.count/25/5)%10
		if a <= 3:
			self.frame = a
		else:
			self.frame = 0


		if self.collide(Player.player):
			Player.player.hp += self.amount
			Info(self.icon, (self.d[0], self.d[1]-10))
			self.kill()

