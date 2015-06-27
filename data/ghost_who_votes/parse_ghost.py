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

poll_dates = []
pollsters = []
poll_seat = []
ALP = []
COA = []

for i in range(0,len(tweets)):
	tweets[i] = tweets[i][:-19]
	split_tweet = tweets[i].split('+0000')
	try:
		date = split_tweet[0][:-1]+split_tweet[1][:5]
		poll_date = datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
		try:
			if poll_date.year == 2013:
				poll_data = split_tweet[1][5:].split('Poll Seat of')
				seat = poll_data[1].split(' 2 ')[0]
				results = poll_data[1].split(' 2 ')[1].split(':')[1]
				pollster = poll_data[0][1:]
				if results[1] == 'A':
					these_results = re.sub(r' (ALP) (\d\d.?\d?) (LIB) (\d\d.?\d?) #?\w+', r'\2, \4', results)
					poll_dates.append(poll_date)
					pollsters.append(pollster)
					poll_seat.append(seat)
					ALP.append(these_results.split(',')[0])
					COA.append(these_results.split(',')[1])
				elif results[1:3] == 'LI':
					these_results = re.sub(r' (LIB) (\d\d.?\d?) (ALP) (\d\d.?\d?) #?\w+', r'\4, \2', results)
					poll_dates.append(poll_date)
					pollsters.append(pollster)
					poll_seat.append(seat)
					ALP.append(these_results.split(',')[0])
					COA.append(these_results.split(',')[1])
				elif results[1:3] == 'LN':
					these_results = re.sub(r' (LNP) (\d\d.?\d?) (ALP) (\d\d.?\d?) #?\w+', r'\4, \2', results)
					poll_dates.append(poll_date)
					pollsters.append(pollster)
					poll_seat.append(seat)
					ALP.append(these_results.split(',')[0])
					COA.append(these_results.split(',')[1])
				elif results[1:3] == 'L/':
					these_results = re.sub(r' (L/NP) (\d\d.?\d?) (ALP) (\d\d.?\d?) #?\w+', r'\4, \2', results)
					poll_dates.append(poll_date)
					pollsters.append(pollster)
					poll_seat.append(seat)
					ALP.append(these_results.split(',')[0])
					COA.append(these_results.split(',')[1])
				else:
					pass
		except IndexError:
			pass
	except IndexError:
		pass

data = pd.DataFrame(poll_dates)
data['pollster'] = pollsters
data['seat'] = poll_seat
data['ALP_TPP'] = ALP
data['COA_TPP'] = COA

data.to_csv('marginals_2013.csv')