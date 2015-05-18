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

'''
Because the Greens are the only third party 
included in every poll, we include an option
in the runoff simulator which groups all other 
parties into an Other grouping.
'''

basic_pref_flows = {'GRN': {'ALP': 83.03, 'LIB': 16.97},
					'OTH': {'ALP': 46.50, 'LIB': 53.50}}

import numpy as np

def Runoff(candidate_dict, pref_flows, group_others = False):

# ## possibilities this needs to guard against:
# ## LIB / LP
# ## NP instead of LIB

	try:
		del candidate_dict['Informal']
	except KeyError:
		pass

# 	if len(candidate_dict) == 3:
# 		group_others = False

# 	if group_others:

# 		if 'LIB' in candidate_dict:
# 			coa = 'LIB'
# 			if 'NP' in candidate_dict:
# 				major_parties = ['ALP', 'LIB', 'GRN', 'NP']
# 				four_corner_contest = True
# 			else:
# 				major_parties = ['ALP', 'LIB', 'GRN']
# 				four_corner_contest = False
# 		elif 'LP' in candidate_dict:
# 			coa = 'LP'
# 			if 'NP' in candidate_dict:
# 				major_parties = ['ALP', 'LP', 'GRN', 'NP']
# 				four_corner_contest = True
# 			else:
# 				major_parties = ['ALP', 'LP', 'GRN']
# 				four_corner_contest = False
# 		else:
# 			return 'Cannot find Coalition...'

# 		others = []

# 		for party in candidate_dict:
# 			if party not in major_parties:
# 				others.append(party)

# 		others_votes = 0
# 		for party in others:
# 			others_votes = others_votes + candidate_dict[party]

# 		new_dict = {'ALP':candidate_dict['ALP'], coa:candidate_dict[coa], 'GRN':candidate_dict['GRN'], 'OTH':0}

# 		if four_corner_contest:
# 			new_dict['NP'] = candidate_dict['NP']

# 		for party in others:
# 			new_dict['OTH'] = new_dict['OTH'] + candidate_dict[party]

# 		new_pref_flows = {'ALP': {                                 coa: pref_flows['ALP'][coa], 'GRN': pref_flows['ALP']['GRN']},
# 		                  coa: {'ALP': pref_flows[coa]['ALP'],                                  'GRN': pref_flows[coa]['GRN']},
# 		                  'GRN': {'ALP': pref_flows['GRN']['ALP'], coa: pref_flows['GRN'][coa],                                },
# 		                  'OTH': {}}
# 		if four_corner_contest:
# 			new_pref_flows['NP'] = {'ALP': pref_flows['NP']['ALP'], coa: pref_flows['NP'][coa], 'GRN': pref_flows['NP']['GRN']}
# 			new_pref_flows['ALP']['NP'] = pref_flows['ALP']['NP']
# 			new_pref_flows[coa]['NP'] = pref_flows[coa]['NP']
# 			new_pref_flows['GRN']['NP'] = pref_flows['GRN']['NP']

# 		for party in major_parties:
# 			others_count = 0
# 			for other_party in others:
# 				others_count = others_count + pref_flows[party][other_party]
# 			new_pref_flows[party]['OTH'] = others_count

# 		## The others groups' preference flows will be the weighted average 
# 		## of its constituent parties

# 		for party in major_parties:
# 			others_percentage = 0
# 			for other_party in others:
# 				others_percentage = others_percentage + pref_flows[other_party][party]*candidate_dict[party]
# 			new_pref_flows['OTH'][party] = others_percentage/others_votes

# 		remaining_candidates = new_dict
# 		pref_flows = new_pref_flows

	remaining_candidates = candidate_dict

	while len(remaining_candidates) > 2:

		# While there are more than two candidates remaining,
		# we take the candidate with the fewest votes and
		# eliminate them from the count, distributing their
		# votes among the remaining candidates acccording
		# to the preference flow data. 

		to_eliminate = min(remaining_candidates, key = remaining_candidates.get)
		votes = remaining_candidates[to_eliminate]
		to_dist = {}
		for key, value in pref_flows[to_eliminate].iteritems():
			if key in remaining_candidates:
				to_dist[key] = value
		count = 0
		for party in to_dist:
			count = count + to_dist[party]
		for party in to_dist:
			to_dist[party] = to_dist[party]/count
		del remaining_candidates[to_eliminate]
		for party in remaining_candidates:
			remaining_candidates[party] = int(np.round(remaining_candidates[party] + to_dist[party]*votes,0))

	return remaining_candidates