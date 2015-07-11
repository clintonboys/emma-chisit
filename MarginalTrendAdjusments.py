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

def LoadMarginals(year):

	tweets = pd.read_csv('data/ghost_who_votes/marginals_'+str(year)+'.csv')
	tweets.columns = ['n','date','pollster','seat','ALP_TPP','COA_TPP']
	polls = []

	for i in range(0,len(tweets)):
		this_poll = Polls.Poll(tweets.pollster[i], tweets.seat[i], tweets.date[i], 500, {},
		                      {'ALP': tweets.ALP_TPP[i], 'COA': tweets.COA_TPP[i]})
		polls.append(this_poll)

	return polls

print LoadMarginals(year)





