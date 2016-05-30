import os
import time
import subprocess
from subprocess import Popen
import tweetMyGame
import tweetLastGame
import logging

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
def looper():
	a=False
	skip=False
	print "Beginning League of Legends.exe checks."
	logging.info("Beginning League of Legends.exe checks.")
	while a is False:
		a=findProcess("League of Legends.exe")
		# when a game starts, it runs a script to tweet information about the game
		if a is True:
			print "Game started. Preparing tweet for current game."
			logging.info("Game started. Preparing tweet for current game.")
			try:
				tweetMyGame.tweetGame()
				print "Waiting for game to end."
				logging.info("Waiting for game to end.")
			except:
				logging.exception('Program failed while attempting to tweet about current game.')
				print "Program failed while attempting to tweet about current game."
				skip=True
		time.sleep(10)
	# after tweeting, it waits until the game ends and then starts the loop over
	while a is True:
		a=findProcess("League of Legends.exe")
		if a is False and skip is False:
			print "Game ended. Waiting for Match History servers to update."
			logging.info("Game ended. Waiting for Match History servers to update.")
			try:
				tweetLastGame.tweetLast(1)
			except:
				logging.exception('Program failed while attempting to tweet about previous game.')
			looper()
		if a is False and skip is True:
			logging.info('Game ended. Skipping postgame tweet due to previous failure.')
			print "Game ended. Skipping postgame tweet due to previous failure."
			looper()
		time.sleep(10)

def main():
	logging.basicConfig(filename='checkLog.log',level=logging.INFO,filemode='w',format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	logging.captureWarnings(True)
	logging.info("Started.")
	looper()

if __name__ == "__main__":
    main()
