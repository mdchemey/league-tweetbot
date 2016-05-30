# league-tweetbot
Automatically tweets information about a player's game at start and end

Thanks to Python, Riot Games, Twitter, Mike Verdone, Setuptools, Requests, Pyinstaller, Farzain M., and various Stack Overflow users for providing utilities and/or information which helped me build this project.

To contact me with questions/problems, tweet @mdchemey on twitter or email me at mdchemey@gmail.com.

BUILD AND USE INSTRUCTIONS:

To build and successfully use this project, you will need: 
* Microsoft Windows
* Python version 2.7.11: download from https://www.python.org/downloads/release/python-2711/, add to system native path during installation
* Requests: in command line, enter "pip install requests" (no quotes)
* Setuptools (needed for Python Twitter Tools): if not installed automatically with Python (check by typing "easy_install" into the command prompt), download from https://pypi.python.org/pypi/setuptools#downloads, extract, follow the readme
* Python Twitter Tools: in command line, enter "easy_install twitter" (no quotes)
* Pyinstaller (if you want to run it as a standalone exe): pip install pyinstaller
* A twitter account: https://www.twitter.com
* A League of Legends account: https://leagueoflegends.com 
* A Riot Games API Key: https://developer.riotgames.com/

To connect the project to your twitter account, you will need to create a Twitter app: 
* Go to apps.twitter.com
* Press "Create New App"
* Fill out the form with whatever you want, it makes no difference
* Create the application 
* Go to the "Keys and Access Tokens" tab in the app's page
* Press "Create my access token"
* Keep the page open until the 'userInfo.txt' file is filled out, as per below

You will then need to empty the placeholder 'userInfo.txt' file and fill it out with the following values, in order, one value per line:
* Your League of Legends summoner name (NO SPACES OR CAPITALIZATION)
* The region your account is on (example: na or euw)
* Your Riot Games API Key
* Your Twitter app's Access Token
* Your Twitter app's Access Token Secret
* Your Twitter app's Consumer Key
* Your Twitter app's Consumer Secret

Save 'userInfo.txt' and close it and your Twitter application's tab; you won't need either from here on out.

If you don't want to bundle the project into a standalone .exe file which can run in the background, you're done. Just make sure all the files from this project are in the same folder (you can delete both .bat files; you won't use them unless you want to later bundle it into a .exe). You can run the project by double-clicking on 'checkLeague.py' in the file explorer.

If you DO want to bundle the project into a standalone .exe file, you have a couple steps to go:
* First, you have to decide if you want to make the program open a window that gives feedback on the program's status when it runs (but can not be closed without stopping the program) or if you want it to run in the background (meaning it can only be closed from the Task Manager but will run completely without disturbing you)
* Then, if you want to run it in a window so you can view some basic status messages, just double-click on the 'bundle-w.bat' file (or run it in the command line) and let it run. It should create two folders ('build' and 'dist') and one file ('checkLeague.spec') if successful.
* If you want to run it in the background, just double-click on the 'bundle-b.bat' file (or run it in the command line) and let it run. It should create two folders ('build' and 'dist') and one file ('checkLeague.spec') if successful.
* The program is now built! You'll find 'checkLeague.exe' in (folder you started in)\dist\checkLeague.
* You can now safely copy 'checkLeague.exe' anywhere you want, as long as you also copy 'userInfo.txt' (which was automatically copied into the \dist\checkLeague folder but can also be found in your original folder) to the same location.

Once running, 'checkLeague.exe' will wait for a game of League of Legends to start on your computer, then tweet "(Summoner Name) is playing (Champion) on the (Map). #LeagueOfLegends" 

It will then wait for the game to end, then pull up information about the game's results and tweet "(Summoner Name) just went (K/D/A) as (Champion) in a (Win/Loss) on the (Map). #LeagueOfLegends (Match History Link to that game)

When running, the program will create a file named 'DONOTTOUCH.txt' and, as the filename suggests, you should not change the contents of that file. If you alter it during a game, the program will break and/or get stuck in an infinite loop and will need to be restarted.

KNOWN ISSUES IN v0.5:

* SSL is not integrated, so you may get warnings about an insecure connection in the log for each call made. This should not interfere with functionality at all, but I would like to get SSL working in the future.
