import LoadData
import MakeSeats
import LoadResultsByPP
import PollsterWeightings
import RunoffElection
#import ClusterSeats
import PollAggregator

import pandas as pd
import numpy as np

year = 2010

aus_results_2010 = LoadResultsByPP.LoadPPResults(2010, 'AUS', True)

act_seats, act_polling_places = aus_results_2010[1]

for seat in act_seats:
	seat.AddResults(year,LoadResultsByPP.GetSeatResults(seat,year))

for seat in act_seats:
	PollsterWeightings.JoinOthersResults(seat._results[year])

basic_pref_flows = {'GRN': {'ALP': 80.00, 'LIB': 20.00, 'OTH': 0},
					'OTH': {'ALP': 45.00, 'LIB': 55.00, 'GRN': 0},
					'ALP': {'LIB': 0, 'GRN':0, 'OTH': 0},
					'LIB': {'ALP': 0, 'GRN':0, 'OTH': 0}}

for seat in act_seats:
	results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)
	print seat._name, year, 'ALP TPP estimate: ', np.round(100*(float(results['ALP']) / (float(results['ALP']) + float(results['LIB']))),3)
