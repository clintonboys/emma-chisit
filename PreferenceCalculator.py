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

-----------------------
PreferenceCalculator.py
-----------------------

v1.0 Takes the primary results for an election and outputs
	 the relevant preference dictionary.

'''

import pandas as pd
import numpy as np
import datetime
import Polls
import Seats
import PollsterWeights
import RunoffElection
import PollAggregator
import ApplySwings
import MarginalTrendAdjustments


def NormaliseDict(d, target=1.0):
	raw = sum(d.values())
	factor = target/raw
	return {key:np.round(value*factor,3) for key,value in d.iteritems()}


def ComputePreferences(primary_results, independent_leanings = 'right', other_leanings = 'right'):

	## Takes as input a dictionary of primary results, together 
	## with a political leaning of the independent candidate(s). 
	## Outputs a normalised preference dictionary. 

	master_preferences = pd.read_csv('AntonyGreenPreferences.csv')

	new_leanings = master_preferences.leaning.tolist()
	new_leanings[3] = independent_leanings
	new_leanings[-1] = other_leanings
	master_preferences['leaning'] = new_leanings

	print master_preferences

	print primary_results.keys()

	pref_dict = {}

	AG_map = {}

	for key in primary_results.keys():
		if key in ['ALP','COA']:
			AG_map[key] = key
		elif key in master_preferences.party.tolist():
			AG_map[key] = key
		else:
			AG_map[key] = 'OTH'
	print AG_map

	for party in primary_results.keys():

		if party in ['ALP','COA']:
			pref_dict[party] = {}
			for second_party in primary_results.keys():
				if party == second_party:
					pref_dict[party][second_party] = 80
				elif second_party in ['ALP','COA']:
					pref_dict[party][second_party] = 20
				elif master_preferences[master_preferences.party == AG_map[second_party]].leaning.iloc[0] == 'left':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == 'GRN'].to_alp.iloc[0]
				elif master_preferences[master_preferences.party == AG_map[second_party]].leaning.iloc[0] == 'right':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == 'SAL'].to_coa.iloc[0]

		else:
			pref_dict[party] = {}
			for second_party in primary_results.keys():
				if second_party == 'ALP':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == AG_map[party]].to_alp.iloc[0]
				elif second_party == 'COA':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == AG_map[party]].to_coa.iloc[0]
				elif master_preferences[master_preferences.party == AG_map[second_party]].leaning.iloc[0] == 'left':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == AG_map[party]].to_alp.iloc[0]
				elif master_preferences[master_preferences.party == AG_map[second_party]].leaning.iloc[0] == 'right':
					pref_dict[party][second_party] = master_preferences[master_preferences.party == AG_map[party]].to_coa.iloc[0]

	new_dict = {}
	for key in pref_dict.keys():
		new_dict[key] = NormaliseDict(pref_dict[key])
	return new_dict

