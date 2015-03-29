import pandas as pd
import numpy as np
import math
import LoadData
from operator import attrgetter

parties = ['ALP', 'LIB', 'NAT', 'COA', 'DEM', 'GRN', 'ONP', 'PUP', 'KAP', 'FF', 'CD', 'OTH']
states = ['NSW', 'VIC', 'SA', 'WA', 'QLD', 'TAS']
pollsters = ['Morgan', 'Newspoll', 'Galaxy', 'Essential', 'ReachTEL']
others = ['DEM', 'ONP', 'PUP', 'KAP', 'FF', 'CD', 'OTH']

VIC_polls = LoadData.LoadPolls('VIC')
NSW_polls = LoadData.LoadPolls('NSW')
SA_polls = LoadData.LoadPolls('SA')
WA_polls = LoadData.LoadPolls('WA')
QLD_polls = LoadData.LoadPolls('QLD')
TAS_polls = LoadData.LoadPolls('TAS')

state_polls = [NSW_polls, VIC_polls, SA_polls, WA_polls, QLD_polls, TAS_polls]

elections_from_2000 = LoadData.LoadElections()

error_dict = {}

for pollster in pollsters:
	error_dict[pollster] = []
	for election in elections_from_2000:
		potential_list = []
		for state in state_polls:
			for poll in state:
				if poll.pollster == pollster:
					if 0 < -(poll.median_date() - election.election_date()).days < 15:
						potential_list.append(poll)
						poll.distance = -(poll.median_date() - election.election_date()).days
		try:
			min_dist = min(potential_list, key=attrgetter('distance'))
			error_dict[pollster].append([min_dist,election])
		except ValueError:
			pass
		
def CoalitionConsistency(poll1,poll2):

	## checks if two polls have the same lib/nat/coalition 
	## data and if not, combines them in the best possible way

def OthersConsistency(poll1,poll2):

	## checks if two polls have the same others
	## configuration and if not, combines them in the 
	## best possible way

def ComputeRMSQ(poll, election):

	## This function computes the RMSQ error
	## of a poll from the actual election outcome

	poll, election = CoalitionConsistency(poll,election)
	poll, election = OthersConsistency(poll,election)

	to_sum = []
	for party in parties:
		count = 0
		if not np.isnan(poll.results(party)):
			if not np.isnan(election.results(party)):
				try:
					resid = poll.results(party) - election.results(party)
					count = count + 1
				except TypeError:
					pass
				try:
					to_sum.append(math.pow(resid,2))
					count = count + 4
				except TypeError:
					pass
		tppresid = poll.tpp() - election.tpp()
		to_sum.append(4*(math.pow(tppresid,2)))

	return sum(to_sum)/count

for party in parties:
	print party, error_dict['Morgan'][0][0].results(party), error_dict['Morgan'][0][1].results(party)
	print np.isnan(error_dict['Morgan'][0][0].results(party))

print error_dict['Morgan'][0][1].election_date()

#print ComputeRMSQ(error_dict['Morgan'][0][0], error_dict['Morgan'][0][1])



