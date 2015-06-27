from twitter import *
from keys import keys
import time
import numpy as np


consumer_key = keys['consumer_key']
consumer_secret = keys['consumer_secret']
access_token = keys['access_token']
access_token_secret = keys['access_token_secret']

twitter = Twitter(
		auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret))

user = "GhostWhoVotes"

# first_results = twitter.statuses.user_timeline(screen_name = user)

start_time = time.time()

# dump_file = open('ghost_tweets.txt', 'w')

# for status in first_results:
# 	dump_file.write(str(status["created_at"]) + str(status["text"]) + str(status["id"]) + '\n')

# new_max = first_results[-1]["id"]

# dump_file.close()

n = 0

new_max = 455927395501867008

while n < 150:

	print 'Now scraping ' + str(n + 98) + 'th page, ' + str(np.round(time.time()-start_time,3)+171) + ' seconds elapsed...'
	results = twitter.statuses.user_timeline(screen_name = user, max_id = new_max)
	new_max = results[-1]["id"]
	with open('ghost_tweets.txt', 'a') as dump_file:
		for status in results:
			try:
				dump_file.write(str(status["created_at"]) + str(status["text"]).encode('utf-8') + str(status["id"]) + '\n')
			except UnicodeEncodeError:
				pass
	n = n+1

dump_file.close()

