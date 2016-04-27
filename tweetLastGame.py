import requests
import twitter
import time
import logging
	
# Retrieves the basic information of your most recent match from Riot servers
def getRecentMatch(ID, key):
	url = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/" + ID + "/recent?api_key=" + key
	response = requests.get(url)
	return response.json()

# Retrieves more detailed information about your most recent match (using getRecentMatch's result) from Riot servers
def getRankedMatchInfo(matchID, key):
	url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + matchID + "?api_key=" + key
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
	key = content[1]
	my_auth = twitter.OAuth(content[2],content[3],content[4],content[5])
	
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
	
	# Retrieve your recent games
	try:
		gamelist = getRecentMatch(ID, key)
	except:
		print "Could not retrieve recent match data. Retrying... %d" % count
		logging.exception("Could not retrieve recent match data. Retrying... %d" % count)
		time.sleep(5)
		tweetLast(count + 1)
		return
	
	# Wait for the servers to update to include your most recent game
	if game != str(gamelist['games'][0]['gameId']):
		print "Still waiting on the servers to update... %d" % count
		logging.info("Still waiting on the servers to update... %d" % count)
		time.sleep(5)
		tweetLast(count + 1)
		return
	
	# Retrieve if you won or lost your most recent game
	winloss = gamelist['games'][0]['stats']['win']
	winloss = str(winloss)
	if winloss == 'True':
		winloss = "win"
	else: 
		winloss = "loss"
		
	# Retrieve your K/D/A from your most recent game
	kills = gamelist['games'][0]['stats']['championsKilled']
	kills = str(kills)
	deaths = gamelist['games'][0]['stats']['numDeaths']
	deaths = str(deaths)
	assists = gamelist['games'][0]['stats']['assists']
	assists = str(assists)
	
	# If your most recent game was a ranked game, retrieve your Account ID to append to the Match History link
	accountID=""
	if "RANKED" in gamelist['games'][0]['subType'] and "UN" not in gamelist['games'][0]['subType']:
		try:
			matchDet = getRankedMatchInfo(game, key)
		except:
			logging.exception('Could not retrieve Ranked Match data.')
		for n in range(0,10):
			if matchDet['participantIdentities'][n]['player']['summonerName'] == summonername:
				accountID = matchDet['participantIdentities'][n]['player']['matchHistoryUri']
				continue
		accountID = accountID[28:]
	
	print "Sending tweet on previous game."
	logging.info("Sending tweet on previous game.")
	
	#Format string, send the tweet
	stringtotweet = summonername + " just went " + kills + "/" + deaths + "/" + assists + " as " + champion + " in a " + winloss + " on the " + map + ". #LeagueofLegends http://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/" + game + accountID + "?tab=overview"
	sendTweet(stringtotweet, my_auth, 1)
