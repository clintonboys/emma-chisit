'''
ComputePreferences.py
---------------------

This file produces preference flow dictionaries
for use in simulating runoff elections. 
'''

def ComputePreferenceFlows(party, parties):

	## For a given party, and a list of other parties
	## contesting the seat with them, this function 
	## uses historical data to estimate the flow of preferences
	## from the given party to all the others. 

	## v1.0: Using a very very simple guess as to 
	## preferences, where the Greens give 83%
	## of their preferences to the labor party, and all other
	## parties give 54% to the liberal party. Will work to 
	## compute preferences when the top party is LP, NAT or ALP. 

	right_majors = ['LIB', 'LP', 'NP', 'NAT', 'LNP', 'COA']
	left_majors = ['ALP']

	if len([x for x in parties if x in right_majors]) > 1:
		three_corner_contest = True

	preferences = {}	

	if party == 'GRN':
		total = 0
		for other_party in parties:
			if party == 'ALP':
				preferences[party] == 83.00
			elif 
				total = total + 1

# basic_pref_flows = {'GRN': {'ALP': 83.03, 'LIB': 16.97},
# 					'OTH': {'ALP': 46.50, 'LIB': 53.50}}


def ComputePreferenceFlowDictionary(results_dict):

	## This function takes as input a dictionary of
	## primary results and outputs a dictionary of
	## preference flow percentages. 