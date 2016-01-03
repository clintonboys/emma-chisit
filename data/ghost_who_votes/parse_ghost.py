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

data = pd.read_csv('test_dump.csv')
new_frame = pd.DataFrame(columns = ['tweet_id','time','poll_source','pollster','state','primary','ALP','COA','GRN','OTH'])
for i in range(0,1928):
	if data['tweet_text'][i].split(' ')[0][0] == '#':   #If the tweet starts with a hashtag it will be a poll; otherwise a retweet (@)
		#print data['tweet_text'][i].split(' ')[0]
		words = data['tweet_text'][i].split(' ')[1:]
		#if 'State' in words:  # This is a state poll
		#	print words
		#elif 'Preferred' in words: # This is a leadership poll
		#	print words
		if 'Federal' in words:     # This is a federal poll
			if 'Primary' in words: # This is a primary poll
				OTH = 0
				try:
					COA = words[words.index('L/NP')+1]
					words.remove(COA)
					COA = float(COA)
					words.remove('L/NP')
				except:
					COA = 0
				try:
					ALP = words[words.index('ALP')+1]
					words.remove(ALP)
					ALP = float(ALP)
					words.remove('ALP')
				except:
					ALP = 0
				try:
					GRN = words[words.index('GRN')+1]
					words.remove(GRN)
					GRN = float(GRN)
					words.remove('GRN')
				except: 
					GRN = 0
				for party in ['PUP','NAT','IND']:
					if party in words:
						OTH += float(words[words.index(party)+1])
				print COA, ALP, GRN, OTH
