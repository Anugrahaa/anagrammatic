import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from words import Anagrammattic

i=0
class ClientChannel(PodSixNet.Channel.Channel):

	def Network(self, data):
		global anagramServe
		print(data)
		global i
		
		gameid = data["gameid"]
		if data["num"]==None and data["entered"]==True:
			i+=1
			data["entered"]=False
		if i==2:
			anagramServe.Startgame()
			i=0
		if data["num"]==1:
			player1score = data["score"]
			anagramServe.Updatescore(player1score,1, gameid)

		elif data["num"]==0:
			player0score = data["score"]
			anagramServe.Updatescore(player0score,0, gameid)

		if data["nextlevel"]==True:
			i+=1
			if i==2:
				anagramServe.LevelUp(gameid)			
				i=0



class AnagramServer(PodSixNet.Server.Server):
	def __init__(self, *args, **kwargs):
		PodSixNet.Server.Server.__init__(self, *args, **kwargs)
		self.games = []
		self.queue = None
		self.currentIndex=0
	channelClass = ClientChannel

	def Startgame(self):
			anagrammatic = Anagrammattic()
			word = anagrammatic.getRandomFiveLetterWord("fiveLetterWords.txt")
			self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid, "word":word})
			self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid, "word":word})
			self.queue=None
	def LevelUp(self, gameid):
		game = []
		print("level up in AnagramServer")
		for a in self.games:
			if a.gameId()==gameid:
				game.append(a)
				break
		print("out of loop in anagram server")
		if len(game)==1:
			print(game[0])
			game[0].levelup()

	def Updatescore(self,playerscore,num,gameid):
		game = []
		for a in self.games:
			if a.gameId()==gameid:
				game.append(a)
				break
		if len(game)==1:
			game[0].Updatescore(playerscore,num)
			
	def Connected(self, channel, addr):
		print("new connection: ", channel)
		if self.queue==None:
		    self.currentIndex+=1
		    channel.gameid=self.currentIndex
		    self.queue=Game(channel, self.currentIndex)

		else:
		    channel.gameid=self.currentIndex
		    self.queue.player1=channel
		    self.games.append(self.queue)
		    

class Game():
	def __init__(self, player, currentIndex):
		self.player0 = player
		self.player1 = None
		self.gameid = currentIndex
		self.player0score = 0
		self.player1score = 0

	def gameId(self):
		return self.gameid

	def Updatescore(self,playerscore,num):
		if num==0:
			self.player0score = playerscore
		else:
			self.player1score = playerscore

	def levelup(self,):
		anagrammatic = Anagrammattic()
		word = anagrammatic.getRandomFiveLetterWord("fiveLetterWords.txt")
		if int(self.player0score) > int(self.player1score):
			self.player0.Send({"action": "win","win":True, "score": self.player0score, "oppscore": self.player1score, "word":word})
			self.player1.Send({"action": "win","win":False, "score": self.player1score, "oppscore": self.player0score, "word":word})

		elif int(self.player0score) < int(self.player1score):
			self.player1.Send({"action": "win","win":True, "score": self.player1score, "oppscore": self.player0score, "word":word})
			self.player0.Send({"action": "win","win":False, "score": self.player0score, "oppscore": self.player1score, "word":word})


print("STARTING SERVER ON LOCALHOST")
anagramServe = AnagramServer()
while True:
	anagramServe.Pump()
	sleep(0.01)



		
