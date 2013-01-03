
from math import cos, sin, atan, hypot, pi

def direction(x, y):
    """Return the direction component of a vector (in radians), given
    cartesian coordinates.
    """
    if x > 0:
        if y >= 0:
            return atan(y / x)
        else:
            return atan(y / x) + pi*2
    elif x == 0:
        if y > 0:
            return pi*.5
        elif y == 0:
            return 0
        else:
            return pi*1.5
    else:
        return atan(y / x) +pi

class Vector(object):
	def __init__(self, mag = 0.0, f = 0.0):
		if mag and f:
			mag = float(mag)
			f = float(f)
			self.components = [mag * cos(f), mag * sin(f)]
		else:
			self.components = [0.0, 0.0]
	
	def heading(self):
		return direction(self.components[0], self.components[1])
	
	def mag(self):
		return hypot(self.components[0], self.components[1])
	
	def __getitem__(self, item):
		return self.components[item]
	
	def __setitem__(self, item, val):
		self.components[item] = val
	
	def __iadd__(self, a):
		self.components[0] += a.components[0]
		self.components[1] += a.components[1]
		return self
	
	def __add__(self, a):
		v = Vector()
		v[:] = self.components[0]+a.components[0], self.components[1]+a.components[1]
		return v
	
	def __sub__(self, a):
		v = Vector()
		v[:] = self.components[0]-a.components[0], self.components[1]-a.components[1]
		return v
	
	def __mul__(self, a):
		v = Vector()
		v[:] = self.components[0] * a, self.components[1] * a
		return v
	
	def __imul__(self, a):
		self.components[0] *= a
		self.components[1] *= a
		return self
	
	def __repr__(self):
		return '<Vector(%s, %s)>' % (self.mag(), self.heading())
