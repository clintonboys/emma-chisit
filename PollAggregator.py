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

to_date = datetime.datetime(2015,1,28) 
state = 'QLD'
N=30
four_parties = ['ALP', 'COA', 'GRN', 'OTH']

def ExpDecay(days,N):
	days = getattr(days,"days",days)
	return np.round(.5 ** (float(days)/float(N)),3)	

poll_data = LoadData.LoadPolls(state)
election_data = LoadData.LoadElections()
relevant_polls = []

def GetLatestElection(state, to_date):
	date = datetime.datetime(1900,1,1)
	latest_election = None
	for election in election_data:
		if (election.state() == state) and (election.election_date() > date > to_date):
			date = election.election_date()
			latest_election = election
	return latest_election

def AggregatePolls(state, to_date, N):

	from_date = to_date - datetime.timedelta(days=N)

	for poll in poll_data:
		if to_date >= poll.median_date() >= from_date:
			relevant_polls.append(poll)

	for poll in relevant_polls:
		PollsterWeightings.JoinCoalition(poll)
		PollsterWeightings.JoinOthers(poll)

	weightings = PollsterWeightings.ComputePollsterWeights()

	aggregate = {}
	results_list = {}

	for party in four_parties:
		for poll in relevant_polls:
			results_list[party] = np.round(
					np.sum(
						np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])*
						np.array([poll.results(party) for poll in relevant_polls])/(np.array([weightings[poll.pollster] for poll in relevant_polls])*
						np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])).sum()),2)

	aggregated_poll = LoadData.Poll('Aggregate', state, (to_date - from_date)/2, 0, results_list, {})
	return aggregated_poll

def GetSwings(state, aggregated_poll):
	latest_election = GetLatestElection(state)

	print latest_election.election_date()

	PollsterWeightings.JoinOthers(latest_election)
	PollsterWeightings.JoinCoalition(latest_election)

	swing_dict = {}

	for party in four_parties:
		swing_dict[party] = np.round(aggregated_poll.results(party) - latest_election.results(party),3)

	return swing_dict
	
print GetSwings(state,AggregatePolls(state, to_date, N))

#print GetSwings(state)




