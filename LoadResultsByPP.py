import pandas as pd
import numpy as np
import LoadData
import MakeSeats
import PollsterWeightings
import RunoffElection

path = 'data/election_data/fed_2010/HouseStateFirstPrefsByPollingPlaceDownload-15508-ACT.csv'
state_name = 'ACT'
year = 2010

data = pd.read_csv(path,header=0,skiprows=1)

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

def GetSeatResults(seat):
	results_dict = {}
	for polling_place in polling_places:
		if MakeSeats.PPinSeat(polling_place, seat):
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

for seat in seats:
	seat.AddResults(year,GetSeatResults(seat))

for seat in seats:
	PollsterWeightings.JoinOthersResults(seat._results[year])
	print seat._results

basic_pref_flows = {'GRN': {'ALP': 83.03, 'LP': 16.97},
					'OTH': {'ALP': 46.50, 'LP': 53.50}}

for seat in seats:
	print RunoffElection.Runoff(seat._results[year], basic_pref_flows, True)