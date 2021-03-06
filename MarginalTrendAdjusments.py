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

---------------------------
MarginalTrendAdjustments.py
---------------------------

v1.0  Loads marginal seat data from GhostWhoVotes
	  and outputs it as a series of polls for the
	  relevant seats. 

'''

import Polls
import Seats
import RunoffElection
import pandas as pd
import numpy as np
import datetime

year = 2013

def LoadMarginals(year, seat, top_two = ['ALP', 'COA'], is_primary = False):

	tweets = pd.read_csv('data/ghost_who_votes/marginals_'+str(year)+'.csv')
	tweets.columns = ['n','date','pollster','seat','ALP_TPP','COA_TPP']
	these_tweets = tweets[tweets['seat'] == ' '+seat]
	polls = []

	if not is_primary:
		for i in range(0,len(these_tweets)):
			this_poll = Polls.Poll(these_tweets.pollster.iloc[i], these_tweets.seat.iloc[i], these_tweets.date.iloc[i], 500, {},
			                      {top_two[0]: these_tweets.ALP_TPP.iloc[i], top_two[1]: these_tweets.COA_TPP.iloc[i]})
			polls.append(this_poll)
	else:
		for i in range(0,len(these_tweets)):
			this_poll = Polls.Poll(these_tweets.pollster.iloc[i], these_tweets.seat.iloc[i], these_tweets.date.iloc[i], 500, 
				{top_two[0]: these_tweets.ALP_TPP.iloc[i], top_two[1]: these_tweets.COA_TPP.iloc[i], 'OTH': 100.0-these_tweets.ALP_TPP.iloc[i]-these_tweets.COA_TPP.iloc[i]},
				{})
			polls.append(this_poll)

	return polls

def AdjustSwing(seat, aggregated_poll, marginal_poll, year):

	## Given a marginal seat, this function computes the adjusment
	## to the swing from that implied by the poll aggregate, using
	## a seat-level poll. 

	seat_results = seat.results(year)

print LoadMarginals(2013, 'Melbourne', ['ALP', 'GRN'], True)[0].results()
print LoadMarginals(2013, 'Corangamite')[0].tpp()




