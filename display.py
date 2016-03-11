import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
black = 0,0,0
white = 255,255,255
class ViewScreen(object):
	def displayScreenBasics(self):
		pygame.init()
		size = width, height = 640,480
		screen = pygame.display.set_mode(size)
		screenrect = screen.get_rect()
		return screen
		

	def displayText(self,screen,worrd,jumbledword):
		basicfont = pygame.font.SysFont(None, 48)
		text1 = basicfont.render(worrd, True, white, black)
		text1rect = text1.get_rect()
		text1rect.x = 10
		text1rect.y = 10
		screen.blit(text1, text1rect)
		text1 = basicfont.render(jumbledword, True, black, white)
		text1rect = text1.get_rect()
		text1rect.x = 100
		text1rect.y = 100
		screen.blit(text1, text1rect)
		pygame.display.flip()
		return

	def ScreenClose(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
		return