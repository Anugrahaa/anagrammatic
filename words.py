import sys, pygame
from pygame.locals import *
import random
import time
import enchant

class Anagrammattic(object):
	def getRandomFiveLetterWord(self,e):
		randomWord = random.choice(open(e, encoding = "latin-1").readlines()).rstrip()
		return randomWord

	def jumbleItUp(self,worrd):
		i=0
		j = random.sample(range(len(worrd)),len(worrd))
		newword = "xxxxx"
		while i < len(worrd):
			newword = newword.replace(newword[i],worrd[j[i]],1)
			i+=1
		return newword