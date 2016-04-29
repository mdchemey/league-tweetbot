import requests
import twitter
import time
import logging

# Retrieves information about the player's current game from Riot servers
def getCurrentGameData(ID, key):
	url = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/" + ID + "?api_key=" + key
	response = requests.get(url)
	return response.json()

# Retrieves information about the player from Riot servers
def getSumInfo(summonername, key):
	url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonername + "?api_key=" + key
	response = requests.get(url)
	return response.json()
	
# Retrieves the name of the champion the player is playing from Riot servers
def getChampName(ID, key):
	url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + ID + "?api_key=" + key
	response = requests.get(url)
	return response.json()

# Retrieves the name of the map the player is using from Riot servers
def getMaps(key):
	url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/map?api_key=" + key
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
			print "Sending current game tweet failed."
			logging.exception("Sending current game tweet failed.")
		else: 
			print "Sending tweet failed. Trying again... %d " % count
			logging.exception("Sending tweet failed. Trying again... %d " % count)
			time.sleep(5)
			sendTweet(string, my_auth, count + 1)
			return

def tweetGame():
	# Retrieves the information from userInfo.txt and applies it to the corresponding variables
	f = open('userInfo.txt')
	content = []
	for line in f:
		content.append(line.rstrip('\n'))
	f.close()
	summonername = content[0]
	key = content[1]
	my_auth = twitter.OAuth(content[2],content[3],content[4],content[5])
	
	# Retrieves remaining variables from the API and formats them
	# Retrieves summoner information
	try:
		summoner = getSumInfo(summonername, key)
	except:
		logging.exception('Could not retrieve summoner data.')
	ID = summoner[summonername]['id']
	ID = str(ID)
	summonername = summoner[summonername]['name']
	partic
	# Retrieves information about your current game
	try:
		game = getCurrentGameData(ID, key)
	except:
		logging.exception('Could not retrieve current game data.')
	gameID = game['gameId']
	
	# Retrieves which participant position you are in
	pos = 0
	try:
		for n in range(0,10):
			if game['participants'][n]['summonerId'] == int(ID):
				pos = n
				continue
	except:
			print "Player not found."
			logging.exception("Player not found.")
		
	# Retrieves information about your Champion
	champion = game['participants'][pos]['championId']
	champion = str(champion)
	try:
		champion = getChampName(champion, key)
	except:
		logging.exception('Could not retrieve champion data.')
	champion = champion['name']
	
	# Retrieves information about the map you're playing on
	mapID = game['mapId']
	mapID = str(mapID)
	try:
		mapname = getMaps(key)
	except:
		logging.exception('Could not retrieve map data.')
	mapname = mapname['data'][mapID]['mapName']
	mapname = mapname.replace("Summoners", "Summoner's")
	if mapname.endswith("New"):
		mapname = mapname[:-3]
	if mapname.startswith("New"):
		mapname = mapname[3:]
	if "ProvingGrounds" in mapname:
		mapname = "HowlingAbyss"
	for i in mapname:
		if i.isupper() and i is not mapname[0]:
			mapname = mapname.replace(i, " " + i)
	
	# Saves some information to a file so tweetLastGame can check against it to see if the servers have updated
	print "Writing game info to file."
	logging.info("Writing game info to file.")
	writesave = open('DONOTTOUCH.txt','w')
	lines=[summonername+"\n",ID+"\n",champion+"\n",mapname+"\n",str(gameID)+"\n",str(pos)]
	writesave.writelines(lines)

	# Format string, send the tweet
	print "Sending tweet on current game."
	logging.info("Sending tweet on current game.")
	stringtotweet = summonername + " is playing " + champion + " on the " + mapname + ". #LeagueOfLegends"
	sendTweet(stringtotweet, my_auth, 1)
