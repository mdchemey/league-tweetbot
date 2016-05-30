import requests
import twitter
import time
import logging

# Retrieves detailed information about your most recent match from Riot servers
def getMatchInfo(matchID, region, key):
	url = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.2/match/" + matchID + "?api_key=" + key
	response = requests.get(url)
	return response.json()
		
def sendTweet(string, my_auth, count):
	twit = twitter.Twitter(auth=(my_auth))
	try:	
		twit.statuses.update(status = string)
		print string
		logging.info("Tweet sent: \"" + string + "\"")
	except:
		if count>5:
			print "Sending post-game tweet failed."
			logging.exception("Sending post-game tweet failed.")
		else: 
			print "Sending tweet failed. Trying again... %d " % count
			logging.exception("Sending tweet failed. Trying again... %d " % count)
			time.sleep(5)
			sendTweet(string, my_auth, count + 1)
			return
	
def tweetLast(count):
	# Retrieves the information from userInfo.txt and applies it to the corresponding variables
	userInfo = open('userInfo.txt')
	content = []
	for line in userInfo:
		content.append(line.rstrip('\n'))
	userInfo.close()
	region = content[1]
	key = content[2]
	my_auth = twitter.OAuth(content[3],content[4],content[5],content[6])
	
	# Opens file created in tweetMyGame and retrieves information about your last game
	latestInfo = open('DONOTTOUCH.txt')
	latestContent = []
	for line in latestInfo:
		latestContent.append(line.rstrip('\n'))
	latestInfo.close()
	
	summonername = latestContent[0]
	ID = latestContent[1]
	champion = latestContent[2]
	map = latestContent[3]
	game = latestContent[4]
	pos = int(latestContent[5])
		
	# Retrieve data on your most recent game once the server has updated
	try:
		match = getMatchInfo(game, region, key)
	except:
		print "Could not retrieve recent match data. Retrying... %d" % count
		logging.exception("Could not retrieve recent match data. Retrying... %d" % count)
		time.sleep(5)
		tweetLast(count + 1)
		return
	try:
		# Retrieve if you won or lost your most recent game
		team = int(pos/5)
		winloss = match['teams'][team]['winner']
		winloss = str(winloss)
		if winloss == 'True':
			winloss = "win"
		else: 
			winloss = "loss"
		# Retrieve your K/D/A from your most recent game
		kills = match['participants'][pos]['stats']['kills']
		kills = str(kills)
		deaths = match['participants'][pos]['stats']['deaths']
		deaths = str(deaths)
		assists = match['participants'][pos]['stats']['assists']
		assists = str(assists)
	except: 
		print "Still waiting on the servers to update... %d" % count
		logging.info("Still waiting on the servers to update... %d" % count)
		time.sleep(5)
		tweetLast(count + 1)
		return
	
	# If your most recent game was a ranked game, retrieve your Account ID to append to the Match History link
	accountID=""
	if "RANKED" in match['queueType'] and "UN" not in match['queueType']:
		accountID = match['participantIdentities'][pos]['player']['matchHistoryUri']
		accountID = accountID[28:]
	
	print "Sending tweet on previous game."
	logging.info("Sending tweet on previous game.")
	
	#Format string, send the tweet
	stringtotweet = summonername + " just went " + kills + "/" + deaths + "/" + assists + " as " + champion + " in a " + winloss + " on the " + map + ". #LeagueofLegends http://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/" + game + accountID + "?tab=overview"
	sendTweet(stringtotweet, my_auth, 1)
