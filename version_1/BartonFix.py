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
import ClusterSeats
import GetClusterMeanSwing
from scipy.stats import norm

prefs = pd.read_csv('data/election_data/fed_2013/pref_ag.csv')

basic_pref_flows = {'COA' :{'ALP': 9.21, 'COA': 90.79, 'GRN': 0},
					'ALP': {'COA': 0, 'GRN':0, 'OTH': 0}}

for i in range(0,len(prefs)):
	basic_pref_flows[prefs['party'][i]] = {'ALP': prefs['to_alp'][i], 'COA': prefs['to_coa'][i]}

aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,7),15)
swing_dict = PollAggregator.GetSwings('AUS', aggregate, datetime.datetime(2013,9,7))

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

results2013 = pd.concat(actual_results)
seats = LoadResultsByPP.LoadNationalSimple(2010)

barton = seats[3]

#print barton._results[2010]
#print RunoffElection.GetTPP(RunoffElection.Runoff(barton._results[2010], basic_pref_flows))
print ComputeSeatSwings.ApplySwings(barton, 2010, swing_dict, basic_pref_flows)
#print RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(barton, 2010, swing_dict, basic_pref_flows), basic_pref_flows))

def ToPercent(results_dict):
	count = 0
	for party in results_dict:
		count = count + results_dict[party]
	final_dict = {}
	for party in results_dict:
		final_dict[party] = 100*float(results_dict[party])/float(count)
	return final_dict

print ToPercent(barton._results[2010])


#print actual_results['alp_tpp'][actual_results['seat']=='Barton']

# path = 'data/election_data/fed_{0}/AUS.csv'.format(2010)
# data = pd.read_csv(path,header=1,skiprows=0)
# swings = []
# for i in range(0,len(data)):
# 	if data['PartyAb'][i] == 'ALP':
# 		swings.append(data['Swing'][i])

# meanswings = GetClusterMeanSwing.GetMeanSwings(2010)

# clusters = ClusterSeats.ClusterSeats(2006,6)

# cluster_nos = {}
# for i in range(0,len(clusters)):
# 	for j in range(0,len(clusters[i])):
# 		cluster_nos[clusters[i][j]] = i

#mu,std = norm.fit(swings)

# for i in range(0,len(clusters)):
# 	proper_cluster = LoadClusterSeats(cluster,2010)
# 	for seat in proper_cluster:
# 		seat._cluster_no = i
# 	print GetClusterSwings(proper_cluster, 2010)['ALP']-mu

# count = 0
# error_dict = []
# wrong_count = 0
# margin_count = 0

# for seat in seats:
# 	try:
# 		actual = results2013[results2013['seat'] == seat.name]['alp_tpp'].iloc[0]
# 		count = count +1
# 	except IndexError:
# #		print "No name for ", seat.name
# 		actual = 0

# 	# try:
# 	# 	cluster_fix = cluster_nos[seat.name]
# 	# 	fix = GetClusterMeanSwing.GetClusterSwings(GetClusterMeanSwing.LoadClusterSeats(clusters[cluster_fix],2010),2010)['ALP'] #- mu
# 	# except KeyError:
# 	# 	fix = 0
# 	try:
# 		estimated = RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(seat, 2010, swing_dict, basic_pref_flows), basic_pref_flows)) #+ fix
# 	except Exception:
# 		estimated = 0
# 	# if seat.state() == 'QLD':
# 	#  	estimated -= 6
# #	print actual, type(actual)
# #	print estimated, type(estimated)

# 	if np.absolute(float(actual) - float(estimated)) > 4.00:
# 		highlight1 = '#######'
# 		margin_count +=1
# 	else:
# 		highlight1 = '       '
# 	if (actual > 50.00) and (estimated < 50.00):
# 		highlight = '*******' 
# 		wrong_count += 1
# 	elif (actual < 50.00) and (estimated > 50.00):
# 		highlight = '*******'
# 		wrong_count +=1 
# 	else:
# 		highlight = ''
# 	len1 = len(seat.name) + len(seat.state()) + 4
# 	pad1 = ' '*(23-len1)
# 	if len(str(actual)) <5 :
# 		pad2 = ' '*(5-len(str(actual)))
# 	else:
# 		pad2 = ''
# 	if len(str(estimated)) < 5:
# 		pad3 = ' '*(5-len(str(estimated)))
# 	else:
# 		pad3 = ''
# 	try:
# 		error_dict.append(np.absolute(float(actual)-float(estimated)))
# 	except TypeError:
# 		pass

# 	print seat.name, '(' , seat.state(), ')', pad1,' | Actual 2013 TPP: ', pad2, actual, ' | Estimated TPP: ', estimated, pad3, highlight1, highlight
# print '-'*80
# print 'Average error: ', str(np.round(np.mean(error_dict),3))
# print 'Incorrect predictions: ', str(wrong_count), '(', str(np.round(100*float(wrong_count)/150.00,3)), '%)'
# print 'Large error margins: ', str(margin_count), '(', str(np.round(100*float(margin_count)/150.00,3)), '%)'
# print '-'*80




# print seats[32].name
# print seats[32]._results[2010]
# print swing_dict
# print ComputeSeatSwings.ApplySwings(seats[32], 2010, swing_dict, basic_pref_flows)

# seat_votes = 0

# for party in seats[32]._results[2010]:
# 	try: 
# 		seat_votes = seat_votes + float(seats[32]._results[2010][party])
# 	except KeyError:
# 		pass

# print seat_votes

# for party in seats[32]._results[2010]:
# 	if party != 'Informal':
# 		try:
# 			seats[32]._results[2010][party] = int(seats[32]._results[2010][party] + 0.01*swing_dict[party]*seat_votes)
# 		except KeyError:
# 			seats[32]._results[2010][party] = int(seats[32]._results[2010][party] + 0.01*swing_dict['OTH']*seat_votes)

# print seats[32]._results[2010]



# print RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(seats[32], 2010, swing_dict, basic_pref_flows), basic_pref_flows)
# estimated = RunoffElection.GetTPP(RunoffElection.Runoff(ComputeSeatSwings.ApplySwings(seats[32], 2010, swing_dict, basic_pref_flows), basic_pref_flows))
# actual = results2013[results2013['seat'] == seats[32].name]['alp_tpp'].iloc[0]
# print estimated
# print actual