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

---------------------------
MarginalTrendAdjustments.py
---------------------------

v1.0  Loads marginal seat data from GhostWhoVotes
	  and outputs it as a series of polls for the
	  relevant seats. 

'''
import datetime
import SecondModel
import Polls
import Seats
import RunoffElection
import PollAggregator
import ApplySwings
import pandas as pd
import numpy as np



year = 2013

def LoadMarginals(year, seat, top_two = ['ALP', 'COA'], is_primary = False):

	tweets = pd.read_csv('data/ghost_who_votes/marginals_'+str(year)+'.csv')
	tweets.columns = ['n','date','pollster','seat','ALP_TPP','COA_TPP']
	these_tweets = tweets[tweets['seat'] == ' '+seat]
	polls = []

	if not is_primary:
		for i in range(0,len(these_tweets)):
			this_poll = Polls.Poll(these_tweets.pollster.iloc[i], these_tweets.seat.iloc[i], these_tweets.date.iloc[i], 500, {},
			                      {top_two[0]: these_tweets.ALP_TPP.iloc[i], top_two[1]: these_tweets.COA_TPP.iloc[i]})
			polls.append(this_poll)
	else:
		for i in range(0,len(these_tweets)):
			this_poll = Polls.Poll(these_tweets.pollster.iloc[i], these_tweets.seat.iloc[i], these_tweets.date.iloc[i], 500, 
				{top_two[0]: these_tweets.ALP_TPP.iloc[i], top_two[1]: these_tweets.COA_TPP.iloc[i], 'OTH': 100.0-these_tweets.ALP_TPP.iloc[i]-these_tweets.COA_TPP.iloc[i]},
				{})
			polls.append(this_poll)

	return polls


def AdjustSwing(seat, to_date, aggregated_poll, pref_flows, marginal_poll, year, top_two = ['ALP', 'COA'], is_primary = False):

	## Given a marginal seat, this function computes the adjustment
	## to the swing from that implied by the poll aggregate, using
	## a seat-level poll. 

	## Take the aggregated poll

	## Make everything compatible

	## Adjust the swing by the marginal poll

	## Clean everything up so it adds to 100 etc

	seat_results = seat.results(year)

	if not is_primary:

		## if we are given a TPP poll (most marginal polls are)
		## we get the TPP data implied by the aggregated poll and 
		## adjust the two parties' primary vote accordingly

		swings = PollAggregator.GetSwings('AUS', aggregated_poll, to_date, ['PUP'])

		after_swing = ApplySwings.ApplySwings(seat,year,swings,pref_flows)

		aggregate_implied_tpp = RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows))

		print aggregate_implied_tpp
		print marginal_poll.tpp()['ALP']
		return (aggregate_implied_tpp + marginal_poll.tpp()['ALP'])/2.0


# results2010 = SecondModel.LoadNationalSimple(2010)

# ## Load polls and perform aggregate

# poll_aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,7), 7, False, ['PUP'])

# ## Compute implied swing

# swings = PollAggregator.GetSwings('AUS', poll_aggregate, datetime.datetime(2013,9,7), ['PUP'])

# prefs = pd.read_csv('data/election_data/fed_2013/pref_ag.csv')

# basic_pref_flows = {'COA' :{'ALP': 40.00, 'IND': 60.00, 'GRN': 0},
# 					'ALP': {'COA': 40.00, 'GRN':0, 'OTH': 0, 'IND': 60.00}
# 					}

# for i in range(0,len(prefs)):
# 	basic_pref_flows[prefs['party'][i]] = {'ALP': prefs['to_alp'][i], 'COA': prefs['to_coa'][i]}

# marginals = {}

# for seat in results2010:
# 	if len(LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)) > 0:
# 		marginals[seat.name] = LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)[0]

# #print marginals.values()[6].tpp()

# #print RunoffElection.GetTPP(RunoffElection.Runoff(ApplySwings.ApplySwings(results2010[30], 2010, swings,
# #	basic_pref_flows),basic_pref_flows))
# to_date = datetime.datetime(2013,9,7)
# print marginals.keys()[6]
# print marginals.values()[6].tpp()
# print results2010[122].name
# print results2010[122].results(2010)
# after_swing = ApplySwings.ApplySwings(results2010[122],2010,swings,basic_pref_flows)
# print RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, basic_pref_flows))

# print AdjustSwing(results2010[122], to_date, poll_aggregate, basic_pref_flows, marginals.values()[6], 2010, top_two = ['ALP', 'COA'], is_primary = False)