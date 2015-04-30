import pandas as pd
import numpy as np
import LoadData
import MakeSeats

path = 'data/election_data/fed_2013/HouseStateFirstPrefsByPollingPlaceDownload-17496-ACT.csv'
state = 'ACT'

data = pd.read_csv(path,header=0,skiprows=1)

seats = []
polling_places = []

for division_id in data['DivisionID'].unique():
	seat = MakeSeats.Seat(data[data['DivisionID'] == division_id]['DivisionNm'][:1], state)
	seats.append(seat)
	for polling_place_id in data['PollingPlaceID'][data['DivisionID'] == division_id].unique():
		pp_frame = data[(data['DivisionID'] == division_id) & (data['PollingPlaceID'] == polling_place_id)]
		polling_place = MakeSeats.PollingPlace(pp_frame['PollingPlace'][:1], seat.name)
		polling_places.append(polling_place)

print seats[0]
