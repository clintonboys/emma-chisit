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

-------------
EmmaChisit.py
-------------

The Emma Chisit model for predicting the upcoming 2016 
Australian federal election.
'''

import pandas as pd
import numpy as np
import datetime
import Polls
import Seats
import PollsterWeights
import ClusterSeats
import RunoffElection
import PollAggregator
import ApplySwings
import MarginalTrendAdjustments
import PreferenceCalculator
import SecondModel

todays_date = datetime.datetime.today()#.date()

## Import pollster weights

weights = PollsterWeights.Weights

## Import seat clusters

clusters = ClusterSeats.Clusters

## Compute poll aggregate

poll_aggregate = PollAggregator.AggregatePolls('AUS', todays_date, 30, False, ['PUP'])

## Compute implied swing

swings = PollAggregator.GetSwings('AUS', poll_aggregate, todays_date, ['PUP'])

ALP_count = 0
COA_count = 0

results2013 = SecondModel.LoadNationalSimple(2013)
for seat in results2013:
	pref_flows = PreferenceCalculator.ComputePreferences(seat.results(2013))
	after_swing = ApplySwings.ApplySwings(seat,2013,swings,pref_flows)

	## adjust all swings for marginal seat adjustments by cluster

	## add further adjustments for personal member effects and minor parties

	if RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows)) > 50.0:
		ALP_count += 1
	else:
		COA_count += 1

print ALP_count
print COA_count





