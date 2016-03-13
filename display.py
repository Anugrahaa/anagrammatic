import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
# import inputbox
black = 0,0,0
white = 255,255,255
class ViewScreen(object):
	def __init__(self):
		pygame.init()
		self.size = self.width, self.height = 640,480
		self.screen = pygame.display.set_mode(self.size)
		self.screenrect = self.screen.get_rect()	
		self.font = pygame.font.SysFont("TimesNewRoman", 60)
		self.scorefont = pygame.font.SysFont("TimesNewRoman", 30)
		self.text = [self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black),self.font.render("abcde", True, white, black)]
		self.textrect = [self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect(),self.text[0].get_rect()]
		self.anagrammatic = Anagrammattic()
		self.clear = pygame.image.load("./images/backspace.png")
		self.clearrect = self.clear.get_rect()
		self.hintrect = self.clear.get_rect()

	def firstScreen(self):
		self.screen.fill(black)
		text = "Enter your name: "
		text = self.scorefont.render(text, True, white, black)
		textrect = text.get_rect()
		textrect.x = 20
		textrect.y = 200
		self.screen.blit(text, textrect)
		pygame.display.flip()

	def playerName(self,name):
		self.screen.fill(black)
		self.firstScreen()
		text1 = ''.join(name)
		text = self.scorefont.render(text1, True, white, black)
		self.screen.blit(text, (250,200))
		pygame.display.flip()
		return text1

	def displayText(self,player,jumbledword, totalscore):
		i=0		
		while i<len(jumbledword):
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

		score = self.scorefont.render(totalscore, True, white, black)
		scorerect = score.get_rect()
		scorerect.x = 150+(85*3)
		scorerect.y = 25
		self.screen.blit(score, scorerect)

		hint = pygame.image.load("./images/hint.png")
		hint = pygame.transform.scale(hint,(50,50))
		self.hintrect = hint.get_rect()
		self.hintrect.x = 150+(85*2)
		self.hintrect.y = 350
		self.screen.blit(hint, self.hintrect)

		player = "Welcome " + player
		player = self.scorefont.render(player, True, white, black)
		self.screen.blit(player, (15,25))

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

	def clearScreen(self, player, jumbledword, tick, totalscore):
		if tick!=0:
			image = "./images/right.png"
		else:
			image = "./images/wrong.png"
		shape = pygame.image.load(image)
		shape = pygame.transform.scale(shape,(100,50))
		shaperect = shape.get_rect()
		shaperect.x = 150	
		shaperect.y = 350
		self.screen.blit(shape, shaperect)
		pygame.display.flip()
		pygame.time.wait(1000)
		self.screen.fill(black)
		self.displayText(player, jumbledword, totalscore)

	def displayHint(self,hintword):
		clearsurface = pygame.Surface((100,40))
		clearsurface.fill(black)
		clearsurfaceRect = clearsurface.get_rect()
		clearsurfaceRect.x = 100
		clearsurfaceRect.y = 420
		self.screen.blit(clearsurface,clearsurfaceRect)

		hintword = "Hint: "+hintword
		hintword = self.scorefont.render(hintword, True, white, black)
		self.screen.blit(hintword, (100,420))
		pygame.display.flip()

	def detectMouseClick(self, text, i, jumbledword, pos,checkword):
		j=0
		if i<5:
			while j<5:
				if self.textrect[j].collidepoint(pos):
					text = text.replace(text[i], jumbledword[j], 1)
					value = checkword(text, jumbledword)
					if value != False:
						self.displayAnsText(text)
						return text
					else:
						text = text.replace(text[i], " ", 1)
						return False
				else:
					j+=1
		if self.clearrect.collidepoint(pos):
			return -1
		if self.hintrect.collidepoint(pos):
			return -2
		return False

	def printScore(self, scoretext, levelup):
		self.screen.fill(black)
		score = self.font.render(scoretext, True, (255,200,100), black)
		scorerect = score.get_rect()
		scorerect.x = 50
		scorerect.y = 100
		self.screen.blit(score, scorerect)
		if levelup:
			scoretext="Next Round"
		else:
			scoretext="Thank You For Playing"
		score = self.font.render(scoretext, True, (255,200,100), black)
		scorerect = score.get_rect()
		scorerect.x = 50
		scorerect.y = 200
		self.screen.blit(score, scorerect)
		if levelup:
			scoretext=""
		else:
			scoretext="Bye"
		score = self.font.render(scoretext, True, (255,200,100), black)
		scorerect = score.get_rect()
		scorerect.x = 50
		scorerect.y = 300
		self.screen.blit(score, scorerect)
		pygame.display.flip()