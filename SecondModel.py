'''
SecondModel.py
-------------
This basic model assumes a four-party system, and applies
the national implied swings on a seat by seat level. 

'''

import pandas as pd
import numpy as np
import datetime
import Polls
import Seats
import PollsterWeights
import RunoffElection
import PollAggregator
import ApplySwings
#import MarginalTrendAdjustments
import PreferenceCalculator

def LoadNationalSimple(year):

	path = 'data/election_data/fed_{0}/AUS.csv'.format(year)
	data = pd.read_csv(path,header=1,skiprows=0)

	seats = []

	for division_id in data['DivisionID'].unique():
		this_data = data[data['DivisionID'] == division_id]
		seat = Seats.Seat(this_data['DivisionNm'].iloc[0], this_data['StateAb'].iloc[0])
		seats.append(seat)
		results_dict = {}
		swing_dict = {}
		for i in range(0,len(this_data)):
			results_dict[this_data['PartyAb'].iloc[i]] = int(this_data['TotalVotes'].iloc[i])
			swing_dict[this_data['PartyAb'].iloc[i]] = float(this_data['Swing'].iloc[i])
		results_dict['Informal'] = results_dict.pop(np.nan)
		swing_dict['Informal'] = swing_dict.pop(np.nan)
		seat.AddResults(year, results_dict)
		seat._swings[year] = swing_dict

	return seats

# nsw_results = pd.read_csv('data/election_data/fed_2013/tpp_nsw.csv')
# nsw_results.columns = ['seat', 'alp_tpp']
# act_results = pd.read_csv('data/election_data/fed_2013/tpp_act.csv')
# act_results.columns = ['seat', 'alp_tpp']
# nt_results = pd.read_csv('data/election_data/fed_2013/tpp_nt.csv')
# nt_results.columns = ['seat', 'alp_tpp']
# sa_results = pd.read_csv('data/election_data/fed_2013/tpp_sa.csv')
# sa_results.columns = ['seat', 'alp_tpp']
# wa_results = pd.read_csv('data/election_data/fed_2013/tpp_wa.csv')
# wa_results.columns = ['seat', 'alp_tpp']
# vic_results = pd.read_csv('data/election_data/fed_2013/tpp_vic.csv')
# vic_results.columns = ['seat', 'alp_tpp']
# qld_results = pd.read_csv('data/election_data/fed_2013/tpp_qld.csv')
# qld_results.columns = ['seat', 'alp_tpp']
# tas_results = pd.read_csv('data/election_data/fed_2013/tpp_tas.csv')
# tas_results.columns = ['seat', 'alp_tpp']

# actual_results = [nsw_results, act_results, nt_results, sa_results, wa_results, vic_results, qld_results, tas_results]

# prefs = pd.read_csv('data/election_data/fed_2013/pref_ag.csv')

# basic_pref_flows = {'COA' :{'ALP': 40.00, 'IND': 60.00, 'GRN': 0},
# 					'ALP': {'COA': 40.00, 'GRN':0, 'OTH': 0, 'IND': 60.00}
# 					}

# for i in range(0,len(prefs)):
# 	basic_pref_flows[prefs['party'][i]] = {'ALP': prefs['to_alp'][i], 'COA': prefs['to_coa'][i]}


# results2010 = LoadNationalSimple(2010)
# results2013 = pd.concat(actual_results)

# poll_aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,7), 7, False, ['PUP'])
# swings = PollAggregator.GetSwings('AUS', poll_aggregate, datetime.datetime(2013,9,7), ['PUP'])

# results2010[68].AddResults(2010,Seats.join_others(Seats.join_coalition(results2010[68].results(2010))))

# # for i in range(0,len(results2010)):
# # 	if results2010[i].name in ['Fairfax', 'Indi', 'Kennedy',
# # 							   'Melbourne', 'Denison', 'Wills',
# # 							   'Batman', 'New England', 'Mallee',
# # 							   'Durack', 'O\'Connor']:
# # 		print i, results2010[i].name

# # for i in [32,60,68,95,100,118,124,128,134,139,144]
# # 	print results2010[i].name
# # 	print RunoffElection.Runoff(results2010[i].results(2010), basic_pref_flows, False, True)
# # 	print '\n'


# #results =  MarginalTrendAdjustments.LoadMarginals(2013, 'Melbourne', ['ALP', 'GRN'], True)[0].results()

# # results = results2010[50].results(2010)
# # print results2010[50].name

# # print PreferenceCalculator.ComputePreferences(results)
# # print poll_aggregate.results('ALP')

# #print MarginalTrendAdjustments.AdjustSwing(results2010[128], datetime.datetime(2013,9,7), poll_aggregate, PreferenceCalculator.ComputePreferences(results),
# #										   MarginalTrendAdjustments.LoadMarginals(2013, 'Melbourne', ['ALP', 'GRN'], True)[0],2010)

# #def Runoff(candidate_dict, pref_flows, group_others = False, print_progress = False):
# #print results
# #print RunoffElection.GetTPP(RunoffElection.Runoff(results, PreferenceCalculator.ComputePreferences(results),group_others = True, print_progress = False),True)

# count = 0
# wrong_count = 0
# errors = []
# final_composition = {}
# for seat in results2010:
# 	#if seat.state != 'TAS':

# 	if seat.name in ['Indi','Denison']:
# 		ind_leaning = 'left'
# 	elif seat.name in ['New England']:
# 		ind_leaning = 'right'
# 	else:
# 		ind_leaning = 'left'

# 	result = RunoffElection.GetTPP(RunoffElection.Runoff(ApplySwings.ApplySwings(seat, 2010, swings, PreferenceCalculator.ComputePreferences(seat.results(2010),independent_leanings = ind_leaning)), PreferenceCalculator.ComputePreferences(seat.results(2010),independent_leanings = ind_leaning)),return_parties = 'True')



# 	# if seat.state == 'QLD':
# 	# 	pass
# 	# 	#result -= 6
# 	# elif seat.state == 'VIC':
# 	# 	pass
# 	# 	#result -= 2
# 	# elif seat.state == 'NSW':
# 	# 	pass
# 	# 	#result -= 2
# 	# elif seat.state == 'SA':
# 	# 	pass
# 		#result -= 4
# 	try:
# 		actual = results2013[results2013['seat'] == seat.name]['alp_tpp'].iloc[0]
# 		difference = np.absolute(result[1]-actual)
# 		errors.append(difference)
# 		if (actual > 50.00) and (result[1] < 50.00):
# 			highlight2 = '****'
# 			wrong_count += 1
# 		elif (actual < 50.00) and (result[1] > 50.00):
# 			highlight2 = '****'
# 			wrong_count += 1
# 		else:
# 			highlight2 = ''
# 	except IndexError:
# 		pass
# 	if difference > 4:
# 		highlight = '####'
# 		count += 1
# 	else:
# 		highlight = ''
# 	print seat.name, result[0], result[1], actual, highlight, highlight2
# 	try:
# 		final_composition[result[0]]+=1
# 	except KeyError:
# 		final_composition[result[0]] = 1

# print count
# print wrong_count, '(', np.round(100*float(wrong_count)/145.00,2), '% )'
# print np.round(np.mean(errors),3)
# print final_composition

# ## Load 2010 results by seat
# ## Apply swings as computed by aggregator
# ## Apply corrections to swings
# ## Compute runoffs
# ## Compare results