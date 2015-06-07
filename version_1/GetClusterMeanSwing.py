'''
GetClusterMeanSwing.py
----------------------

Given a cluster of demographically similar seats, 
this module computes their mean swings from previous
elections. 


'''

import pandas as pd
import numpy as np
import datetime
import LoadData
import MakeSeats
import ClusterSeats
import LoadResultsByPP
import PollsterWeightings
import RunoffElection
import PollAggregator
import ComputeSeatSwings
import matplotlib.pyplot as plt
from scipy.stats import norm

def LoadSwings(year):

	path = 'data/election_data/fed_{0}/AUS.csv'.format(year)
	data = pd.read_csv(path,header=1,skiprows=0)

	seats = []

	for division_id in data['DivisionID'].unique():
		this_data = data[data['DivisionID'] == division_id]
		seat = MakeSeats.Seat(this_data['DivisionNm'].iloc[0], this_data['StateAb'].iloc[0])
		seats.append(seat)
		results_dict = {}
		swing_dict = {}
		for i in range(0,len(this_data)):
			results_dict[this_data['PartyAb'].iloc[i]] = int(this_data['TotalVotes'].iloc[i])
			swing_dict[this_data['PartyAb'].iloc[i]] = float(this_data['Swing'].iloc[i])
		results_dict['Informal'] = results_dict.pop(np.nan)
		swing_dict['Informal'] = swing_dict.pop(np.nan)
		seat.AddResults(2010, results_dict)
		seat._swings[year] = swing_dict

	return seats

def GetMeanSwings(year):

	path = 'data/election_data/fed_{0}/AUS.csv'.format(year)
	data = pd.read_csv(path,header=1,skiprows=0)

	swing_dict = {}

	for i in range(0,len(data)):
		try:
			swing_dict[data['PartyAb'][i]].append(data['Swing'][i])
		except KeyError:
			swing_dict[data['PartyAb'][i]] = [data['Swing'][i]]

	av_dict = {}
	for party in swing_dict:
		av_dict[party] = np.round(np.mean(swing_dict[party]),3)
	return av_dict

def GetClusterSwings(cluster, year):

	seats = LoadSwings(year)
	n = len(cluster)
	total_dict = {}
	for seat in cluster:
		for party in seat.swing(year):
			try:
				total_dict[party] = total_dict[party] + seat.swing(year)[party]
			except KeyError:
				total_dict[party] = seat.swing(year)[party]

	for party in total_dict:
		total_dict[party] = np.round(float(total_dict[party])/float(n),3)


	return total_dict

def LoadClusterSeats(cluster, year):

	n = len(cluster)
	seat_list = []

	seats_proper = LoadResultsByPP.LoadNationalSimple(year)

	for seat in seats_proper:
		if seat.name in cluster:
			seat_list.append(seat)

	q = len(seat_list)

	# if n != q:
	# 	print str(np.absolute(n-q)) + ' seats from census data do not match electorate list in ' + str(year) + '...'

	return seat_list





# path = 'data/election_data/fed_{0}/AUS.csv'.format(2010)
# data = pd.read_csv(path,header=1,skiprows=0)
# swings = []
# for i in range(0,len(data)):
# 	if data['PartyAb'][i] == 'ALP':
# 		swings.append(data['Swing'][i])



# mu,std = norm.fit(swings)
# #print mu, std

# seats = LoadSwings(2010)
# cluster = [seats[0], seats[1], seats[5]]
# #print GetClusterSwings(cluster, 2010)

# meanswings = GetMeanSwings(2010)
# clusters = ClusterSeats.ClusterSeats(2006,6)
# # for cluster in clusters:
# # 	proper_cluster = LoadClusterSeats(cluster,2010)
# # 	print GetClusterSwings(proper_cluster, 2010)['ALP']-mu
# cluster_nos = {}
# for i in range(0,len(clusters)):
# 	for j in range(0,len(clusters[i])):
# 		cluster_nos[clusters[i][j]] = i

# print cluster_nos


