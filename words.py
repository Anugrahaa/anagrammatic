import sys, pygame
from pygame.locals import *
import random
from random import shuffle
import time
import enchant

class Anagrammattic(object):
	def __init__(self):
		self.score = 0
		self.WORD = "words"
		self.d = enchant.Dict("en_US")
		self.score = {"A":1, "B":3, "C":3, "D":2, "E":1, "F":4, "G":2, "H":4, "I":1, "J":8, "K":5, "L":1, "M":3, "N":1, "O":1, "P":3, "Q":10, "R":1, "S":1, "T":1, "U":1, "V":4, "W":4, "X":8, "Y":4, "Z":1}
		self.listOfWords = []
		self.noOfWords = 0
		for i in range(30):
			self.listOfWords.append("xxxxx")

	def getRandomFiveLetterWord(self,e):
		self.WORD = random.choice(open(e, encoding = "latin-1").readlines()).rstrip()
		return self.WORD

	def jumbleItUp(self):
		word = list(self.WORD)
		shuffle(word)
		newword = ''.join(word)
		return newword

	def checkword(self, word):
		rightword = self.WORD
		i=0
		word = word.replace(" ","")
		print(word)
		while i<len(word):
			if word[i] not in rightword:
				return False
			i+=1
		return True

	def checkcorrectness(self,word):
		score = 0
		word = word.replace(" ","")
		x = self.d.check(word)
		if x==True:
			if word not in self.listOfWords:
				i=0
				while i<len(word):
					score+=self.score[word[i].upper()]
					i+=1
		if score!=0:
			self.listOfWords[self.noOfWords] = word
		return score


