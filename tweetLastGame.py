import requests
import twitter
import time

# Retrieves information about the player from Riot servers
def getSumInfo(summonername, key):
    url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + summonername + "?api_key=" + key
    response = requests.get(url)
    return response.json()
	
# Retrieves the champion information the player used from Riot servers
def getChamp(ID, key):
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + ID + "?api_key=" + key
    response = requests.get(url)
    return response.json()

# Retrieves the name of the map the player used from Riot servers
def getMaps(key):
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/map?api_key=" + key
    response = requests.get(url)
    return response.json()
	
# Retrieves the basic information of your most recent match from Riot servers
def getRecentMatch(ID, key):
	url = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/" + ID + "/recent?api_key=" + key
	response = requests.get(url)
	return response.json()

# Retrieves more detailed information about your most recent match (using getRecentMatch's result) from Riot servers
def getMatchInfo(matchID, key):
	url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + matchID + "?api_key=" + key
	response = requests.get(url)
	return response.json()
	
def tweetLast(count):
	# Retrieves the information from userInfo.txt and applies it to the corresponding variables
	userInfo = open('userInfo.txt')
	content = []
	for line in userInfo:
		content.append(line.rstrip('\n'))
	summonername = content[0]
	key = content[1]
	my_auth = twitter.OAuth(content[2],content[3],content[4],content[5])
	
	# Retrieves remaining variables from the API and formats them
	# Retrieve and format summoner information
	summoner=getSumInfo(summonername, key)
	ID = summoner[summonername]['id']
	ID = str(ID)
	summonername = summoner[summonername]['name']
	# Retrieve your recent games and the list of maps to refer to
	gamelist = getRecentMatch(ID, key)
	maplist = getMaps(key)
	# Retrieve the game ID of your latest game
	game = gamelist['games'][0]['gameId']
	game = str(game)
	# Retrieve and format the map information of your latest game
	map = gamelist['games'][0]['mapId']
	map = str(map)
	map = maplist['data'][map]['mapName']
	map = map.replace("Summoners", "Summoner's")
	if map.endswith("New"):
		map = map[:-3]
	if map.startswith("New"):
		map = map[3:]
	if "ProvingGrounds" in map:
		map = "HowlingAbyss"
	for i in map:
		if i.isupper() and i is not map[0]:
			map = map.replace(i, " " + i)
	# Retrieve and format the information on the champion you played in your latest game
	champion = gamelist['games'][0]['championId']
	champion = str(champion)
	champion = getChamp(champion, key)
	champion = champion['name']
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
	# Currently not in use due to errors, will try to reimplement
	accountID=""
	# if "RANKED" in gamelist['games'][0]['subType']:
		# matchDet = getMatchInfo(game, key)
		# for n in range(0,10):
			# if matchDet['participantIdentities'][n]['player']['summonerName'] == summonername:
				# accountID = matchDet['participantIdentities'][n]['player']['matchHistoryUri']
				# continue
		# accountID = accountID[28:]
	# Checks against the file created in tweetMyGame to make sure the servers have updated
	latestInfo = open('DONOTTOUCH.txt')
	latestContent = []
	for line in latestInfo:
		latestContent.append(line.rstrip('\n'))
	if champion != latestContent[0] or map != latestContent[1]:
		print "Still waiting on the servers to update... %d" % count
		time.sleep(5)
		tweetLast(count + 1)
		return
	
	print "Sending tweet on previous game."
	
	#Format string, send the tweet
	stringtotweet = summonername + " just went " + kills + "/" + deaths + "/" + assists + " as " + champion + " in a " + winloss + " on the " + map + ". #LeagueofLegends http://matchhistory.na.leagueoflegends.com/en/#match-details/NA1/" + game + accountID + "?tab=overview"
	print stringtotweet
	twit = twitter.Twitter(auth=(my_auth))
	twit.statuses.update(status = stringtotweet)
