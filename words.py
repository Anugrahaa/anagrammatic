import sys, pygame
from pygame.locals import *
import random
import time
import enchant

class Anagrammattic(object):
	def __init__(self):
		self.score = 0
		self.WORD = "words"
		self.d = enchant.Dict("en_US")
		self.score = {"A":1, "B":3, "C":3, "D":2, "E":1, "F":4, "G":2, "H":4, "I":1, "J":8, "K":5, "L":1, "M":3, "N":1, "O":1, "P":3, "Q":10, "R":1, "S":1, "T":1, "U":1, "V":4, "W":4, "X":8, "Y":4, "Z":1}
	def getRandomFiveLetterWord(self,e):
		self.WORD = random.choice(open(e, encoding = "latin-1").readlines()).rstrip()
		return self.WORD

	def jumbleItUp(self):
		i=0
		j = random.sample(range(len(self.WORD)),len(self.WORD))
		newword = "xxxxx"
		while i < len(self.WORD):
			newword = newword.replace(newword[i],self.WORD[j[i]],1)
			i+=1
		return newword

	def checkword(self, word):
		rightword = self.WORD
		i=0
		word = word.replace(" ","")
		print(word,"l")
		print(rightword)
		while i<len(word):
			j=0
			flag=False
			while j<len(rightword)-i:
				if(word[i]==rightword[j]):
					rightword = rightword.replace(rightword[j], rightword[len(rightword)-i-1],1)
					flag=True
					print(rightword)
					break
				else:
					flag=False
				j+=1
			if(flag==False):
				return False
			i+=1
		return True

	def checkcorrectness(self,word):
		score = 0
		word = word.replace(" ","")
		x = self.d.check(word)
		if x==True:
			i=0
			while i<len(word):
				score+=self.score[word[i].upper()]
				i+=1
			print(score)
		return x


