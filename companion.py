#!/usr/bin/python3

import requests, json
from git import Repo
from datetime import date
import configparser
import feedparser
import os
import shutil
import sys
import time

# Preferred temperature unit
TEMP_UNIT = ""

# This setup will only work for the USA.
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

# The city of which you reside in, or otherwise want weather data from.
CITY = ""
CITY_HUMANFRIENDLY = ""

# Your OpenWeatherMap API key. You must get your own.
API_KEY = ""

# Full API URL for weather data.
WEATHER_URL = ""

# RSS Feeds - the first one is always the repository RSS feed.
FEEDS = []

# Refresh times for News, Weather, and Pages, respectively.
NEWS_REFRESH = -1
WEATHER_REFRESH = -1
PAGE_REFRESH = -1

isDaemon = False

def loadConfig():
	global TEMP_UNIT
	global CITY
	global CITY_HUMANFRIENDLY
	global API_KEY
	global WEATHER_URL
	global FEEDS
	global NEWS_REFRESH
	global WEATHER_REFRESH
	global PAGE_REFRESH

	config = configparser.ConfigParser()

	if (os.path.exists('companion.ini')):
		config.read('companion.ini')
	else:
		print("FATAL: companion.ini does not exist. Have you setup the companion? Check README.md.")
		sys.exit(1)

	TEMP_UNIT=config['Weather']['DegreeUnit']
	CITY=config['Weather']['City']
	API_KEY=config['Weather']['APIKey']

	# We must run through the CITY to replace all spaces with "%20"
	CITY_HUMANFRIENDLY = CITY
	CITY = CITY.replace(" ", "%20")

	WEATHER_URL = WEATHER_BASE_URL + "q=" + CITY + "&appid=" + API_KEY

	feedsPreparse=config['RSS']['Commits'] + " " + config['RSS']['Feeds']
	FEEDS = feedsPreparse.split()

	if (isDaemon):
		NEWS_REFRESH = config['Daemon']['NewsRefresh']
		WEATHER_REFRESH = config['Daemon']['WeatherRefresh']
		PAGE_REFRESH = config['Daemon']['PageRefresh']

def mainMenu():
	print("Hypolive Companion v0.01")
	print("------------------------")
	print("What would you like to do?")
	continueFlag = True

	while(continueFlag):
		print("1. Update (Pull) Hypnolive pages")
		print("2. Reset all pages (DO THIS BEFORE COMMITS)")
		print("3. Update weather data")
		print("4. Update RSS feeds (News)")
		print("A. Full update")
		print("B. Periodic full update")
		print("X. Exit")
		choice = input("Enter your choice > ")

		match choice:
			case "1":
				print("Updating Hypnolive...")
				updateHypnolive()
			case "2":
				print("Resetting all modified pages...")
				print("Restoring weather...")
				restoreWeather()
				print("Restoring RSS feeds...")
				restoreNews()
				print("Done")
			case "3":
				print("Updating weather...")
				updateWeather()
			case "4":
				print("Updating RSS feeds...")
				updateNews()
			case "A":
				print("Full update")
				updateAll()
			case "B":
				print("Periodic full update")
				print("In order to do a periodic full update, you must run this file as a daemon.")
				print("A daemon is a process that runs in the background.")
				print("You can do this by running this script with the -d switich (python3 companion.py -d)")
				print("Information on how to automatically do this on startup is located in the README file.")
			case "X":
				continueFlag = False
			case _:
				print("Invalid Command. Note that the input must be uppercase if it's a letter.")

def daemonize():
	print("Starting Hypnolive Companion in daemon mode.")
	print("News will update every " + str(NEWS_REFRESH) + " seconds.")
	print("Weather will update every " + str(WEATHER_REFRESH) + " seconds.")
	print("Pages will update every " + str(PAGE_REFRESH) + " seconds.")
	
	# We update everything first, then begin the loop.
	updateAll()

	timeStartNews	= time.time()
	timeStartWeather= time.time()
	timeStartPages	= time.time()
	
	while(True):
		timeNews	= time.time()
		timeWeather	= time.time()
		timePages	= time.time()


		if ((timeNews - timeStartNews) > float(NEWS_REFRESH)):
			print("Updating News...")
			updateNews()
			print("Done.")
			timeStartNews = time.time()
		
		if ((timeWeather - timeStartWeather) > float(WEATHER_REFRESH)):
			print("Updating Weather...")
			updateWeather()
			print("Done.")
			timeWeather = time.time()

		if ((timePages - timeStartPages) > float(PAGE_REFRESH)):
			print("Updating Hypnolive pages...")
			updateHypnolive()
			print("Done.")
			timePages = time.time()

