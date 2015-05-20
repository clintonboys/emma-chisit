'''
PollsterWeightings.py
---------------------

Computes weightings for all pollsters in the database 
of polling data to use in the model, based on historical
reliability. 

'''

import pandas as pd
import numpy as np
import math
import LoadData
from operator import attrgetter

states = ['NSW', 'VIC', 'SA', 'WA', 'QLD', 'TAS', 'AUS']
pollsters = ['Morgan', 'Newspoll', 'Galaxy', 'Essential', 'ReachTEL', 'Nielsen', 'Ipsos']

def GetRelevantPolls(n = 14):

	## For each election, find the closest poll for each pollster
	## which was conduction within n days before the election (this 
	## value defaults to two weeks), and add them all to a
	## dictionary of pollsters and polls. 

	elections_from_2000 = LoadData.LoadElections()
	state_polls = []
	for state in states:
		state_polls.append(LoadData.LoadPolls(state))

	error_dict = {}

	for pollster in pollsters:
		error_dict[pollster] = []
		for election in elections_from_2000:
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
		return 'Can only compute RMSQ error when parties match in poll and election...'

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
		poll._results = LoadData.JoinCoalition(poll)
		poll._results = LoadData.JoinOthers(poll)
		election._results = LoadData.JoinCoalition(election)
		election._results = LoadData.JoinOthers(election)

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