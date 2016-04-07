# Thanks to Farzain M., Riot Games, Twitter, Mike Verdone, ActiveState, and the creators of setuptools for building resources or API's used in this project,
# as well as various Stack Overflow users for assistance in formatting various commands and recommending appropriate libraries

import os
import time
import subprocess
from subprocess import Popen
import tweetMyGame
import tweetLastGame

# opens the tasklist, filtering out all processes other than the specified process
def findProcess(processId):
	ps=subprocess.Popen(r'tasklist.exe /NH /FI "Imagename eq %s"' % processId, shell=True, stdout=subprocess.PIPE)
	output=ps.stdout.read()
	ps.stdout.close()
	ps.wait()
	if processId in output:
		return True
	else:
		return False

# regularly checks OS to see if a game of League is running
def looper(a):
	print "Beginning League of Legends.exe checks."
	while a is False:
		a=findProcess("League of Legends.exe")
		# when a game starts, it runs a script to tweet information about the game
		if a is True:
			print "Sending Tweet"
			tweetMyGame.tweetGame()
			continue
		time.sleep(10)
	# after tweeting, it waits until the game ends and then starts the loop over
	while a is True:
		time.sleep(10)
		a=findProcess("League of Legends.exe")
		if a is False:
			time.sleep(5)
			tweetLastGame.tweetLast()
			looper(a)

# checks to make sure your userInfo.txt file is filled out properly, then starts the loop
def main():
	a=False
	looper(a)

if __name__ == "__main__":
    main()