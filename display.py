import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
black = 0,0,0
white = 255,255,255
class ViewScreen(object):
	def __init__(self):
		pygame.init()
		self.size = self.width, self.height = 640,480
		self.screen = pygame.display.set_mode(self.size)
		self.screenrect = self.screen.get_rect()	
		self.font = pygame.font.SysFont("TimesNewRoman", 60)
		self.text = [self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black)]
		self.textrect = [self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect()]
		self.anagrammatic = Anagrammattic()
		self.clear = pygame.image.load("./images/backspace.png")
		self.clearrect = self.clear.get_rect()

	def displayText(self,jumbledword):
		i=0		
		while i<len(jumbledword):
			# self.text[i] = self.font.render(jumbledword[i], True, white, black)
			text = "./letters/"+jumbledword[i].upper()+".png"
			self.text[i] = pygame.image.load(text)
			self.text[i] = pygame.transform.scale(self.text[i], (75,75))
			self.textrect[i] = self.text[i].get_rect()
			self.textrect[i].x = 150+(85*i)
			self.textrect[i].y = 100
			self.screen.blit(self.text[i], self.textrect[i])
			i+=1
		i=0
		while i<len(jumbledword):
			blank = pygame.image.load("./images/line.jpg")
			blank = pygame.transform.scale(blank, (65,100))
			blankrect = blank.get_rect()
			blankrect.x = 150+(85*i)
			blankrect.y = 250
			self.screen.blit(blank, blankrect)
			i+=1
		self.clear = pygame.image.load("./images/backspace.png")
		self.clear = pygame.transform.scale(self.clear, (50,50))
		self.clearrect = self.clear.get_rect()
		self.clearrect.x = 150+(85*i)
		self.clearrect.y = 250
		self.screen.blit(self.clear,self.clearrect)

		tick = pygame.image.load("./images/tick.png")
		tick = pygame.transform.scale(tick, (100,50))
		tickrect = tick.get_rect()
		tickrect.x = 150
		tickrect.y = 350
		self.screen.blit(tick,tickrect)

		pygame.display.flip()
		return self.screen.blit(self.text[0], self.textrect[0])

	def displayAnsText(self, text):
		i=0
		text = text.replace(" ","")
		while i<len(text):
			clearsurface = pygame.Surface((65,100))
			clearsurface.fill(black)
			clearsurfaceRect = clearsurface.get_rect()
			clearsurfaceRect.x = 150+(85*i)
			clearsurfaceRect.y = 250
			self.screen.blit(clearsurface, clearsurfaceRect)
			newtext = "./letters/"+text[i].upper()+".png"
			# letter = self.font.render(text[i], True, white, black)
			letter = pygame.image.load(newtext)
			letter = pygame.transform.scale(letter, (65,65))
			letterrect = letter.get_rect()
			letterrect.x = 150+(85*i)
			letterrect.y = 250
			self.screen.blit(letter, letterrect)
			i+=1
		pygame.display.flip()

	def Timer(self,timetext):
		time = self.font.render(timetext, True, white, black)
		timerect = time.get_rect()
		timerect.x = 150+(85*4)
		timerect.y = 350
		self.screen.blit(time, timerect)
		pygame.display.flip()

	def clearScreen(self, jumbledword,tick):
		self.screen.fill(black)
		if tick==True:
			image = "./images/tick.png"
		else:
			image = "./images/wrong.png"

		shape = pygame.image.load(image)
		shape = pygame.transform.scale(shape,(100,100))
		shaperect = shape.get_rect()
		shaperect.x = 100
		shaperect.y = 100
		self.screen.blit(shape, shaperect)
		pygame.display.flip()
		pygame.time.wait(1000)
		self.screen.fill(black)
		self.displayText(jumbledword)

	def detectMouseClick(self, text, i, jumbledword, pos,checkword):
		j=0
		if i<5:
			while j<5:
				if self.textrect[j].collidepoint(pos):
					text = text.replace(text[i], jumbledword[j], 1)
					value = checkword(text)
					print(value,j)
					if value != False:
						self.displayAnsText(text)
						print(text,self.anagrammatic.checkcorrectness(text))
						return text
					else:
						text = text.replace(text[i], " ", 1)
						return False
				else:
					j+=1
		if self.clearrect.collidepoint(pos):
			return -1
		return False

	def ScreenClose(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()