def updateAll():
	print("Updating weather...")
	updateWeather()

	print("Updating RSS feeds...")
	updateNews()
	
	print("Updating Hypnolive Pages...")
	updateHypnolive()
	
	print("Done.")

def updateHypnolive():
	# This is poorly tested
	#git = repo.git

	#git.pull()
	print("Hypnolive Page updating not yet implemented.")
	

def updateWeather():
	response = requests.get(WEATHER_URL)

	if response.status_code == 200:
		data = response.json()

		main = data['main']

		# Get weather data
		temperature = main['temp']
		temperatureHigh = main['temp_max']
		temperatureLow = main['temp_min']
		humidity = main['humidity']
		pressure = main['pressure']
		report = data['weather']

		# Write weather data into array.
		weatherData = [
			"Weather for " + CITY_HUMANFRIENDLY,
			"Temperature: " + str(temperature) + " Kelvin",
			"High: " + str(temperatureHigh) + " Kelvin",
			"Low: " + str(temperatureLow) + " Kelvin",
			"It is currently " + report[0]['main'] + ", " + report[0]['description'],
			"Humidity: " + str(humidity) + " Percent",
			"Pressure: " + str(pressure) + " hPa"
			]

		# Open ~weather.hsp to read current json.
		f = open('hs/69_hypnolive/hypnolivenews/~weather.hsp', 'r')
		data = json.load(f)

		# Close ~weather.hsp and reopen it with write permissions instead.
		f.close()
		f = open('hs/69_hypnolive/hypnolivenews/~weather.hsp', 'w')
		

		print("Changes to be made to hs/69_hypnolive/hypnolivenews/~weather.hsp:")
		for i in range(9, 16):
			print(data['data'][i][1][5] + " --> " + weatherData[i-9]);

		print("----------------------------")
		print("Making changes...")
		
		for i in range(9, 16):
			data['data'][i][1][5] = weatherData[i-9]

		# Insert current date.
		today = date.today()
		#print(today.strftime("%B %d, %Y"))

		data['data'][17][1][5] = " " + today.strftime("%B %d, %Y")

		print("Saving and closing...")

		newJson = json.dumps(data)

		f.seek(0)
		f.write(newJson)
	
		f.close

	else:
		print("Error in HTTP request. Check your API key, or try again later.")
		print("HTTP error code: " + str(response.status_code))

def restoreWeather():
	# Open the actual Hypnospace file and the stock file.
	workingFile=open("hs/69_hypnolive/hypnolivenews/~weather.hsp", "w")
	stockFile=open("stockfiles/~weather.hsp", "r")

	# Read stock file into string and close.
	stockFileData = stockFile.read()
	stockFile.close()

	# Write stock file into working file and close.
	workingFile.seek(0)
	workingFile.write(stockFileData)
	workingFile.close()
	
	print("~weather.hsp reverted to stock.")

