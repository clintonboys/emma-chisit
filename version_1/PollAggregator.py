''' 
PollAggregator.py
-----------------

Specify a state (or Australia) and a date. 
The aggregator will combine together all polls
from that state (or Australia) into a single
collection of primary vote figures. 

The aggregator will account for pollster 
accuracy using PollsterWeightings.py, and for recency
using a simple exponential decay weighting. 

For Australian federal elections, there is
an option to also consider state polls to obtain
state-by-state breakdowns of the primary vote. In each
state, the state poll aggregate is included with 
a particular weight; the best weight to use
is determined by referring to historical data
(see HistoricalStatePollWeights.py).
'''

import datetime
import numpy as np
import pandas as pd
import LoadData
import PollsterWeightings

state = 'AUS'
four_parties = ['ALP', 'COA', 'GRN', 'OTH']

def ExpDecay(days, N = 30):

	## Simple exponential decay formula to compute the weight
	## of old polls in the model. 

	days = getattr(days,"days",days)
	return np.round(.5 ** (float(days)/float(N)),3)	

def GetLatestElection(state, to_date):

	## For a given state and a given date, returns the most recent
	## election to that date. 

	election_data = LoadData.LoadElections()

	relevant_elections = []
	for election in election_data:
		if (election.state() == state):
			if election.election_date() < to_date:
				relevant_elections.append(election)

	date = datetime.datetime(1900,1,1)
	latest_election = None

	for election in relevant_elections:
		if election.election_date() > date:
			date = election.election_date()
			latest_election = election
	return latest_election

def AggregatePolls(state, to_date, N = 30):

	## This function aggregates all polls for the given state up to the 
	## given date. The optional argument N, which defaults to a month
	## (the optimal period according to Nate Silver), gives how many days
	## backwards from to_date the model looks for polls. 

	poll_data = LoadData.LoadPolls(state)

	relevant_polls = []

	from_date = to_date - datetime.timedelta(days=N)

	for poll in poll_data:
		if to_date >= poll.median_date() >= from_date:
			relevant_polls.append(poll)

	for poll in relevant_polls:
#		print poll._results['ALP']
		poll._results = LoadData.JoinCoalition(poll)
		poll._results = LoadData.JoinOthers(poll)

	weightings = PollsterWeightings.ComputePollsterWeights()

	aggregate = {}
	results_list = {}

	for poll in relevant_polls:
		for party in poll._results:
			results_list[party] = np.round(
					np.sum(
						np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])*
						np.array([poll.results(party) for poll in relevant_polls])/(np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])).sum()),2)

	aggregated_poll = LoadData.Poll('Aggregate', state, (to_date - from_date)/2, 0, results_list, {})
	return aggregated_poll

def GetSwings(state, aggregated_poll, to_date):

	latest_election = GetLatestElection(state, to_date)

	latest_election._results = LoadData.JoinOthers(latest_election)
	latest_election._results = LoadData.JoinCoalition(latest_election)

	swing_dict = {}

	for party in latest_election._results:
		swing_dict[party] = np.round(aggregated_poll.results(party) - latest_election.results(party),3)

	return swing_dict