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

from_date = datetime.datetime(2015,1,1) 
to_date = datetime.datetime(2015,1,31)
state = 'QLD'
N=30

def ExpDecay(days,N):
	days = getattr(days,"days",days)
	return np.round(.5 ** (float(days)/float(N)),3)

poll_data = LoadData.LoadPolls(state)
relevant_polls = []

for poll in poll_data:
	if to_date >= poll.median_date() >= from_date:
		relevant_polls.append(poll)

for poll in relevant_polls:
	PollsterWeightings.JoinCoalition(poll)
	PollsterWeightings.JoinOthers(poll)

weightings = PollsterWeightings.ComputePollsterWeights()
print weightings['Newspoll']

aggregate = {}
results_list = {}

for party in ['ALP', 'COA', 'GRN', 'OTH']:
	for poll in relevant_polls:
		# print poll.results(party)
		# print ExpDecay(to_date - poll.median_date(),N)
		# print weightings[poll.pollster]
		results_list[party] = np.round(
				np.sum(
					np.array([weightings[poll.pollster] for poll in relevant_polls])*
					np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])*
					np.array([poll.results(party) for poll in relevant_polls])/(np.array([weightings[poll.pollster] for poll in relevant_polls])*
					np.array([ExpDecay(to_date - poll.median_date(),N) for poll in relevant_polls])).sum()),2)

print results_list
print np.sum([results_list[party] for party in ['ALP', 'COA', 'GRN', 'OTH']])