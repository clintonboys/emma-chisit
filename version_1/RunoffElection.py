'''
RunoffElection.py
-----------------

Simulates an Australian federal lower-house election 
using single transferable instant runoff voting. 

We take as input two dictionaries. The first consists of 
the raw first-preference vote numbers for each party. 
'''

sample_dict = {'ALP':10000, 'LIB':8500, 'GRN':1300, 'FF':400, 'IND':150, 'SEX':50}

'''
The second consists of a matrix of preference data, 
which can be obtained for example through historical
preference data or by polls. Note that this matrix does 
not give the complete picture of preference flows, just
the percentage of each party's first preferences which
end up being distributed to other parties. 
'''

pref_flows = {'ALP':{             'LIB': 0.20, 'GRN': 0.50, 'FF':0.15, 'IND': 0.10, 'SEX': 0.05},
			  'LIB':{'ALP': 0.10,              'GRN': 0.15, 'FF':0.60, 'IND': 0.10, 'SEX': 0.05},
			  'GRN':{'ALP': 0.85, 'LIB': 0.10,              'FF':0.02, 'IND': 0.01, 'SEX': 0.02},
			   'FF':{'ALP': 0.25, 'LIB': 0.55, 'GRN': 0.05,            'IND': 0.10, 'SEX': 0.05},
			  'IND':{'ALP': 0.40, 'LIB': 0.40, 'GRN': 0.10, 'FF':0.05,              'SEX': 0.05},
			  'SEX':{'ALP': 0.55, 'LIB': 0.05, 'GRN': 0.35, 'FF':0.01, 'IND': 0.04             }}

import numpy as np

def Runoff(candidate_dict, pref_flows, group_others = False):

	# While there are more than two candidates remaining,
	# we take the candidate with the fewest votes and
	# eliminate them from the count, distributing their
	# votes among the remaining candidates acccording
	# to the preference flow data, which is calculated using
	# ComputePreferences.py. 

	try:
		del candidate_dict['Informal']
	except KeyError:
		pass

	remaining_candidates = candidate_dict

	round_no = 0

	# print '------------------'
	# print 'Runoff Election'
	# print candidate_dict
	# print '------------------'

	while len(remaining_candidates) > 2:

		round_no = round_no + 1

		to_eliminate = min(remaining_candidates, key = remaining_candidates.get)

		is_oth = False

		if to_eliminate not in pref_flows:
			is_oth = True

#		print 'Runoff election round #' + str(round_no) + ', eliminating ' + to_eliminate
		votes = remaining_candidates[to_eliminate]
		to_dist = {}
		if is_oth:
			for key,value in pref_flows['OTH'].iteritems():
				if key in remaining_candidates:
					to_dist[key] = value
		else:
			for key, value in pref_flows[to_eliminate].iteritems():
				if key in remaining_candidates:
					to_dist[key] = value
		count = 0
		for party in to_dist:
			count = count + to_dist[party]
		for party in to_dist:
			try:
				to_dist[party] = to_dist[party]/count
			except ZeroDivisionError:

#				print remaining_candidates
				return 

				#raise Exception('Cannot compute this runoff, minor party in final two.')
#		print to_dist
		del remaining_candidates[to_eliminate]
		for party in remaining_candidates:
			if party in to_dist:
				remaining_candidates[party] = int(np.round(remaining_candidates[party] + to_dist[party]*votes,0))
			else:
				remaining_candidates[party] = int(remaining_candidates[party])

	return remaining_candidates

def GetTPP(results_dict):

	## This function computes the ALP TPP percentage given a 
	## results dictionary with two candidates.

	if len(results_dict) > 2:
		return 'Error: perform runoff election with Runoff(...) before computing TPP...'

	else:
		try:
			return np.round(100*(float(results_dict['ALP']) / (float(sum(results_dict.values())))),2)
		except KeyError:
			raise Exception('Error: ALP not in final two candidates...')