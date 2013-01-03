
from physics import *

class Info(PhysicsObject, DisplaySprite):
	def __init__(self, image=0, pos=(0,0), t1=20*40, t2=40*40):
		PhysicsObject.__init__(self)
		DisplaySprite.__init__(self, "info.bmp")
		
		self.frame = image
		
		self.d[:] = pos
		self.v[1] = -.05
		self.a[1] = 0
		self.count = 0
		
		self.t1 = t1
		self.t2 = t2
		
		PhysicsObject.update(self, 0)
	
	def impulse(self, p):
		pass
	
	def update(self, t):
		if self.count > self.t2:
			self.kill()
			return
		elif self.count > self.t1:
			self.v[1] = 0
		PhysicsObject.update(self, t)

