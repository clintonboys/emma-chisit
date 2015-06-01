import pandas as pd
import numpy as np
import datetime
import LoadData
import MakeSeats
import LoadResultsByPP
import PollsterWeightings
import RunoffElection
import PollAggregator
import ComputeSeatSwings

prefs = pd.read_csv('data/election_data/fed_2013/pref_ag.csv')

basic_pref_flows = {'COA' :{'ALP': 9.21, 'COA': 90.79, 'GRN': 0},
					'ALP': {'COA': 0, 'GRN':0, 'OTH': 0}}

for i in range(0,len(prefs)):
	basic_pref_flows[prefs['party'][i]] = {'ALP': prefs['to_alp'][i], 'COA': prefs['to_coa'][i]}

aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,6))
swing_dict = PollAggregator.GetSwings('AUS', aggregate, datetime.datetime(2013,9,6))

seats = LoadResultsByPP.LoadNationalSimple(2010)

#barton = seats[3]

# print barton._results[2010]
# print RunoffElection.GetTPP(RunoffElection.Runoff(barton._results[2010], basic_pref_flows))
# print RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(barton, 2010, swing_dict, basic_pref_flows), basic_pref_flows))

nsw_results = pd.read_csv('data/election_data/fed_2013/tpp_nsw.csv')
nsw_results.columns = ['seat', 'alp_tpp']
act_results = pd.read_csv('data/election_data/fed_2013/tpp_act.csv')
act_results.columns = ['seat', 'alp_tpp']
nt_results = pd.read_csv('data/election_data/fed_2013/tpp_nt.csv')
nt_results.columns = ['seat', 'alp_tpp']
sa_results = pd.read_csv('data/election_data/fed_2013/tpp_sa.csv')
sa_results.columns = ['seat', 'alp_tpp']
wa_results = pd.read_csv('data/election_data/fed_2013/tpp_wa.csv')
wa_results.columns = ['seat', 'alp_tpp']
vic_results = pd.read_csv('data/election_data/fed_2013/tpp_vic.csv')
vic_results.columns = ['seat', 'alp_tpp']
qld_results = pd.read_csv('data/election_data/fed_2013/tpp_qld.csv')
qld_results.columns = ['seat', 'alp_tpp']
tas_results = pd.read_csv('data/election_data/fed_2013/tpp_tas.csv')
tas_results.columns = ['seat', 'alp_tpp']

actual_results = [nsw_results, act_results, nt_results, sa_results, wa_results, vic_results, qld_results, tas_results]

results2013 = pd.concat(actual_results)

count = 0

# for seat in seats:
# 	try:
# 		actual = results2013[results2013['seat'] == seat.name]['alp_tpp'].iloc[0]
# 		count = count +1
# 	except IndexError:
# 		print "No name..."
# 		actual = 0
# 	print actual
# 	estimated = RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(seat, 2010, swing_dict, basic_pref_flows), basic_pref_flows))
# 	print estimated
# 	if np.absolute(float(actual) - float(estimated)) > 4.00:
# 		highlight1 = '#######'
# 	else:
# 		highlight1 = ''
# 	if type(estimated) is float:
# 		if (actual > 50.00) and (estimated < 50.00):
# 			highlight = '*******' 
# 		elif (actual < 50.00) and (estimated > 50.00):
# 			highlight = '*******'
# 		else:
# 			highlight = ''
# 	else:
# 		highlight = ''
# 	print seat.name, ' | Actual 2013 TPP: ', actual, ' | Estimated TPP: ', estimated, highlight, ' ', highlight1
# print count

print seats[31].name
print seats[31]._results[2010]
swinged = ComputeSeatSwings.ApplySwings(seats[31], 2010, swing_dict, basic_pref_flows)
print RunoffElection.GetTPP(RunoffElection.Runoff(swinged, basic_pref_flows))
