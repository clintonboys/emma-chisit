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

database = 'poll_database.csv'

data = pd.read_csv('test_dump.csv')
#new_frame = pd.DataFrame(columns = ['tweet_id','time','poll_source','pollster','state','primary','ALP','COA','GRN','OTH'])
for i in range(61,500):
	if 'counted):' not in data['tweet_text'][i].split(' ')[1:]:
		if data['tweet_text'][i].split(' ')[0][0] == '#':   #If the tweet starts with a hashtag it will be a poll; otherwise a retweet (@)
			#print data['tweet_text'][i].split(' ')[0]
			words = data['tweet_text'][i].split(' ')[1:]
			pollster = data['tweet_text'][i].split(' ')[0][1:]
			#if 'State' in words:  # This is a state poll
			#	print words
			#elif 'Preferred' in words: # This is a leadership poll
			#	print words
			if 'Federal' in words:
				state = 'Federal'
			elif 'State' in words:
				state = words[words.index('State')-1]     # This is a federal poll
			if 'Primary' in words: # This is a primary poll
				OTH = 0
				try:
					COA = words[words.index('L/NP')+1]
					words.remove(COA)
					COA = float(COA)
					words.remove('L/NP')
				except:
					try:
						COA = words[words.index('LIB')+1]
						words.remove(COA)
						COA = float(COA)
						words.remove('LIB')
					except:
						try:
							COA = words[words.index('LNP')+1]
							words.remove(COA)
							COA = float(COA )
							words.remove('LNP')
						except:
							COA = 0
							print words

				try:
					ALP = words[words.index('ALP')+1]
					words.remove(ALP)
					ALP = float(ALP)
					words.remove('ALP')
				except:
					ALP = 0
					print words
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
				with open(database, 'a') as f:
					f.write('ghost,'+pollster+','+str(data['time'][i])+',Federal,true,'+str(ALP)+','+str(COA)+','+str(GRN)+','+str(OTH)+','+str(data['tweet_id'][i])+'\n')
			elif '2' in words:  # This is a TPP poll
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
				with open(database, 'a') as f:
				 	f.write('ghost,'+pollster+','+str(data['time'][i])+','+state+',false,'+str(ALP)+','+str(COA)+',N/A,N/A,'+str(data['tweet_id'][i])+'\n')
			# elif 'State' in words:
			# 	print words
				#elif ['2','Party','Preferred'] in words:
					#print words