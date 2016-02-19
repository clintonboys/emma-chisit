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
import os

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
results_frame = pd.DataFrame(columns = ['seat','state','winner','TPP'])
seats = []
states = []
winners = []
TPPs = []

results2013 = SecondModel.LoadNationalSimple(2013)
for seat in results2013:
	pref_flows = PreferenceCalculator.ComputePreferences(seat.results(2013))
	after_swing = ApplySwings.ApplySwings(seat,2013,swings,pref_flows)
	if seat.name == 'Fairfax':
		after_swing['PUP'] = after_swing['PUP']*2
	if seat.name in ('Denison','Indi'):
		after_swing['IND'] = after_swing['IND']*2
	if seat.name == 'Kennedy':
		after_swing['KAP'] = after_swing['KAP']*2
	## adjust all swings for marginal seat adjustments by cluster

	## add further adjustments for personal member effects and minor parties
	seats.append(seat.name)
	states.append(seat.state)
	winner, TPP = RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows), True)
	if winner in ['COA','LNP','LIB','NAT']:
		winners.append('COA')
	elif winner in ['ALP','CLP']:
		winners.append('ALP')
	else:
		winners.append(winner)
	TPPs.append(TPP)
	#TPPs.append(RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows)))

results_frame['seat'] = seats
results_frame['state'] = states
results_frame['winner'] = winners
results_frame['TPP'] = TPPs

print results_frame.groupby('winner').count()

results_frame.to_csv('current_forecast.csv')

