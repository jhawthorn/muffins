
import os

import pygame
from pygame.locals import *




def _loadImage(name, colorkey=None):
	fullname = os.path.join('gfx', name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
	image = image.convert()
	if colorkey is not None:
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image

def loadImage(name, colorkey=None):
	return _loadImage(name, colorkey)
