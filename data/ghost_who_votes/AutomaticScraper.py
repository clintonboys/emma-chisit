'''
 _______  _______  _______  _______ 
(  ____ \(       )(       )(  ___  )
| (    \/| () () || () () || (   ) |
| (__    | || || || || || || (___) |
|  __)   | |(_)| || |(_)| ||  ___  |
| (      | |   | || |   | || (   ) |
| (____/\| )   ( || )   ( || )   ( |
(_______/|/     \||/     \||/     \|
                                    
 _______          _________ _______ __________________
(  ____ \|\     /|\__   __/(  ____ \|__   __/\__   __/
| (    \/| )   ( |   ) (   | (    \/   ) (      ) (   
| |      | (___) |   | |   | (_____    | |      | |   
| |      |  ___  |   | |   (_____  )   | |      | |   
| |      | (   ) |   | |         ) |   | |      | |   
| (____/\| )   ( |___) (___/\____) |___) (___   | |   
(_______/|/     \|\_______/\_______)\_______/   )_( 

(c) Clinton Boys 2015

-------------------
AutomaticScraper.py
-------------------

v1.0  Scrapes the GhostWhoVotes twitter feed for 
	  all recent tweets. Maintains a unique and 
	  ordered database of tweets for parsing as polls.

'''

from twitter import *
from keys import keys
from store_id import id_dict
import time
import numpy as np
import pandas as pd
import os 

## Authorisation for Twitter API.

consumer_key        = keys['consumer_key']
consumer_secret     = keys['consumer_secret']
access_token        = keys['access_token']
access_token_secret = keys['access_token_secret']

twitter = Twitter(auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

user = "GhostWhoVotes"
database = 'tweet_database.csv'

## Helper function to print ordinal numbers properly

def OrdinalString(n):
	if len(str(n)) == 1:
		if n == 1:
			return '1st'
		elif n == 2:
			return '2nd'
		elif n == 3:
			return '3rd'
		else:
			return str(n)+'th'
	else:
		if str(n)[-1] == '1' and str(n)[-2] != '1':
			return str(n)+'st'
		elif str(n)[-1] == '2' and str(n)[-2] != '1':
			return str(n)+'nd'
		elif str(n)[-1] == '3' and str(n)[-2] != '1':
			return str(n)+'rd'
		else:
			return str(n) + 'th'

## Check if the database exists; if not, create it.

def main():

	print '''Emma Chisit v1.0\n-------------------\nAutomaticScraper.py\n-------------------'''

	if not os.path.isfile(database):
		with open(database, 'a') as dump_file:
			dump_file.write('tweet_id,tweet_text,time'+'\n') 

	## Read the database

	print 'Reading tweet database....'

	data = pd.read_csv(database)[['tweet_id','tweet_text','time']]

	## Data needs to be sorted by timestamp

	data.time = pd.to_datetime(data.time, dayfirst = True)
	data = data.sort('time', ascending = False)
	data.index = range(0,len(data))
	print 'Found ' + str(len(data)) + ' records....'

	## Check if duplicates have been introduced,
	## remove them and reindex. 

	this_length = len(data)
	new_length = len(data.drop_duplicates())
	if this_length > new_length:
		data = data.drop_duplicates()
		print 'Removed ' + str(this_length - new_length) + ' duplicates....'
	data.index = range(0,len(data))

	## Get the ID of the most recent tweet if it 
	## exists; if not, scrape since the beginning
	## of 2015. 

	if len(data) > 0:
		since_id = data['tweet_id'].iloc[0]
	else: 
		since_id = 550642284887547904  # First tweet of 2015
	start_time = time.time()

	max_id   = 999999999999999999

	tweets_left = False
	n = 1
	while not tweets_left:

		## Use max_id and since_id to paginate the tweets.

		print 'Now scraping ' + OrdinalString(n) + ' page, ' + str(np.round(time.time()-start_time,3)) + ' seconds elapsed...'
		results = twitter.statuses.user_timeline(screen_name = user, since_id = since_id, max_id = max_id)
		try:
			max_id = results[-1]["id"]
		except IndexError:

			## If we get no max_id, there were no tweets since since_id. 

			tweets_left = True
			print 'No new tweets...'
			pass
		for status in results:
			try:

				## For each status on this page, add the tweet to the end 
				## of the dataframe, ignoring encode errors. 

				print str(status["created_at"]), str(status["id"])
				data.loc[len(data)]=[status["id"],str(status["text"]).encode('utf-8').replace(',','').replace('\n','').replace('\t',''),status["created_at"]] 
			except UnicodeEncodeError:
				pass
		length = len(results)
		if length < 2:
			tweets_left = True
		n = n+1

	## Coerce to timetamp, reorder, drop duplicates and write to file. 

	data['time'] = pd.to_datetime(data['time'],dayfirst = True)
	data = data.sort('time',ascending = False)
	data = data.drop_duplicates()
	data.index = range(0,len(data))
	data.to_csv(database)


if __name__ == "__main__":

    main()