def updateNews():
	#print(FEEDS)
	newsFeed = feedparser.parse(FEEDS[1])
	entry = newsFeed.entries[0]

	# Get ~rssfeedsfull.hsp data to play with, then reopen with write permissions.
	try:
		allRSSFeeds = open("hs/69_hypnolive/hypnolivenews/~rssfeedsfull.hsp", "r")
		allRSSFeedsJSON = json.load(allRSSFeeds)
		allRSSFeeds.close()
	except:
		# This fix sucks.
		print("First run. Resetting pages.")
		restoreWeather()
		restoreNews()
		
		allRSSFeeds = open("hs/69_hypnolive/hypnolivenews/~rssfeedsfull.hsp", "r")
                allRSSFeedsJSON = json.load(allRSSFeeds)
                allRSSFeeds.close()

	allRSSFeeds = open("hs/69_hypnolive/hypnolivenews/~rssfeedsfull.hsp", "w")

	currentElement = 1
	currentMainElement = 1
	currentFeed = 0
	currentArticle = 0
	
	for i in FEEDS:
		linkJSONObject = json.loads('[["Text",' + str(13734+currentFeed) + ',"Feed ' + str(currentFeed) + '","","","","","","","","","","","","","","","","","",""],["DEFAULT","0","' + str(10+(10*(currentFeed))) + '","100","0","  Link to ' + i + '","241919","HypnoFont","0n","0","hs\\\\69_hypnolive\\\\hypnolivenews\\\\feeds\\\\~feed' + str(currentFeed) + '.hsp","0","0","10","65535","10","0","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""]]')
		allRSSFeedsJSON['data'].append(linkJSONObject)

		newsFeed=feedparser.parse(i)
		f=open("stockfiles/~singlefeed.hsp", "r")
		newFeedPage = json.load(f)
		f.close()
		f=open("hs/69_hypnolive/hypnolivenews/feeds/~feed" + str(currentFeed) + ".hsp", "w")

		for j in newsFeed.entries:
			
			titleJSONObject = json.loads('[["Text",' + str(13933+currentElement) + ',"Update ' + str(currentArticle) + '","","","","","","","","","","","","","","","","","",""],["DEFAULT","0","' + str(65*(currentArticle))+ '","100","0","   ' + j.title + '","14542059","HypnoFont","0b","0","-1","0","0","10","-1","10","0","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""]]')
			articleJSONObject = json.loads('[["Text",' + str(13933+currentElement+1) + ',"Update ' + str(currentArticle) + ' Text","","","","","","","","","","","","","","","","","",""],["DEFAULT","0"," ' + str(10+(65*(currentArticle)))+ ' ","100","0","     ' + j.summary + '","14542059","HypnoFont","0n","0","-1","0","0","10","-1","10","0","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""],["","","","","","","","","","","","","","","","","","","","",""]]')
			
			newFeedPage['data'].append(titleJSONObject)
			newFeedPage['data'].append(articleJSONObject)

			#print("Updates from " + i)
			#print("Title: " + j.title)
			#print("Published: " + j.published)
			#print("Summary:")
			#print(j.summary)
			#print("Link: " + j.link)
			currentElement = currentElement + 2
			currentArticle = currentArticle + 1
		newFeedPage['size'][0] = currentElement
		newPage = json.dumps(newFeedPage)
		f.seek(0)
		f.write(newPage)
		f.close()
		currentElement = 0
		currentArticle = 0
		currentFeed = currentFeed + 1
		currentMainElement = currentMainElement + 1

	allRSSFeedsJSON['size'][0] = currentMainElement	
	newRSSFull = json.dumps(allRSSFeedsJSON)
	allRSSFeeds.seek(0)
	allRSSFeeds.write(newRSSFull)
	allRSSFeeds.close

def restoreNews(): # Ugly.
	# Open the actual Hypnospace file and the stock file.
	workingFile=open("hs/69_hypnolive/hypnolivenews/~rssfeedsfull.hsp", "w")
	stockFile=open("stockfiles/~rssfeedsfull.hsp", "r")

	# Read stock file into string and close.
	stockFileData = stockFile.read()
	stockFile.close()

	# Write stock file into working file and close.
	workingFile.seek(0)
	workingFile.write(stockFileData)
	workingFile.close()

	print("~rssfeedsfull.hsp reverted to stock.")

	# Open the actual Hypnospace file and the stock file.
	workingFile=open("hs/69_hypnolive/hypnolivenews/~rssfeeds.hsp", "w")
	stockFile=open("stockfiles/~rssfeeds.hsp", "r")

	# Read stock file into string and close.
	stockFileData = stockFile.read()
	stockFile.close()

	# Write stock file into working file and close.
	workingFile.seek(0)
	workingFile.write(stockFileData)
	workingFile.close()

	print("~rssfeeds.hsp reverted to stock.")

	for root, dirs, files in os.walk('hs/69_hypnolive/hypnolivenews/feeds/'):
		for f in files:
			os.unlink(os.path.join(root, f))
		for d in dirs:
			shutil.rmtree(os.path.join(root, d))

	print("Feed cache deleted.")

def loadArgs():
	global isDaemon

	for arg in sys.argv:
		match (arg):
			case ("-d"):			# Daemonize
				isDaemon = True

def main():
	loadArgs()
	loadConfig()

	if (isDaemon):
		daemonize()
	else:
		mainMenu()
	

# First we must check that Python version is >= 3.10
if (sys.version_info.major != 3 and sys.version_info.minor < 10):
	print("FATAL: Python 3.10 or higher is required.")
	sys.exit(1)

# Now we may run the main function
main()
