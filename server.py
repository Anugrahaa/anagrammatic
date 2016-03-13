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

		if data["num"]==None and data["entered"]==True:
			i+=1
			data["entered"]=False
		if i==2:
			anagramServe.Startgame()
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


print("STARTING SERVER ON LOCALHOST")
anagramServe = AnagramServer()
while True:
	anagramServe.Pump()
	sleep(0.01)



		
