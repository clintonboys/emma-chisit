import pandas as pd
import numpy as np
import math
import LoadData
from operator import attrgetter

parties = ['ALP', 'LIB', 'NAT', 'COA', 'DEM', 'GRN', 'ONP', 'PUP', 'KAP', 'FF', 'CD', 'OTH']
others = ['DEM', 'ONP', 'PUP', 'KAP', 'FF', 'CD', 'OTH', 'SPA']
joined_parties = ['ALP', 'COA', 'GRN', 'OTH']

states = ['NSW', 'VIC', 'SA', 'WA', 'QLD', 'TAS', 'AUS']
pollsters = ['Morgan', 'Newspoll', 'Galaxy', 'Essential', 'ReachTEL', 'Nielsen', 'Ipsos']

VIC_polls = LoadData.LoadPolls('VIC')
NSW_polls = LoadData.LoadPolls('NSW')
SA_polls = LoadData.LoadPolls('SA')
WA_polls = LoadData.LoadPolls('WA')
QLD_polls = LoadData.LoadPolls('QLD')
TAS_polls = LoadData.LoadPolls('TAS')
FED_polls = LoadData.LoadPolls('AUS')

state_polls = [NSW_polls, VIC_polls, SA_polls, WA_polls, QLD_polls, TAS_polls, FED_polls]

elections_from_2000 = LoadData.LoadElections()

error_dict = {}

for pollster in pollsters:
	error_dict[pollster] = []
	for election in elections_from_2000:
		potential_list = []
		for state in state_polls:
			for poll in state:
				if poll.state() == election.state():
					if poll.pollster == pollster:
						if 0 < -(poll.median_date() - election.election_date()).days < 15:
							potential_list.append(poll)
							poll.distance = -(poll.median_date() - election.election_date()).days
		try:
			min_dist = min(potential_list, key=attrgetter('distance'))
			error_dict[pollster].append([min_dist,election])
		except ValueError:
			pass
		
def JoinCoalition(poll):

	if np.isnan(poll.results('NAT')):
		poll.change_result('NAT', 0)

	if np.isnan(poll.results('COA')):
		poll.change_result('COA', poll.results('LIB') + poll.results('NAT'))

## Because different pollsters poll different "Other" parties, it's 
## only fair to combine all the other parties into a single group
## for the purposes of computing accuracies. 

def JoinOthers(poll):

	others_vote = 0
	for party in others:
		try:
			if not np.isnan(poll.results(party)) and poll.results(party) != 0:
				others_vote = others_vote + poll.results(party)
		except KeyError:
			pass
	try:

		del poll._results['Informal']
	except KeyError:
		pass

	poll.change_result('OTH', others_vote)

def JoinOthersResults(results):

	del results['Informal']

	if len(results) == 3:
		return results

	others_vote = 0
	for party in others:
		try:
			if not np.isnan(results[party]) and results[party] != 0:
				others_vote += results[party]
				del results[party]
		except KeyError:
			pass
	try:
		del results['Informal']
	except KeyError:
		pass
	results['OTH'] = others_vote

def ComputeRMSQ(poll, election):

	## This function computes the RMSQ error
	## of a poll from the actual election outcome

	to_sum = []
	count = 0
	for party in joined_parties:
		resid = poll.results(party) - election.results(party)
		try:
			to_sum.append(math.pow(resid,2))
		except TypeError:
			pass
		count = count + 1
	tppresid = poll.tpp() - election.tpp()
	if not np.isnan(tppresid):
		try:
			to_sum.append(4*(math.pow(tppresid,2)))
		except TypeError:
			pass
	count = count + 4

	return np.round(math.sqrt(sum(to_sum)/count),4)

def ComputePollsterError():
	av_error = []
	final_error_dict = {}

	for pollster in pollsters:

		errors = []

		for i in range(0,len(error_dict[pollster])):

			JoinCoalition(error_dict[pollster][i][0])
			JoinCoalition(error_dict[pollster][i][1])
			JoinOthers(error_dict[pollster][i][0])
			JoinOthers(error_dict[pollster][i][1])

			errors.append(np.round(ComputeRMSQ(error_dict[pollster][i][0], error_dict[pollster][i][1]),3))

		av_error.append(np.mean(errors))
		final_error_dict[pollster] = np.round(np.mean(errors), 3)
	return final_error_dict

def ComputePollsterWeights():

	errors = ComputePollsterError()

	mean_error_dict = []

	for pollster in errors:
		mean_error_dict.append(errors[pollster])

	av_error = np.round(np.mean(mean_error_dict),3)

	weight_dict = {}

	for pollster in pollsters:
		weight_dict[pollster] = np.round(1/(errors[pollster] / av_error),3)

	return weight_dict