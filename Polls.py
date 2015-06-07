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

-----------
Polls.py
-----------

v1.0 Contains the classes for polls and elections
     used by the model, together with the functions
     to load poll data and election data from the 
     database into memory, and some helper functions
     for dealing with poll objects. 

v2.0 Polls are now all based on percentages. The 
	 functionality for years and times is improved. 
	 Defensive coding for errors. Grouping of minor 
	 parties improved. 

'''

import pandas as pd
import numpy as np
from collections import OrderedDict

major_parties = ['ALP', 'COA', 'LP', 'NAT', 'LNP', 'GRN']

class Poll(object):

    ##
    ## Poll objects should be initialised with
    ## a pollster, state, median date, sample size
    ## and (primary) results dict in percentages
    ##
    ## e.g. dummy_poll = Poll('Morgan', 'NSW', '27/1/15', 500, 
    ##                        {'ALP': 50.00, 'COA': 30.00, 'GRN': 10.00, 'FF': 10.00})
    ## 
    ## Then obtain information by calling, e.g.
    ## dummy_poll.sample_size()
    ## dummy_poll.results('ALP')
    ##
    ## The others grouping functionality specifies which
    ## parties, other than the Greens, not to group together
    ## in a single others category. 
    ##

    def __init__(self, pollster, state, mediandate, samplesize, results, TPP = None, others = []):
        self._pollster = pollster
        self._state = state
        self._mediandate = mediandate
        self._samplesize = samplesize
        self._results = results
        self._TPP = TPP
        self._others = others
        self.distance = 42090  # This variable will be used to find closest 
                               # polls to elections and so is set arbitrarily
                               # high. 
        
    @property
    def pollster(self):
        return self._pollster

    def state(self):
        return self._state

    def median_date(self):
        return self._mediandate

    def sample_size(self):
        return self._samplesize

    def results(self,party = None):
    	if party is None:
    		return self._results
    	else:
	        try:
	            return self._results[party]
	        except KeyError:
	            return 0

    def change_result(self,party,new):
        try:
            self._results[party] = new
        except KeyError:
            pass

    def tpp(self):
        if self._TPP is None:
            print 'Poll Error: Poll (pollster' + self._pollster + 'on ' +str(self._mediandate) +' did not include two-party preferred data.'
            return 0.00
        else:
            return self._TPP

    def join_coalition(self):

    	liberal = 0
    	national = 0
    	liberal_party = None
    	national_party = None

    	for party in ['LIB', 'LP', 'LNQ']:
	        if self.results(party) > 0:
	            liberal = liberal + self.results(party)
	            liberal_party = party
		for party in ['NAT', 'NP']:
			if self.results(party) > 0:
				national = national + self.results(party)
	    		national_party = party
		results_dict = {'COA': liberal + national}
		for party in self._results:
			if party not in ['LIB', 'LP', 'LNQ', 'NAT', 'NP', 'COA']:
				results_dict[party] = self.results(party)
		self._results = results_dict

    def join_others(self, others = []):

    	major_parties = ['ALP', 'COA', 'LIB', 'LP', 'NP', 'NAT', 'GRN', 'LNQ', 'OTH']
    	if len(others) > 0:
    		for party in others:
    			major_parties.append(party) 
    	try:
    		others_vote = self.results('OTH')
    	except KeyError:
    		others_vote = 0
    	for party in self._results:
			if party not in major_parties:
				others_vote = others_vote + self.results(party)
        results_dict = {'OTH': others_vote}
        for party in major_parties:
			if self.results(party) > 0:
				results_dict[party] = self.results(party)
        self._results = results_dict

class Election(Poll):

    ## Elections are just polls with a huge sample size, and the 
    ## median poll date becomes the date of the election. 

    def formal_votes(self):
        return self._samplesize

    def election_date(self):
        return self._mediandate


def LoadPolls(state):

    ## This function loads into memory all polling data from 
    ## the database for a given state (or AUS for federal polls). 

    poll_list = []
    if state != 'AUS':
        filename = 'data/polling_data/' + state + '_state_polls.csv'
    else:
        filename = 'data/polling_data/FED_polls_primary.csv'
    pollframe = pd.read_csv(filename)
    if state != 'AUS':
        parties = pollframe.columns[4:-2]
    else:
        parties = pollframe.columns[2:]
    for i in range(0,len(pollframe)):
        results_dict = {}
        for party in parties:
            if not np.isnan(pollframe[party][i]):
                results_dict[party] = pollframe[party][i]
        try:
            sample_size = pollframe['N'][i]
        except KeyError:
            sample_size = np.nan
        try:
            poll_list.append(Poll(pollframe['Pollster'][i], state, 
                pd.to_datetime(pollframe['PollMedianDate'][i],dayfirst=True), 
                sample_size, results_dict, pollframe['ALP_TPP'][i]))
        except KeyError:
            poll_list.append(Poll(pollframe['Pollster'][i], state, 
                pd.to_datetime(pollframe['PollMedianDate'][i],dayfirst=True), 
                sample_size, results_dict, np.nan))
    return poll_list

def LoadElections():

    ## This function loads into memory all election results, 
    ## federal, state and territory, since 2000. 

    electionframe = pd.read_csv('data/election_data/elections_from_2000.csv')
    election_list = []
    parties = electionframe.columns[2:-2]
    for i in range(0,len(electionframe)):
        results_dict = {}
        for party in parties:
            if not np.isnan(electionframe[party][i]):
                results_dict[party] = electionframe[party][i]
        election_list.append(Election('Election', electionframe['State'][i], 
            pd.to_datetime(electionframe['Date'][i],dayfirst=True), 
            electionframe['N'][i], results_dict, electionframe['ALP_TPP'][i]))
    return election_list
