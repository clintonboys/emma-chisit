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

--------------
ApplySwings.py
--------------

Version history
---------------
1.0 	Everything is written to work in the 
		four-party model. Currently applies nationwide
		swing to each seat. 

'''

import Polls
import Seats
import RunoffElection
import pandas as pd
import numpy as np
import datetime

def ApplySwings(seat, year, swing_dict, pref_dict):

	## Applies the swings calculated in swing_dict, using preference
	## flows in pref_dict, to the seat seat in year year. For example, 
	## compute a swing from a poll aggregate and apply this to the 
	## previous election's results to obtain the implied result for 
	## this seat by the nationwide swing. 

    liberal = 0
    national = 0
    liberal_party = None
    national_party = None
    for party in ['LIB', 'LP']:
        if seat.results(year,party) > 0:
            liberal = liberal + seat.results(year,party)
            liberal_party = party

    for party in ['NAT', 'NP']:
        if seat.results(year,party) > 0:
            national = national + seat.results(year,party)
            national_party = party

    results_dict = {'COA': liberal + national}

    fourth_parties = [party for party in swing_dict if (party not in seat._results[year]) and (party not in ['OTH', 'COA'])]
    total = sum([seat._results[year][party] for party in seat._results[year]])
    swing_total = sum([swing_dict[party] for party in fourth_parties])
    for party in seat._results[year]:
    	seat._results[year][party] = (1-0.01*swing_total)*seat._results[year][party]
    for party in fourth_parties:
    	seat._results[year][party] = swing_dict[party]*0.01*total

    for party in seat._results[year]:
        if party not in [liberal_party, national_party]:
            results_dict[party] = seat.results(year,party)

    seat._results[year] = results_dict
    seat_votes = 0
    for party in seat._results[year]:
		try: 
			seat_votes = seat_votes + float(seat._results[year][party])
		except KeyError:
			pass
    for party in seat._results[year]:
		if party != 'Informal':
			try:
				seat._results[year][party] = int((1+0.01*swing_dict[party])*seat._results[year][party])
			except KeyError:
				seat._results[year][party] = int((1+0.01*swing_dict['OTH'])*seat._results[year][party])
    return seat._results[year]