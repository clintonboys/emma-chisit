'''
FirstModel.py
-------------
This basic model assumes a four-party system, and applies
the national implied swings on a seat by seat level. 

'''

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

# basic_pref_flows = {'GRN': {'ALP': 83.03, 'COA': 16.97, 'OTH': 0},
# 					'OTH': {'ALP': 46.50, 'COA': 53.50, 'GRN': 0},
# 					'COA' :{'ALP': 9.21, 'COA': 90.79, 'GRN': 0},
# 					'ALP': {'COA': 0, 'GRN':0, 'OTH': 0}}

prefs = pd.read_csv('data/election_data/fed_2013/pref_ag.csv')

basic_pref_flows = {'COA' :{'ALP': 9.21, 'COA': 90.79, 'GRN': 0},
					'ALP': {'COA': 0, 'GRN':0, 'OTH': 0}}

for i in range(0,len(prefs)):
	basic_pref_flows[prefs['party'][i]] = {'ALP': prefs['to_alp'][i], 'COA': prefs['to_coa'][i]}

aus_results_2010 = LoadResultsByPP.LoadPPResults(2010, 'AUS', True)

nsw_results_seats_2010, nsw_results_pp_2010 = aus_results_2010[0]
act_results_seats_2010, act_results_pp_2010 = aus_results_2010[1]
nt_results_seats_2010, nt_results_pp_2010 = aus_results_2010[2]
sa_results_seats_2010, sa_results_pp_2010 = aus_results_2010[3]
wa_results_seats_2010, wa_results_pp_2010 = aus_results_2010[4]
vic_results_seats_2010, vic_results_pp_2010 = aus_results_2010[5]
qld_results_seats_2010, qld_results_pp_2010 = aus_results_2010[6]
tas_results_seats_2010, tas_results_pp_2010 = aus_results_2010[7]

results = [nsw_results_seats_2010, act_results_seats_2010, nt_results_seats_2010, sa_results_seats_2010, wa_results_seats_2010, vic_results_seats_2010, qld_results_seats_2010, tas_results_seats_2010]

for i in range(0,len(results)):
	for seat in results[i]:
		seat.AddResults(2010,LoadResultsByPP.GetSeatResults(seat,2010))
#		seat._results[2010] = MakeSeats.SeatJoinOthers(seat,2010)	

aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,6))

swing_dict = PollAggregator.GetSwings('AUS', aggregate, datetime.datetime(2013,9,6))

print swing_dict

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

error_dict = []

# print ComputeSeatSwings.ApplySwings(results[0][0], 2010, swing_dict, basic_pref_flows)
# print ComputeSeatSwings.ApplySwings(results[0][1], 2010, swing_dict, basic_pref_flows)
# print ComputeSeatSwings.ApplySwings(results[0][2], 2010, swing_dict, basic_pref_flows)


# bad_count = 0
# unable_count = 0
# for j in range(0,len(results)):
# 	for i in range(0,len(results[j])):
# #		print RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(results[j][i], 2010, swing_dict, basic_pref_flows), basic_pref_flows)
# 		try:
# 			tpp = RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(results[j][i], 2010, swing_dict, basic_pref_flows), basic_pref_flows))
# 			if j == 6:
# 				try:
# 					tpp = tpp - 5
# 				except TypeError:
# 					pass
# 			actual_tpp = actual_results[j]['alp_tpp'][i]
# 			if (tpp > 50.00) and (actual_tpp < 50.00):
# 				highlight = '************' 
# 				bad_count += 1
# 			elif (tpp < 50.00) and (actual_tpp > 50.00):
# 				highlight = '************'
# 				bad_count += 1
# 			else:
# 				highlight = ''
# 			try:
# 				if np.absolute(actual_tpp - tpp) > 4:
# 					highlight_2 = '############'
# 				else:
# 					highlight_2 = ''
# 			except TypeError:
# 				highlight_2 = ''
# 			print results[j][i].name, actual_results[j]['seat'][i], tpp, actual_tpp, highlight, highlight_2
# 			try:
# 				error_dict.append(np.absolute(tpp - float(actual_results[j]['alp_tpp'][i])))
# 			except TypeError:
# 				pass
# 		except ZeroDivisionError:
# 			print nsw_results_seats_2010[i].name, "Non TPP contest..."
# 			unable_count += 1
# 		except KeyError:
# 			print nsw_results_seats_2010[i].name, "Non TPP contest..."
# 			unable_count += 1
# print np.mean(error_dict)
# print bad_count, 'out of 150 seats predicted wrong,', unable_count, 'out of 150 unable to predict '

#print RunoffElection.Runoff(results[0][1]._results[2010], basic_pref_flows)

#print RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(results[0][1], 2010, swing_dict, basic_pref_flows), basic_pref_flows)


