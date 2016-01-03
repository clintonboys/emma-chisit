from twitter import *
from keys import keys
from store_id import id_dict
import time
import numpy as np
import pandas as pd
import os 

#since_id = id_dict['since_id']

consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

twitter = Twitter(
		auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

user = "GhostWhoVotes"

if not os.path.isfile('test_dump.csv'):
	with open('test_dump.csv', 'a') as dump_file:
		dump_file.write('tweet_id,tweet_text,time'+'\n') 

data = pd.read_csv('test_dump.csv')

if len(data) > 0:
	since_id = data['tweet_id'].iloc[1]
else: 
	since_id = 550642284887547904  # First tweet of 2015

start_time = time.time()

max_id   = 999999999999999999

tweets_left = False
n = 1
while not tweets_left:

	print 'Now scraping ' + str(n) + 'th page, ' + str(np.round(time.time()-start_time,3)) + ' seconds elapsed...'
	results = twitter.statuses.user_timeline(screen_name = user, since_id = since_id, max_id = max_id)
	max_id = results[-1]["id"]
	with open('test_dump.csv', 'a') as dump_file:
		for status in results:
			try:
				print str(status["created_at"]), str(status["id"])
				dump_file.write(str(status["id"]) + ',' + str(status["text"]).encode('utf-8').replace(',','').replace('\n','').replace('\t','')+ ',' + str(status["created_at"]) + '\n')
			except UnicodeEncodeError:
				pass
	length = len(results)
	if length < 2:
		tweets_left = True
	n = n+1


## Scrape everything since then

## PARSER

## Take each tweet and check for a pre-det