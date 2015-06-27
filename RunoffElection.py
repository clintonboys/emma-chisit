'''
 _______  _______  _______  _______ 
(  ____ \(       )(       )(  ___  )
| (    \/| () () || () () || (   ) |
| (__    | || || || || || || (___) |
|  __)   | |(_)| || |(_)| ||  ___  |
| (      | |   | || |   | || (   ) |
| (____/\| )   ( || )   ( || )   ( |
(_______/|/     \||/     \||/     \|
                                    
 _______          _________ _______ __________________
(  ____ \|\     /|\__   __/(  ____ \|__   __/\__   __/
| (    \/| )   ( |   ) (   | (    \/   ) (      ) (   
| |      | (___) |   | |   | (_____    | |      | |   
| |      |  ___  |   | |   (_____  )   | |      | |   
| |      | (   ) |   | |         ) |   | |      | |   
| (____/\| )   ( |___) (___/\____) |___) (___   | |   
(_______/|/     \|\_______/\_______)\_______/   )_( 

(c) Clinton Boys 2015

-----------------
RunoffElection.py
-----------------

v1.0 Simulates an Australian federal lower-house election 
	 using single transferable instant runoff voting, taking
	 as input a dictionary of raw primary vote data, and a 
	 matrix of preference flow data.  

v2.0 Improved to work with percentage data, as well as non-
	 traditional candidate combinations and inclusions of fourth
	 parties in the model.

'''

import numpy as np

def Runoff(candidate_dict, pref_flows, group_others = False, print_progress = False):

	#
	# While there are more than two candidates remaining,
	# we take the candidate with the fewest votes and
	# eliminate them from the count, distributing their
	# votes among the remaining candidates acccording
	# to the preference flow data.
	#

	total = np.sum([candidate_dict[key] for key in candidate_dict])

	try:
		del candidate_dict['Informal']
	except KeyError:
		pass

	remaining_candidates = candidate_dict
	round_no = 0

	if print_progress:
		print '---------------'
		print 'Runoff Election'
		print '---------------'
		print 'Initial primary results:'
		print candidate_dict
		print '---------------'

	while len(remaining_candidates) > 2:

		round_no = round_no + 1

		to_eliminate = min(remaining_candidates, key = remaining_candidates.get)

		if print_progress:
			print 'Runoff Election. Round #' + str(round_no) + ': eliminating ' + to_eliminate

		votes = remaining_candidates[to_eliminate]
		to_dist = {}

		del remaining_candidates[to_eliminate]
		try:
			to_dist = pref_flows[to_eliminate]
		except KeyError:
			to_dist = {}
			for party in remaining_candidates:
				if party in ['LP', 'COA', 'LIB' 'LNP', 'NAT', 'NP', 'LNQ']:
					to_dist[party] = 45.95
				elif party == 'ALP':
					to_dist[party] = 54.05
				else:
					to_dist[party] = 0


		## Rescale the preference matrix to compensate for 
		## the missing columns. 

		fixed_prefs = {}
		for party in remaining_candidates:
			if party in to_dist:
				fixed_prefs[party] = to_dist[party]
		preference_sum = np.sum([fixed_prefs[key] for key in fixed_prefs])
		for party in fixed_prefs:
			fixed_prefs[party] = fixed_prefs[party]/preference_sum

		for party in remaining_candidates:
			if party in to_dist:
				remaining_candidates[party] = int(np.round(remaining_candidates[party] + to_dist[party]*0.01*votes))
			else:
				if float(remaining_candidates[party])/float(total) > 0.1:
					if print_progress:
						print 'Runoff Error: Missing preference data for important contest.'

		if print_progress:
			if len(remaining_candidates) > 2:
				print remaining_candidates

	return remaining_candidates

def GetTPP(results_dict, return_parties = False):

	## This function computes the two candidate preferred percentage 
	## given a results dictionary with two candidates.

	if len(results_dict) > 2:
		print 'Runoff Error: Cannot compute TCP with more than two candidates.'
		print '              First perform runoff election with RunoffElection.Runoff().'
		return 0.00

	else:
		winner = max(results_dict, key = results_dict.get)
		loser = min(results_dict, key = results_dict.get)
		result = np.round(100*(float(results_dict[winner]) / (float(sum(results_dict.values())))),2)
		if return_parties:
			if winner not in ['ALP', 'COA']:
				print str(winner) + ' wins with '
				return result
			else:
				if winner == 'ALP':
					return result
				else:
					return 100 - result
		else:
			if winner == 'ALP':
				return result
			else:
				return 100 - result
 