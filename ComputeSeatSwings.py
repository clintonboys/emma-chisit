'''
ComputeSeatSwings.py
--------------------

Using historical election data and the 
poll aggregator, we compute implied swings
for each seat in terms of popular vote, and 
then perform runoffs to get two-party-preferred
totals for each seat. 

'''

'''
Version history
---------------
1.0 	Will work only for contests where the 
		dominant parties are ALP and LP, and 
		will not use clustering or the strong
		transition model. 
'''

import LoadData
import MakeSeats
import LoadResultsByPP
import PollsterWeightings
import RunoffElection
#import ClusterSeats
import PollAggregator

import pandas as pd
import numpy as np
import datetime

state = 'AUS'
to_date = datetime.datetime(2013,9,6) 
N = 30
year = 2010
current_national_swings = PollAggregator.GetSwings(state, PollAggregator.AggregatePolls(state, to_date, N))

aus_results_2010 = LoadResultsByPP.LoadPPResults(2010, 'AUS', True)

nsw_results_seats_2010, nsw_results_pp_2010 = aus_results_2010[0]

for seat in nsw_results_seats_2010:
	seat.AddResults(year,LoadResultsByPP.GetSeatResults(seat,year))

for seat in nsw_results_seats_2010:
	PollsterWeightings.JoinOthersResults(seat._results[year])

basic_pref_flows = {'GRN': {'ALP': 80.00, 'LP': 20.00, 'OTH': 0, 'NP': 0.00},
					'OTH': {'ALP': 45.00, 'LP': 50.00, 'GRN': 0, 'NP': 5.00},
					'NP' :{'ALP': 15.00, 'LP': 80.00, 'GRN': 2.00, 'OTH': 3.00},
					'ALP': {'LP': 0, 'GRN':0, 'OTH': 0, 'NP': 0.00},
					'LP': {'ALP': 0, 'GRN':0, 'OTH': 0, 'NP': 100.00}}

seat = nsw_results_seats_2010[13]

print seat._name
print seat._results[2010]
old_results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)

print old_results

'''
ApplySwings takes as input a seat, a year which 
the election results are taken from (the previous election),
and a dictionary of swings for the four major
parties (ALP, LP, GRN and OTH). 
'''

def ApplySwings(seat, state, year, swing_dict):

	swing_dict['LP'] = swing_dict.pop('COA')  ## Make all of this consistent across the 
											  ## various modules. 


	old_results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)

	seat_votes = 0

	for party in ['ALP', 'LP', 'GRN', 'OTH']:
		try: 
			seat_votes = seat_votes + float(seat._results[year][party])
		except KeyError:
			pass

	for party in current_national_swings:
		seat._results[year][party] = int(seat._results[year][party] + 0.01*current_national_swings[party]*seat_votes)

	new_results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)

	print seat._name, '2010', 'ALP TPP estimate: ', np.round(100*(float(old_results['ALP']) / (float(old_results['ALP']) + float(old_results['LP']))),3)
	print seat._name, '2013', 'ALP TPP estimate: ', np.round(100*(float(new_results['ALP']) / (float(new_results['ALP']) + float(new_results['LP']))),3)


print ApplySwings(seat, state, year, current_national_swings)

# for seat in nsw_results_seats_2010:
# 	if not 'NP' in seat._results[year]:
# 		try:
# 			seat_votes = float(seat._results[year]['ALP']) + float(seat._results[year]['LP']) + float(seat._results[year]['GRN']) + float(seat._results[year]['OTH'])			
# 			for party in current_national_swings:
# 				seat._results[year][party] += current_national_swings[party]*seat_votes
# 			try:
# 				results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)
# 				try:
# 					print seat._name, year, 'ALP TPP estimate: ', np.round(100*(float(results['ALP']) / (float(results['ALP']) + float(results['LP']))),3)
# 				except KeyError:
# 					pass
# 			except ZeroDivisionError:
# 				pass
# 		except KeyError:
# 			pass
## Adjust totals in each seat by current swings

## Perform runoffs
