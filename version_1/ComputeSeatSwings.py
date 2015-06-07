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
1.0 	Everything is written to work in the 
		four-party model. Currently applies nationwide
		swing to each seat. 

'''

import LoadData
import MakeSeats
import LoadResultsByPP
import PollsterWeightings
import RunoffElection
import PollAggregator

import pandas as pd
import numpy as np
import datetime

def ApplySwings(seat, year, swing_dict, pref_dict):

	## Applies the swings calculated in swing_dict, using preference
	## flows in pref_dict, to the seat seat in year year. For example, 
	## compute a swing from a poll aggregate and apply this to the 
	## previous election's results to obtain the implied result for 
	## this seat by the nationwide swing. 

	seat._results[year] = MakeSeats.SeatJoinCoalition(seat,year)
	#seat._results[year] = MakeSeats.SeatJoinOthers(seat,year)

	#old_results = RunoffElection.Runoff(seat._results[year], pref_dict, True)

	seat_votes = 0

	for party in seat._results[year]:
		try: 
			seat_votes = seat_votes + float(seat._results[year][party])
		except KeyError:
			pass

	for party in seat._results[year]:
		if party != 'Informal':
			try:
				seat._results[year][party] = int((1+0.01*swing_dict[party])*seat._results[year][party])
			except KeyError:
				seat._results[year][party] = int((1+0.01*swing_dict['OTH'])*seat._results[year][party])



	#new_results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)

	return seat._results[year]