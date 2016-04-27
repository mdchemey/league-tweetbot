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
	
	# Retrieves information about your current game
	try:
		game = getCurrentGameData(ID, key)
	except:
		logging.exception('Could not retrieve current game data.')
	gameID = game['gameId']
	
	# Retrieves which participant position you are in (tried 'for n in range (0,10)' to replace this if chain but consistently returned errors)
	val = 0
	if game['participants'][0]['summonerId'] == int(ID):
		val = 0
	elif game['participants'][1]['summonerId'] == int(ID):
		val = 1
	elif game['participants'][2]['summonerId'] == int(ID):
		val = 2
	elif game['participants'][3]['summonerId'] == int(ID):
		val = 3
	elif game['participants'][4]['summonerId'] == int(ID):
		val = 4
	elif game['participants'][5]['summonerId'] == int(ID):
		val = 5
	elif game['participants'][6]['summonerId'] == int(ID):
		val = 6
	elif game['participants'][7]['summonerId'] == int(ID):
		val = 7
	elif game['participants'][8]['summonerId'] == int(ID):
		val = 8
	elif game['participants'][9]['summonerId'] == int(ID):
		val = 9
	else:
		print "Player not found."
		logging.info("Player not found.")
		
	# Retrieves information about your Champion
	champion = game['participants'][val]['championId']
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
	lines=[summonername+"\n",ID+"\n",champion+"\n",mapname+"\n",str(gameID)]
	writesave.writelines(lines)

	# Format string, send the tweet
	print "Sending tweet on current game."
	logging.info("Sending tweet on current game.")
	stringtotweet = summonername + " is playing " + champion + " on the " + mapname + ". #LeagueOfLegends"
	sendTweet(stringtotweet, my_auth, 1)
