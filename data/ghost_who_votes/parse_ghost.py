'''
ParseGhost.py
-------------
We parse the GhostWhoVotes twitter data which we scraped
using get_ghost.py.
'''

from datetime import datetime
import re
import pandas as pd
import os
from pandas import DataFrame

tweet_database = 'tweet_database.csv'
poll_database = 'poll_database.csv'
marginal_poll_database = 'marginal_poll_database.csv'

try:
    os.remove(poll_database)
except OSError:
    pass

if not os.path.isfile(poll_database):
	with open(poll_database, 'a') as dump_file:
		dump_file.write('source,pollster,time,state,primary,ALP,COA,GRN,OTH,tweet_id'+'\n') 

try:
    os.remove(marginal_poll_database)
except OSError:
    pass

if not os.path.isfile(marginal_poll_database):
	with open(marginal_poll_database, 'a') as dump_file:
		dump_file.write('source,pollster,time,seat,primary,ALP,COA,GRN,OTH,tweet_id'+'\n') 


data = pd.read_csv(tweet_database)
#new_frame = pd.DataFrame(columns = ['tweet_id','time','poll_source','pollster','state','primary','ALP','COA','GRN','OTH'])
tweets_parsed = 0
total_tweets = 0
for i in range(0,1500):
	if 'counted):' not in data['tweet_text'][i].split(' ')[1:] and 'USA' not in data['tweet_text'][i].split(' ')[1:]:
		if data['tweet_text'][i].split(' ')[0][0] == '#':   #If the tweet starts with a hashtag it will be a poll; otherwise a retweet (@)
			#rint data['tweet_text'][i].split(' ')[1:]
			total_tweets += 1
			words = data['tweet_text'][i].split(' ')[1:]
			pollster = data['tweet_text'][i].split(' ')[0][1:]
			if 'State' in words:  # This is a state poll
				if words[0] == 'Poll':
					state = words[1]
				else:
					state = words[0] 
				classification = 'State'
			elif 'Federal' in words:  # This is a federal poll
				classification = 'Federal'
				state = 'Federal'
			elif 'Preferred' in words and ('PM' in words or 'PM:' in words): # This is a federal leadership poll
				print 'Federal Leadership'
				classification = 'Federal Leadership'
			elif 'Preferred' in words and ('Premier' in words or 'Premier:' in words): # This is a state leadership poll
				print 'State Leadership'
				classification = 'State Leadership'
			elif 'Quarterly' in words: # This is a quarterly Newspoll
				print 'Quarterly Newspoll'
				classification = 'Quarterly Newspoll'
			elif 'Seat' in words and  'of' in words:
				print 'Marginal' # This is a marginal seat poll
				classification = 'Marginal'
			else: # This is another kind of poll, probably not relevant
				print 'Other'
				classification = 'Other'

			if classification == 'Federal':
				if 'Primary' in words: # This is a primary poll
					print 'Primary'
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
					with open(poll_database, 'a') as f:
						f.write('ghost,'+pollster+','+str(data['time'][i])+',Federal,true,'+str(ALP)+','+str(COA)+','+str(GRN)+','+str(OTH)+','+str(data['tweet_id'][i])+'\n')
						tweets_parsed += 1
				elif '2' in words:  # This is a TPP poll
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
					with open(poll_database, 'a') as f:
					 	f.write('ghost,'+pollster+','+str(data['time'][i])+','+state+',false,'+str(ALP)+','+str(COA)+',N/A,N/A,'+str(data['tweet_id'][i])+'\n')
					 	tweets_parsed += 1

			elif classification == 'Marginal':
				seat = words[words.index('of')+1].replace('#','')
				if seat == 'New':
					seat = seat + ' ' + str(words[words.index('New')+1])
				print words
				if 'Primary' in words: # This is a primary poll
					print 'Primary'
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
					with open(marginal_poll_database, 'a') as f:
						f.write('ghost,'+pollster+','+str(data['time'][i])+','+str(seat)+',true,'+str(ALP)+','+str(COA)+','+str(GRN)+','+str(OTH)+','+str(data['tweet_id'][i])+'\n')
						tweets_parsed += 1
				elif '2' in words:  # This is a TPP poll
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
					if COA == 50.0:
						ALP = 50.0
					else:
						try:
							ALP = words[words.index('ALP')+1]
							words.remove(ALP)
							ALP = float(ALP)
							words.remove('ALP')
						except:
							ALP = 0
					with open(marginal_poll_database, 'a') as f:
					 	f.write('ghost,'+pollster+','+str(data['time'][i])+','+str(seat)+',false,'+str(ALP)+','+str(COA)+',N/A,N/A,'+str(data['tweet_id'][i])+'\n')
					 	tweets_parsed += 1



print total_tweets, tweets_parsed