import pandas as pd
import numpy as np
from collections import OrderedDict

parties = {'ALP', 'LIB', 'NAT', 'COA', 'DEM', 'GRN', 'ONP', 'PUP', 'KAP', 'FF', 'CD', 'OTH'}
states = {'AUS', 'NSW', 'VIC', 'SA', 'WA', 'QLD', 'TAS'}

class Poll(object):

    ##
    ## Poll objects should be initialised with
    ## a pollster, state, median date, sample size
    ## and results dict. 
    ##
    ## e.g. dummy_poll = Poll('Morgan', 'NSW', '27/1/15', 500, {'ALP': 50, 'COA': 50})
    ## 
    ## Then obtain information by
    ## dummy_poll.sample_size()
    ## dummy_poll.results('ALP')
    ##

    def __init__(self, pollster, state, mediandate, samplesize, results, TPP):
        self._pollster = pollster
        self._state = state
        self._mediandate = mediandate
        self._samplesize = samplesize
        self._results = results
        self._tpp = TPP
        self.distance = 100000  # This variable will be used to find closest polls to elections

    @property
    def pollster(self):
        return self._pollster

    def state(self):
        return self._state

    def median_date(self):
        return self._mediandate

    def sample_size(self):
        return self._samplesize

    def results(self,party):
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
        return self._tpp


class Election(Poll):

    ## elections are just polls with a huge sample size

    def formal_votes(self):
        return self._samplesize

    def election_date(self):
        return self._mediandate

def LoadPolls(state):
    poll_list = []
    if state != 'AUS':
        filename = 'data/polling_data/' + state + '_state_polls.csv'
    else:
        filename = 'data/polling_data/FED_polls_primary.csv'
    pollframe = pd.read_csv(filename)
    for i in range(0,len(pollframe)):
        results_dict = {}
        for party in parties:
            try: 
                results_dict[party] = pollframe[party][i]
            except KeyError:
                pass
        try:
            sample_size = pollframe['N'][i]
        except KeyError:
            sample_size = np.nan
        try:
            poll_list.append(Poll(pollframe['Pollster'][i], state, pd.to_datetime(pollframe['PollMedianDate'][i],dayfirst=True), sample_size, results_dict, pollframe['ALP_TPP'][i]))
        except KeyError:
            poll_list.append(Poll(pollframe['Pollster'][i], state, pd.to_datetime(pollframe['PollMedianDate'][i],dayfirst=True), sample_size, results_dict, np.nan))
    return poll_list

def LoadElections():
    electionframe = pd.read_csv('data/election_data/elections_from_2000.csv')
    election_list = []
    for i in range(0,len(electionframe)):
        results_dict = {}
        for party in parties:
            try:
                results_dict[party] = electionframe[party][i]
            except KeyError:
                pass
        election_list.append(Election('Election', electionframe['State'][i], pd.to_datetime(electionframe['Date'][i],dayfirst=True), electionframe['N'][i], results_dict, electionframe['ALP_TPP'][i]))
    return election_list

LoadPolls('AUS')