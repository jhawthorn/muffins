
import pygame
from pygame.locals import *

from image import *

class Background(pygame.Surface):
	def __init__(self, filename):
		tmp = loadImage("back.bmp")
		
		pygame.Surface.__init__(self, (tmp.get_width()*2, tmp.get_height()))
		
		self.blit(tmp, (0, 0))
		self.blit(tmp, (tmp.get_width(), 0))
