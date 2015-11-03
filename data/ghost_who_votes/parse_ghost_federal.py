'''
ParseGhost.py
-------------
We parse the GhostWhoVotes twitter data which we scraped
using get_ghost.py.
'''

from datetime import datetime
import re
import pandas as pd
from pandas import DataFrame

with open('ghost_tweets.txt') as f:
	tweets = f.readlines()

pattern_old = r'L/NP\s(\d*)\s(\((\-|\+)?\d\))\sALP\s(\d*)\s(\((\-|\+)?\d\))(\s(\S*)\s(\d*)\s(\((\-|\+)?\d\)))*'
pattern_old2 = r'L/NP\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))\sALP\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))(\s(\S*)\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\)))*'
pattern = r'L/NP\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))\sALP\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))(\s(\S*)(\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))))?(\s(\S*)(\s(\d{1,2}\.?\d?)\s(\((\-|\+)?\d\.?\d?\))))?'

for i in range(0,1000):
	try:
		date, tweet = tweets[i].split('+0000 ')
	except ValueError:
		#print tweet
		pass
	date = date + tweet[0:4]
	tweet = tweet[4:]
	if 'Poll' in tweet.split(' '):
		poll_type = tweet.split(':')[0]
		try:
			poll_results = tweet.split(':')[1]
		except IndexError:
			#print tweet
			pass
		pollster = poll_type.split(' ')[0][1:]
		poll_type = ' '.join(poll_type.split(' ')[2:])
		if poll_type == 'Federal Primary Votes':
			match = re.search(pattern, poll_results)
			if match:
				#print len(re.findall(pattern, poll_results))
				#print poll_results
				results_dict = {}
				results_dict['COA'] = match.group(1)
				results_dict['ALP'] = match.group(4)
				next_res = match.group(7).split(' ')
				results_dict[next_res[1]] = next_res[2]
				if match.group(13) is not None:
					final_res = match.group(13).split(' ')
					results_dict[final_res[1]] = final_res[2]
			else:
				#COA_res = 0
				print poll_results
			print date, '|', pollster, '|', poll_type, '|', results_dict