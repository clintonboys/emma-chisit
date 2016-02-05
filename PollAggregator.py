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

-----------------
PollAggregator.py
-----------------

v1.0 Aggregates opinion polls (federal or state) into a single
	 aggregate adjusting for recency and for pollster accuracy.

v2.0 Improved to work with percentage data, as well as non-
	 traditional candidate combinations and inclusions of fourth
	 parties in the model. Also allows for the alteration of 
	 the federal aggregate by state poll aggregates. Some 
	 improvements to speed by primitive caching of pollster weights.

'''

import datetime
import numpy as np
import pandas as pd
import Polls
from operator import attrgetter
import PollsterWeights

def ExpDecay(days, N = 30):

	## Simple exponential decay formula to compute the weight
	## of old polls in the model. Defaults to 30 days. 

	days = getattr(days,"days",days)
	return np.round(.5 ** (float(days)/float(N)),3)	

def GetLatestElection(state, to_date):

	## For a given state and a given date, returns the most recent
	## election to that date. 

    electionframe = pd.read_csv('data/election_data/elections_from_2000.csv')
    election_data = []
    parties = electionframe.columns[2:-2]

    for i in range(0,len(electionframe)):
        if (electionframe['State'][i] == state) and (pd.to_datetime(electionframe['Date'][i], dayfirst = True) < to_date):
        	results_dict = {}
	        for party in parties:
	            if not np.isnan(electionframe[party][i]):
	                results_dict[party] = electionframe[party][i]
	        election_data.append(Polls.Election('Election', electionframe['State'][i], 
	                             pd.to_datetime(electionframe['Date'][i],dayfirst=True), 
	                             electionframe['N'][i], results_dict, electionframe['ALP_TPP'][i]))

    date = max([election.election_date() for election in election_data])
    this_election = None
    for election in election_data:
    	if election.election_date() == date:
    		this_election = election
    #print this_election.results()
    return this_election

def AggregatePolls(state, to_date, N = 30, compute_weights = False, others = []):

	## This function aggregates all polls for the given state up to the 
	## given date. The optional argument N, which defaults to a month
	## (the optimal period according to Nate Silver), gives how many days
	## backwards from to_date the model looks for polls. 

	## Unless we need to recompute them, the weights are stored in a
	## static vector in PollsterWeights, as they take around 10s to
	## compute. 

	if compute_weights:
		weightings = PollsterWeights.ComputePollsterWeights()
	else:
		weightings = PollsterWeights.Weights

	poll_data = Polls.LoadPolls(state)

	## We only need to consider polls within the window. 

	relevant_polls = []

	from_date = to_date - datetime.timedelta(days=N)

	for poll in poll_data:
		if to_date >= poll.median_date() >= from_date:
			relevant_polls.append(poll)

	# for poll in relevant_polls:
	# 	poll.join_coalition()
	# 	poll.join_others(others)

	aggregate = {}
	results_list = {}

	for poll in relevant_polls:
		for party in poll._results:
			results_list[party] = np.round(
					np.sum(
						np.trim_zeros(np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])*
						np.array([poll.results(party) for poll in relevant_polls]))/(np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls]))[np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])*
						np.array([poll.results(party) for poll in relevant_polls]) > 0].sum()),2)

    ## Since any fourth party will take votes from the others column,
    ## we now correct for this (in a fairly ad hoc way). 

	aggregated_poll = Polls.Poll('Aggregate', state, (to_date - from_date)/2, 0, results_list, None, others)
	change = sum([aggregated_poll.results()[party] for party in aggregated_poll.results()])
	old_others = aggregated_poll.results('OTH')
	aggregated_poll.change_result('OTH', old_others -change + 100)

	#print aggregated_poll.results()
	return aggregated_poll

def GetSwings(state, aggregated_poll, to_date, others, from_date = None):

	latest_election = GetLatestElection(state, to_date)
	#print latest_election.results()

	latest_election.join_coalition()
	latest_election.join_others(others)

	swing_dict = {}

	for party in aggregated_poll.results():
		swing_dict[party] = np.round(aggregated_poll.results(party) - latest_election.results(party),3)

	return swing_dict

#print AggregatePolls('AUS',datetime.datetime(2016,2,5),30).results()
# print GetSwings('AUS', AggregatePolls('AUS',datetime.datetime(2016,1,23),50), datetime.datetime(2016,1,23), ['OTH'])

# print GetSwings('WA', AggregatePolls('WA', datetime.datetime(2013,9,7), 300, False, ['PUP']), datetime.datetime(2013,9,7), ['PUP'])
# print GetSwings('NSW', AggregatePolls('NSW', datetime.datetime(2013,9,7), 300, False, ['PUP']), datetime.datetime(2013,9,7), ['PUP'])
# print GetSwings('VIC', AggregatePolls('VIC', datetime.datetime(2013,9,7), 300, False, ['PUP']), datetime.datetime(2013,9,7), ['PUP'])
# print GetSwings('SA', AggregatePolls('SA', datetime.datetime(2013,9,7), 300, False, ['PUP']), datetime.datetime(2013,9,7), ['PUP'])
# print GetSwings('QLD', AggregatePolls('QLD', datetime.datetime(2013,9,7), 300, False, ['PUP']), datetime.datetime(2013,9,7), ['PUP'])

