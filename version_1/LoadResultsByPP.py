'''
LoadResultsByPP.py
------------------

Loads into memory the primary vote results for all 
polling places in a given state in a given year's
election.

'''


import pandas as pd
import numpy as np
import LoadData
import MakeSeats
import PollsterWeightings
import RunoffElection

def ReadPPResults(path,state_name,year):

	## Given a filename pointing to a .csv file of primary
	## vote data by polling place in the format provided by 
	## the AEC, this function returns a list of all seats in the file,
	## and a list of all polling places in the file with primary
	## results added. 

	data = pd.read_csv(path,header=1,skiprows=0)

	seats = []
	polling_places = []

	for division_id in data['DivisionID'].unique():
		seat_name = data[data['DivisionID'] == division_id]['DivisionNm'][:1].iloc[0]
		seat = MakeSeats.Seat(seat_name, state_name)
		seats.append(seat)
		for polling_place_id in data['PollingPlaceID'][data['DivisionID'] == division_id].unique():
			pp_frame = data[(data['DivisionID'] == division_id) & (data['PollingPlaceID'] == polling_place_id)]
			pp_name = pp_frame['PollingPlace'][:1].iloc[0]
			polling_place = MakeSeats.PollingPlace(pp_name, seat)
			results_dict = {}
			for i in range(0,len(pp_frame)):
				results_dict[pp_frame['PartyAb'].iloc[i]] = int(pp_frame['OrdinaryVotes'].iloc[i])
				polling_place.AddResults(year,results_dict)
			polling_places.append(polling_place)

	return seats, polling_places


def LoadPPResults(year, state_name, fed=False):

	## For a given state (or federally, in which case the function
    ## loads results for all states in the given year) this function
	## loads into memory the seats and polling places loaded with 
	## primary results. s

	if fed:
		
		composite_states = ['NSW', 'ACT', 'NT', 'SA', 'WA', 'VIC', 'QLD', 'TAS']
		full_results = []
		for state in composite_states:
			path = 'data/election_data/fed_{0}/{1}.csv'.format(year,state)
			full_results.append(ReadPPResults(path,state_name,year))

		return full_results
	
	else:

		path = 'data/election_data/{0}_{1}/{2}.csv'.format(state_name.lower(),year,year)

		return ReadPPResults(path,state_name,year)

def GetSeatResults(seat,year):

	## Having loaded all the polling place data into memory,
	## this function accumulates it all into a results
	## dictionary for the full seat in the given year. 

	results_dict = {}
	for polling_place in seat.pollingplaces():
		for party in polling_place._results[year]:
			try:
				results_dict[party] += polling_place.GetResults(year,party)
			except KeyError:
				results_dict[party] = polling_place.GetResults(year,party)
	try:
		results_dict['Informal'] = results_dict.pop(np.nan)
	except KeyError:
		pass
	return results_dict

def GetSingleSeat(seat, year):

	state = seat.state()
	path = 'data/election_data/fed_{0}/{1}.csv'.format(year,state)
	data = pd.read_csv(path,header=1,skiprows=0)

	seat_name = seat.name

	new_data = data[(data['DivisionNm'] == seat_name)]

	polling_places = []

	for division_id in new_data['DivisionID'].unique():
		for polling_place_id in new_data['PollingPlaceID'][new_data['DivisionID'] == division_id].unique():
			pp_frame = new_data[(new_data['DivisionID'] == division_id) & (new_data['PollingPlaceID'] == polling_place_id)]
			pp_name = pp_frame['PollingPlace'][:1].iloc[0]
			polling_place = MakeSeats.PollingPlace(pp_name, seat)
			results_dict = {}
			for i in range(0,len(pp_frame)):
				results_dict[pp_frame['PartyAb'].iloc[i]] = int(pp_frame['OrdinaryVotes'].iloc[i])
				polling_place.AddResults(year,results_dict)
			polling_places.append(polling_place)

	results_dict = {}
	for polling_place in polling_places:
		for party in polling_place._results[year]:
			try:
				results_dict[party] += polling_place.GetResults(year,party)
			except KeyError:
				results_dict[party] = polling_place.GetResults(year,party)
	try:
		results_dict['Informal'] = results_dict.pop(np.nan)
	except KeyError:
		pass
	return results_dict

def LoadNationalSimple(year):

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