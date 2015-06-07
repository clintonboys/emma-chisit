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

------------------
PollsterWeights.py
------------------

v1.0 Computes weightings for all pollsters in the database 
	 of polling data to use in the model, based on historical
	 reliability. 

v2.0 Now works with improved poll classes. Will not need to be 
	 computed every time. 

'''

import pandas as pd
import numpy as np
import math
import Polls
from operator import attrgetter

pollsters = ['Morgan', 'Newspoll', 'Galaxy', 'Essential', 'ReachTEL', 'Nielsen', 'Ipsos']

def GetRelevantPolls(n = 14):

	## For each election, find the closest poll for each pollster
	## which was conduction within n days before the election (this 
	## value defaults to two weeks), and add them all to a
	## dictionary of pollsters and polls. 

	election_data = Polls.LoadElections()

	states = ['NSW', 'VIC', 'SA', 'WA', 'QLD', 'TAS', 'AUS']

	state_polls = []
	for state in states:
		state_polls.append(Polls.LoadPolls(state))

	error_dict = {}

	for pollster in pollsters:
		error_dict[pollster] = []
		for election in election_data:
			potential_list = []
			for state in state_polls:
				for poll in state:
					if poll.state() == election.state():
						if poll.pollster == pollster:
							if 0 < -(poll.median_date() - election.election_date()).days < n:
								potential_list.append(poll)
								poll.distance = -(poll.median_date() - election.election_date()).days
			try:
				min_dist = min(potential_list, key=attrgetter('distance'))
				error_dict[pollster].append([min_dist,election])
			except ValueError:
				pass

	return error_dict
			
			
def ComputeRMSQ(poll, election, weight_TPP = False, TPP_weight = 4):

	## This function computes the RMSQ error
	## of a poll from the actual election outcome. 
	## It will only work if the poll and election
	## have been adjusted to have the same parties. 
	## We also allow to include the predicted TPP in the 
	## calculation with a specified weight. 

	if set(list(poll._results.keys())) == set(list(election._results.keys())):

		to_sum = []
		count = 0
		for party in list(poll._results.keys()):
			resid = poll.results(party) - election.results(party)
			try:
				to_sum.append(math.pow(resid,2))
			except TypeError:
				pass
			count = count + 1

		if weight_TPP:

			tppresid = poll.tpp() - election.tpp()
			if not np.isnan(tppresid):
				try:
					to_sum.append(TPP_weight*(math.pow(tppresid,2)))
				except TypeError:
					pass
			count = count + TPP_weight

		return np.round(math.sqrt(sum(to_sum)/count),3)

	else:
		print 'Pollster Weight Error: Can only compute RMSQ error when parties match in poll and election...'
		return 0.00


def ComputeError(pollster, n = 14):

	## Computes the average RMSQ error of a pollster, 
	## first converting polls and elections into a 
	## compatible form. 

	error_dict = GetRelevantPolls(n)[pollster]

	av_error = []

	errors = []

	for i in range(0,len(error_dict)):

		poll = error_dict[i][0]
		election = error_dict[i][1]
		poll.join_coalition()
		poll.join_others()
		election.join_coalition()
		election.join_others()

		print election._results
		print poll._results

		errors.append(np.round(ComputeRMSQ(poll, election),3))

	av_error.append(np.mean(errors))
	return np.round(np.mean(errors), 3)

def ComputePollsterWeights(n = 14):

	errors = {}
	for pollster in pollsters:
		errors[pollster] = ComputeError(pollster, n)

	av_error = np.round(np.mean(errors.values()),3)

	weight_dict = {}

	for pollster in pollsters:
		weight_dict[pollster] = np.round(1/(errors[pollster] / av_error),3)

	return weight_dict

Weights = {'Newspoll': 0.60599999999999998, 'Nielsen': 1.4550000000000001, 'Ipsos': 1.0720000000000001, 'Morgan': 1.0149999999999999, 'ReachTEL': 1.169, 'Essential': 1.1599999999999999, 'Galaxy': 0.97299999999999998}