#!/usr/bin/env python

#
#      This program is free software; you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation; either version 2 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program; if not, write to the Free Software
#      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import sys, os
import pygame
from pygame.locals import *
if not pygame.mixer: print 'Warning, sound disabled'

from image import *
from sprite import *
from background import *
from player import *
from enemy import *
from candy import *

def loadSound(name):
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound()
	fullname = os.path.join('sfx', name)
	try:
		sound = pygame.mixer.Sound(fullname)
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return sound

class Screen(PhysicsObject):
	def __init__(self):
		PhysicsObject.__init__(self, ground=False)
		Sprite.__init__(self)
		#self.count = 0
		self.rect = pygame.rect.Rect(0, 0, 640, 480)
		self.a[1] = 0
		self.kill()
	
	def update(self, screenx):
		self.d[0] = (Player.player.d[0] - 160)
		PhysicsObject.update(self, screenx)

class gameWorld ( object ):
	def __init__(self):
		#Initialize Everything
		pygame.init()
		
		pygame.display.set_mode((640, 480))
		pygame.display.set_icon(loadImage("icon.bmp", True))
		
		pygame.display.set_caption('Muffins')
		pygame.mouse.set_visible(0)
		
		#Create The Backgound
		self.background = Background("back.bmp")
		
		self.screenx = 0
		self.screen = Screen()
		
		Player()
		
		for x in xrange(100, 600, 30):
			Muncher((x,0))
		
		for x in xrange(115, 600, 30):
			Health((x,180), (x/30)%2)
		
		for y in xrange(0, 900, 30):
			Cruncher((-100*((y/30)%210),y%210))
		
		self.stats = Stats()
		
		#Prepare Game Objects
		self.clock = pygame.time.Clock()
	
	def start(self):
		while 1:
			keys = pygame.key.get_pressed()
			
			if Player.player.onGround():
				Player.player.v[0] = 0
				if keys[K_SPACE] or keys[K_UP]:
					Player.player.bounce()
			
			if keys[K_RIGHT]:
				Player.player.v[0] = max(Player.player.v[0], 0.1)
			if keys[K_LEFT]:
				Player.player.v[0] = min(Player.player.v[0], -0.1)
			
			
			#Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
					raise SystemExit
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						raise SystemExit
				elif event.type == KEYUP:
					if event.key == K_SPACE or event.key == K_UP:
						Player.player.v[1] = max(-0.1, Player.player.v[1])
			
			#find all sprites that are onscreen
			screensprites = pygame.sprite.spritecollide(self.screen, Sprite.group, False)
			
			Sprite.group.update(1000.0/40.0)
			self.screen.update(1000.0/40.0)
			
			#Draw Everything
			pygame.display.get_surface().blit(self.background, (-(self.screen.d[0]*2 % 640), 0))
			
			for sprite in screensprites:
				sprite.draw(self.screen.d[0]*2)
			
			Player.player.draw(self.screen.d[0]*2)
			self.stats.draw()
			
			pygame.display.flip()
			
			self.clock.tick(40)

def main():
	gameWorld().start()

if __name__ == "__main__":
	if 1:
		try:
			import psyco
			psyco.full()
		except ImportError:
			pass
		main()
	else:
		#Profile
		import hotshot
		import hotshot.stats
		prof = hotshot.Profile("hotshot_stats")
		try:
			prof.runcall(main)
		except SystemExit:
			pass
		prof.close()
		hotshot.stats.load("hotshot_stats").sort_stats("time").print_stats()


