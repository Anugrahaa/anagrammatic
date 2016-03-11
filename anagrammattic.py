import sys, pygame
from pygame.locals import *
import random
import time
import enchant
from words import Anagrammattic
from display import ViewScreen

d = enchant.Dict("en_US")
anagrammattic = Anagrammattic()

jumbledword = worrd = anagrammattic.getRandomFiveLetterWord("fiveLetterWords.txt")

while(d.check(jumbledword)==True):
	jumbledword = anagrammattic.jumbleItUp(worrd)

gameScreen = ViewScreen()

screen = gameScreen.displayScreenBasics()

gameScreen.displayText(screen,worrd,jumbledword)	

gameScreen.ScreenClose()

# print("The Five-Letter Word Generator generates:",worrd,worrd[0])
# i=0
# newword = "rando"
# j = random.sample(range(len(worrd)),len(worrd))



# # print("new word: ", newword)
# d = enchant.Dict("en_US")
# print("Is this word in the dictonary?", d.check(worrd), newword)
