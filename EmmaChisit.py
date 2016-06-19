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
from config import independent_seats, sophomore_seats, retiring_seats

todays_date = datetime.datetime.today()#.date()
#print todays_date

## Import pollster weights

weights = PollsterWeights.Weights

## Import seat clusters

clusters = ClusterSeats.Clusters

## Compute poll aggregate

poll_aggregate = PollAggregator.AggregatePolls('AUS', todays_date, 30, False, ['NXT'])

print poll_aggregate.results()
## Compute implied swing

swings = PollAggregator.GetSwings('AUS', poll_aggregate, todays_date, ['NXT'])
#print swings
swings = {'COA': -5.5, 'GRN': 3.0, 'ALP': -0.02, 'PUP': -99.9, 'OTH':5}


ALP_count = 0
COA_count = 0
results_frame = pd.DataFrame(columns = ['seat','state','winner','TPP'])
seats = []
states = []
winners = []
TPPs = []

## adjust swing for marginal polls
from_date = todays_date - datetime.timedelta(days=30)

results2013 = SecondModel.LoadNationalSimple(2013)

marginal_dict = {}

for seat in results2013:

	marginal_polls = MarginalTrendAdjustments.LoadMarginals(todays_date, seat.name)
	if marginal_polls:
		marginal_polls = [poll for poll in marginal_polls if datetime.datetime.strptime(poll.median_date(), '%Y-%m-%d %H:%M:%S') > from_date ]
		if len(marginal_polls) > 0:
			min_date = min(poll.median_date() for poll in marginal_polls)
			most_recent_marginal = [poll for poll in marginal_polls if poll.median_date() == min_date][0]

			for i in range(0,len(clusters)):
				if seat.name in clusters[i]:
					this_cluster = i
			try:
				marginal_dict[this_cluster].append(most_recent_marginal)
			except:
				marginal_dict[this_cluster] = [most_recent_marginal]
#print marginal_dict

for cluster in marginal_dict:
	if len(marginal_dict[cluster]) > 1:
		averaged_poll = {'ALP':0.0, 'COA':0.0}
		for poll in marginal_dict[cluster]:
			averaged_poll['ALP'] += poll.results()['ALP']
			averaged_poll['COA'] += poll.results()['COA']
		averaged_poll['ALP'] = averaged_poll['ALP']/float(len(marginal_dict[cluster]))
		averaged_poll['COA'] = averaged_poll['COA']/float(len(marginal_dict[cluster]))
		marginal_dict[cluster] = [averaged_poll]
	elif len(marginal_dict[cluster]) == 1:
		marginal_dict[cluster] = [marginal_dict[cluster][0].results()]

for seat in results2013:
	pref_flows = PreferenceCalculator.ComputePreferences(seat.results(2013))
	after_swing = ApplySwings.ApplySwings(seat,2013,swings,pref_flows)
	# if seat.name == 'Fairfax':
	# 	after_swing['PUP'] = after_swing['PUP']*2
	# if seat.name in ('Denison','Indi'):
	# 	after_swing['IND'] = after_swing['IND']*2
	# if seat.name == 'Kennedy':
	# 	after_swing['KAP'] = after_swing['KAP']*2
	## adjust all swings for marginal seat adjustments by cluster

	## add further adjustments for personal member effects and minor parties

	for retiring_seat in retiring_seats:
		if retiring_seat == seat.name:
			after_swing[retiring_seats[retiring_seat]] = after_swing[retiring_seats[retiring_seat]]*0.9

	for sophomore_seat in sophomore_seats:
		if sophomore_seat == seat.name:
			after_swing[sophomore_seats[sophomore_seat]] = after_swing[sophomore_seats[sophomore_seat]]*1.1

	for independent_seat in independent_seats:
		if independent_seat == seat.name:
			after_swing[independent_seats[independent_seat]] = after_swing[independent_seats[independent_seat]]*2


	seats.append(seat.name)
	states.append(seat.state)
	winner, TPP = RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows, False, True), True)
	print winner, TPP
	if winner in ['COA','LNP','LIB','NAT']:
		winner = 'COA'
		prelim_results = {'COA': TPP, 'ALP': 100-TPP}
	elif winner in ['ALP','CLP']:
		winner = 'ALP'
		prelim_results = {'COA':100-TPP, 'ALP':TPP}
	# if winner in ['ALP','COA']:
	# 	for i in range(0,len(clusters)):
	# 		if seat.name in clusters[i]:
	# 			this_cluster = i
	# 	if this_cluster in marginal_dict:
	# 		#print marginal_dict[this_cluster]
	# 		prelim_results['COA'] += marginal_dict[this_cluster][0]['COA']
	# 		prelim_results['ALP'] += marginal_dict[this_cluster][0]['ALP']
	# 		prelim_results['COA'] = prelim_results['COA']/2.0
	# 		prelim_results['ALP'] = prelim_results['ALP']/2.0
	# 	TPP = max([prelim_results[party] for party in ['ALP','COA']])
	# 	winner = [key for key, value in prelim_results.iteritems() if value == TPP][0]

	TPPs.append(TPP)
	winners.append(winner)
	#TPPs.append(RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows)))

results_frame['seat'] = seats
results_frame['state'] = states
results_frame['winner'] = winners
results_frame['TPP'] = TPPs

print results_frame.groupby('winner').count()

results_frame.to_csv('current_forecast.csv')

