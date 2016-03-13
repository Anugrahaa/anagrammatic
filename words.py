import sys, pygame
from pygame.locals import *
import random
from random import shuffle
import time
import enchant

class Anagrammattic(object):
	def __init__(self):
		self.score = 0
		self.d = enchant.Dict("en_US")
		self.score = {"A":1, "B":3, "C":3, "D":2, "E":1, "F":4, "G":2, "H":4, "I":1, "J":8, "K":5, "L":1, "M":3, "N":1, "O":1, "P":3, "Q":10, "R":1, "S":1, "T":1, "U":1, "V":4, "W":4, "X":8, "Y":4, "Z":1}
		
		self.noOfWords = 0
	

	def getRandomFiveLetterWord(self,e):
		word = random.choice(open(e).readlines()).rstrip()
		return word

	def jumbleItUp(self,word):
		word = list(word)
		shuffle(word)
		newword = ''.join(word)
		return newword

	def checkword(self, word, jumbledword):
		rightword = jumbledword
		i=0
		word = word.replace(" ","")
		while i<len(word):
			j=0
			flag=False
			while j<len(rightword)-i:
				if(word[i]==rightword[j]):
					rightword = rightword.replace(rightword[j], rightword[len(rightword)-i-1],1)
					flag=True
					break
				else:
					flag=False
				j+=1
			if(flag==False):
				return False
		# while i<len(word):
		# 	if word[i] not in rightword:
		# 		return False
			i+=1
		return True

	def checkcorrectness(self,word,listOfWords):
		score = 0
		word = word.replace(" ","")
		if(len(word)):
			x = self.d.check(word)
		else:
			return 0
		if x==True:
			if word not in listOfWords:
				i=0
				while i<len(word):
					score+=self.score[word[i].upper()]
					i+=1
		
		return score

	def gethint(self, hintno, word):
		if hintno == 1:
			return "_ _ "+word[2]+" _ _"
		elif hintno == 2:
			return "_ _ "+word[2]+" "+word[3]+" _"
		else:
			return word[0]+" _ "+word[2]+" "+word[3]+" _ :"+"No more hints!"



