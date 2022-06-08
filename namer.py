import pygame as pg

class Namer:
	def __init__(self, input_surface, input_width, input_height ):
		self.screen = input_surface
		self.dimX = input_width
		self.dimY = input_height
		self.complete = False
		# temporary place holder
		self.img = pg.image.load('assets/greeter.png')
		self.img_rect = self.img.get_rect(center = self.screen.get_rect().center)

	def draw(self):
		# draw black screen
		self.screen.fill((0,0,0))
		self.screen.blit(self.img,  self.img_rect )
		# update
		pg.display.flip() 
		self.complete = True		
		


