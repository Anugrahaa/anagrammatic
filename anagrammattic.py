import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
from display import ViewScreen

def main():
	d = enchant.Dict("en_US")
	anagrammattic = Anagrammattic()

	jumbledword = word = anagrammattic.getRandomFiveLetterWord("fiveLetterWords.txt")

	while(d.check(jumbledword)==True):
		jumbledword = anagrammattic.jumbleItUp()

	gameScreen = ViewScreen()
	b = gameScreen.displayText(jumbledword)
	pygame.time.wait(1000)
	chk = True
	enteredWord = "     "
	i=0
	clock = pygame.time.Clock()
	minutes = 0
	seconds = 0
	milliseconds = 0
	while chk:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.QUIT:
				if event.type == pygame.QUIT:
					chk = False
				else:
					pos = pygame.mouse.get_pos()
					value = gameScreen.detectMouseClick(enteredWord,i,jumbledword,pos,anagrammattic.checkword)
					if value!=False:
						if value!=-1:
							enteredWord = value
							i+=1
						else:
							if i!=0:
								i-=1
								enteredWord = enteredWord.replace(enteredWord[i]," ",1)
								gameScreen.displayText(jumbledword)
								gameScreen.displayAnsText(enteredWord)

					print(pos,i)
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key)!='backspace':
					if pygame.key.name(event.key)!='return':
						if i<len(word):
							enteredWord = enteredWord.replace(enteredWord[i], pygame.key.name(event.key), 1)
							value = anagrammattic.checkword(enteredWord)
							if value == True:
								gameScreen.displayAnsText(enteredWord)
								print(enteredWord,anagrammattic.checkcorrectness(enteredWord),i)
								i+=1
							else:
								enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
					else:
						gameScreen.clearScreen(jumbledword,anagrammattic.checkcorrectness(enteredWord))
						i=0
						enteredWord = "     "
				else:
					if i>0:
						i-=1
						enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
						gameScreen.displayText(jumbledword)
						gameScreen.displayAnsText(enteredWord)
					if i!=0:
						print(enteredWord,anagrammattic.checkcorrectness(enteredWord))


		milliseconds += clock.tick_busy_loop(60)
		if milliseconds >= 1000:
			seconds += 1
			milliseconds -= 1000
		if seconds >= 60:
			minutes += 1
			seconds -= 60

		gameScreen.Timer("{}:{}".format(minutes, seconds))
		pygame.time.wait(1000)		
				
	pygame.quit()
	sys.exit
main()