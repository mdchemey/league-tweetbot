import requests
import twitter

# Retrieves information about the player's current game from Riot servers
def getCurrentGameData(ID, key):
    url = "https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/" + ID + "?api_key=" + key
    response = requests.get(url)
    return response.json()

# Retrieves information about the player from Riot servers
def getSumName(summonername, key):
    url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonername + "?api_key=" + key
    response = requests.get(url)
    return response.json()
	
# Retrieves the name of the champion the player is playing from Riot servers
def getChampName(ID, key):
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + ID + "?api_key=" + key
    response = requests.get(url)
    return response.json()

# Retrieves the name of the map the player is using from Riot servers
def getMapName(key):
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/map?api_key=" + key
    response = requests.get(url)
    return response.json()

def tweetGame():
	# Retrieves the information from userInfo.txt and applies it to the corresponding variables
	f = open('userInfo.txt')
	content = []
	for line in f:
		content.append(line.rstrip('\n'))
	summonername = content[0]
	key = content[1]
	my_auth = twitter.OAuth(content[2],content[3],content[4],content[5])
	
	# Retrieves remaining variables from the API and formats them
	# Retrieves summoner information
	getname = getSumName(summonername, key)
	ID = getname[summonername]['id']
	ID = str(ID)
	summonername = getname[summonername]['name']
	# Retrieves information about your current game
	game = getCurrentGameData(ID, key)
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
		exit()
	# Retrieves information about your Champion
	champion = game['participants'][val]['championId']
	champion = str(champion)
	champion = getChampName(champion, key)
	champion = champion['name']
	# Retrieves information about the map you're playing on
	mapID = game['mapId']
	mapID = str(mapID)
	mapname = getMapName(key)
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
    
	#Format string, send the tweet
	stringtotweet = summonername + " is playing " + champion + " on the " + mapname + ". #LeagueOfLegends\n\nBeep boop, this tweet was automated "
	print stringtotweet
	twit = twitter.Twitter(auth=(my_auth))
	twit.statuses.update(status = stringtotweet)
