import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
from display import ViewScreen
from PodSixNet.Connection import ConnectionListener, connection

class Anagram(ConnectionListener):
	def __init__(self):
		
		# address=raw_input("Address of Server: ")
	 #        try:
	 #            if not address:
	 #                host, port="localhost", 8000
	 #            else:
	 #                host,port=address.split(":")
	 #            self.Connect((host, int(port)))
	 #        except:
	 #            print "Error Connecting to Server"
	 #            print "Usage:", "host:port"
	 #            print "e.g.", "localhost:31425"
	 #            exit()
	 #        print "Boxes client started"
	 	self.gameid = None
	 	self.num = None
		self.listOfWords = []
		for i in range(50):
			self.listOfWords.append("xxxxx")
		self.noOfWords = 0
		self.Connect()

		self.running=False
		
		#determine attributes from player #
		

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
						self.Send({"action":"startgame","score":0, "entered": True, "num": self.num, "gameid":self.gameid, "nextlevel": False})
						msg = gameScreen.playerName("Wait for the opponent")
						while not self.running:
						    self.Pump()
						    connection.Pump()
						    time.sleep(0.01)
						if self.running:
							self.running = False
							self.main(player)
							chk=False
				if event.type == pygame.QUIT:
					chk = False
		pygame.quit()
		sys.exit()

	def Network_startgame(self, data):
		self.running=True
		self.num=data["player"]
		self.gameid=data["gameid"]
		self.word = self.jumbledword = data["word"]
		print("Game started")

	def Network_win(self, data):
		print("you are here")
		if data["win"]==True:
			text = "You Won"
		else:
			text = "Better Luck Next Time"
		gameScreen = ViewScreen()
		gameScreen.FinalScreen(text, data["score"], data["oppscore"])
		self.running=True
		self.word = data["word"]


	def main(self,player):
		levelup=False
		d = enchant.Dict("en_US")
		anagrammattic = Anagrammattic()


		while(d.check(self.jumbledword)==True):
			self.jumbledword = anagrammattic.jumbleItUp(self.word)

		gameScreen = ViewScreen()
		overallscore = 0
		overallscoretext = "Total Score: "+ str(overallscore)
		b = gameScreen.displayText(player,self.jumbledword, overallscoretext)
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
						value = gameScreen.detectMouseClick(enteredWord,i,self.jumbledword,pos,anagrammattic.checkword)
						if value!=False:
							if value!=-1 and value!=-2:
								enteredWord = value
								i+=1
							else:
								if value == -1:
									if i!=0:
										i-=1
										enteredWord = enteredWord.replace(enteredWord[i]," ",1)
										overallscoretext = "Total Score: "+str(overallscore)
										gameScreen.displayText(player,self.jumbledword,overallscoretext)
										gameScreen.displayAnsText(enteredWord)

								else:
									if hint_no<3 and overallscore>=10:
										hint_no+=1
										hintword = anagrammattic.gethint(hint_no, self.word)
										overallscore-=10
										overallscoretext = "Score: "+str(overallscore)
										gameScreen.clearScreen(player,self.jumbledword,score, overallscoretext)
										gameScreen.displayHint(hintword)
										self.Send({"action":"hint","words":self.listOfWords[:self.noOfWords],"score":overallscore, "gameid":self.gameid, "num":self.num, "nextlevel":False})



				if event.type == pygame.KEYDOWN:
					if pygame.key.name(event.key)!='backspace':
						if pygame.key.name(event.key)!='return':
							if len(pygame.key.name(event.key))==1:
								if i<len(self.word):
									enteredWord = enteredWord.replace(enteredWord[i], pygame.key.name(event.key), 1)
									value = anagrammattic.checkword(enteredWord, self.jumbledword)
									if value == True:
										gameScreen.displayAnsText(enteredWord)
										i+=1
										
									else:
										enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
						else:
							score = anagrammattic.checkcorrectness(enteredWord, self.listOfWords)
							# totalscore+=score
							# totalscoretext = "Score: "+str(totalscore)
							overallscore=overallscore+score
							overallscoretext = "Total Score: "+str(overallscore)
							gameScreen.clearScreen(player,self.jumbledword,score, overallscoretext)
							i=0
							if score:
								self.listOfWords[self.noOfWords] = enteredWord.replace(" ","")
								self.noOfWords+=1
								self.Send({"action": "formword", "words": self.listOfWords[:self.noOfWords],"score":overallscore, "gameid":self.gameid, "num":self.num, "nextlevel":False})
								if len(enteredWord.replace(" ",""))==5:
									print(enteredWord)
									levelup=True
							enteredWord = "     "
							
					else:
						if i>0:
							i-=1
							enteredWord = enteredWord.replace(enteredWord[i], " ", 1)
							gameScreen.displayText(player,self.jumbledword,overallscoretext)
							gameScreen.displayAnsText(enteredWord)

			connection.Pump()
			self.Pump()

			milliseconds += clock.tick_busy_loop(60)
			if milliseconds >= 1000:
				seconds += 1
				milliseconds -= 1000
			if seconds >= 60:
				minutes += 1
				seconds -= 60
				overallscoretext = "Total Score: "+str(overallscore)
				gameScreen.printScore(overallscoretext,levelup)
				pygame.time.wait(2000)
				chk = False

			gameScreen.Timer("{}:{}".format(str(minutes).zfill(2), str(seconds).zfill(2)))
			pygame.time.wait(1000)		
		
		self.Send({"action":"done","score":overallscore,"num":self.num, "gameid":self.gameid, "nextlevel": True})
		
		while not self.running:
				time.sleep(0.01)
				connection.Pump()
				self.Pump()
		pygame.time.wait(1000)
		if levelup and not quitevent:
			print("Reached")
			self.main(player)
		else:
			return

anagram = Anagram()