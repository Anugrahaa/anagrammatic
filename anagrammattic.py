import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
from display import ViewScreen
overallscore=0

def first_screen():
	gameScreen = ViewScreen()
	chk = True
	name=[]
	gameScreen.firstScreen()
	while chk:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				x = pygame.key.name(event.key)
				if x not in ['backspace', 'return'] and len(x)==1:
					name+=x
					player = gameScreen.playerName(name)
				if x=='backspace' and name:
					name.pop()
					player = gameScreen.playerName(name)

				if x=='return':
					main(player)
					chk=False
			if event.type == pygame.QUIT:
				chk = False
	pygame.quit()
	sys.exit()

def main(player):
	levelup=False
	d = enchant.Dict("en_US")
	anagrammattic = Anagrammattic()

	jumbledword = word = anagrammattic.getRandomFiveLetterWord("fiveLetterWords.txt")

	while(d.check(jumbledword)==True):
		jumbledword = anagrammattic.jumbleItUp()

	gameScreen = ViewScreen()
	totalscore = 0
	global overallscore
	totalscoretext = "Total Score: "+ str(totalscore)
	b = gameScreen.displayText(player,jumbledword, totalscoretext)
	pygame.time.wait(1000)
	chk = True
	quitevent = False
	enteredWord = "     "
	i=0
	clock = pygame.time.Clock()
	minutes = 0
	seconds = 0
	milliseconds = 0
	hint_no = 0
	while chk and not quitevent:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or event.type == pygame.QUIT:
				if event.type == pygame.QUIT:
					quitevent = True
				else:
					pos = pygame.mouse.get_pos()
					value = gameScreen.detectMouseClick(enteredWord,i,jumbledword,pos,anagrammattic.checkword)
					if value!=False:
						if value!=-1 and value!=-2:
							enteredWord = value
							i+=1
						else:
							if value == -1:
								if i!=0:
									i-=1
									enteredWord = enteredWord.replace(enteredWord[i]," ",1)
									totalscoretext = "Total Score: "+str(totalscore)
									gameScreen.displayText(player,jumbledword,totalscoretext)
									gameScreen.displayAnsText(enteredWord)

							else:
								if hint_no<3 and totalscore>=10:
									hint_no+=1
									hintword = anagrammattic.gethint(hint_no)
									totalscore-=10 
									overallscore-=10
									totalscoretext = "Score: "+str(totalscore)
									gameScreen.clearScreen(player,jumbledword,score, totalscoretext)
									gameScreen.displayHint(hintword)



			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key)!='backspace':
					if pygame.key.name(event.key)!='return':
						if len(pygame.key.name(event.key))==1:
							if i<len(word):
								enteredWord = enteredWord.replace(enteredWord[i], pygame.key.name(event.key), 1)
								value = anagrammattic.checkword(enteredWord)
								if value == True:
									gameScreen.displayAnsText(enteredWord)
									i+=1
									
								else:
									enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
					else:
						score = anagrammattic.checkcorrectness(enteredWord)
						totalscore+=score
						totalscoretext = "Score: "+str(totalscore)
						overallscore=overallscore+score
						overallscoretext = "Total Score: "+str(overallscore)
						gameScreen.clearScreen(player,jumbledword,score, totalscoretext)
						i=0
						if len(enteredWord.replace(" ",""))==5 and score:
							print(enteredWord)
							levelup=True
						enteredWord = "     "
						
				else:
					if i>0:
						i-=1
						enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
						gameScreen.displayText(player,jumbledword,totalscoretext)
						gameScreen.displayAnsText(enteredWord)


		milliseconds += clock.tick_busy_loop(60)
		if milliseconds >= 1000:
			seconds += 1
			milliseconds -= 1000
		if seconds >= 60:
			minutes += 1
			seconds -= 60
			totalscoretext = "Total Score: "+str(overallscore)
			gameScreen.printScore(totalscoretext,levelup)
			pygame.time.wait(2000)
			chk = False

		gameScreen.Timer("{}:{}".format(str(minutes).zfill(2), str(seconds).zfill(2)))
		pygame.time.wait(1000)		


	if levelup and not quitevent:
		main(player)
	else:
		return

first_screen()