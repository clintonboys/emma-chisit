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
nsw_seats, nsw_polling_places = aus_results_2010[0]

for seat in act_seats:
	seat.AddResults(year,LoadResultsByPP.GetSeatResults(seat,year))

print act_seats[0].results(2010, 'ALP')
print act_seats[0].results(2010)

basic_pref_flows = {'GRN': {'ALP': 80.00, 'LIB': 20.00},
					'ALP': {'GRN': 60.00, 'LIB': 40.00},
					'LIB': {'ALP': 60.00, 'GRN': 40.00}}

print RunoffElection.Runoff(act_seats[0].results(2010), basic_pref_flows)

# for seat in act_seats:
# 	PollsterWeightings.JoinOthersResults(seat._results[year])

# basic_pref_flows = {'GRN': {'ALP': 80.00, 'LIB': 20.00, 'OTH': 0},
# 					'OTH': {'ALP': 45.00, 'LIB': 55.00, 'GRN': 0},
# 					'ALP': {'LIB': 0, 'GRN':0, 'OTH': 0},
# 					'LIB': {'ALP': 0, 'GRN':0, 'OTH': 0}}

# for seat in act_seats:
# 	results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)
# 	print seat._name, year, 'ALP TPP estimate: ', np.round(100*(float(results['ALP']) / (float(results['ALP']) + float(results['LIB']))),3)

# print '\n'

# for seat in nsw_seats:
# 	seat.AddResults(year,LoadResultsByPP.GetSeatResults(seat,year))

# for seat in nsw_seats:
# 	PollsterWeightings.JoinOthersResults(seat._results[year])

# basic_pref_flows = {'GRN': {'ALP': 80.00, 'LP': 20.00, 'OTH': 0, 'NP': 0.00},
# 					'OTH': {'ALP': 45.00, 'LP': 50.00, 'GRN': 0, 'NP': 5.00},
# 					'NP' :{'ALP': 15.00, 'LP': 80.00, 'GRN': 2.00, 'OTH': 3.00},
# 					'ALP': {'LP': 0, 'GRN':0, 'OTH': 0, 'NP': 0.00},
# 					'LP': {'ALP': 0, 'GRN':0, 'OTH': 0, 'NP': 100.00}}

# for seat in nsw_seats:
# 	#print seat._name, seat._results[year]
# 	results = RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)
# 	try:
# 		print seat._name, year, 'ALP TPP estimate: ', np.round(100*(float(results['ALP']) / (float(results['ALP']) + float(results['LP']))),3)
# 	except TypeError:
# 		print seat._name, year, 'ALP TPP estimate: ', np.round(100*(float(results['ALP']) / (float(results['ALP']) + float(results['NP']))),3)
