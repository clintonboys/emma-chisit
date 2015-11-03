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

def ComputePreferences(primary_results, independent_leanings = 'right'):

	## Takes as input a dictionary of primary results, together 
	## with a political leaning of the independent candidate(s). 

	master_preferences = pd.read_csv('AntonyGreenPreferences.csv')

	print primary_results.keys()



	## Get a list of all the parties

dummy = {'ALP': 0.32, 'COA': 0.31, 'GRN': 0.12, 'PUP': 0.13, 'KAP':0.06, 'SEX':0.02, 'IND':0.04}
independent_leanings = 'left'

print ComputePreferences(dummy, independent_leanings)

