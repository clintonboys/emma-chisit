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

    def __init__(self, pollster, state, mediandate, samplesize, results, TPP = None, others = {}):
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
        if self._TPP is None:
            print 'Poll Error: Poll (pollster' + self._pollster + 'on ' +str(self._mediandate) +' did not include two-party preferred data.'
            return 0.00
        else:
            return self._TPP

class Election(Poll):

    ## Elections are just polls with a huge sample size, and the 
    ## median poll date becomes the date of the election. 

    def formal_votes(self):
        return self._samplesize

    def election_date(self):
        return self._mediandate

