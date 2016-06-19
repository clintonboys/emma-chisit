# import datetime
# import SecondModel
# import PollAggregator
# import ClusterSeats
# import MarginalTrendAdjustments
# import PreferenceCalculator
# import ApplySwings
# import RunoffElection

# ## Load 2013 results

# results2013 = SecondModel.LoadNationalSimple(2013)

# ## Load polls and perform aggregate

# poll_aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2016,2,4), 30, False, ['PUP'])
# #print poll_aggregate.results()
# ## Compute implied swing

# swings = PollAggregator.GetSwings('AUS', poll_aggregate, datetime.datetime(2013,9,7), ['PUP'])

# ## Compute seat clusters

# clusters = ClusterSeats.ClusterSeats(2006,6)

# ## Load marginal polls

# marginals = {}

# for seat in results2013:
# 	if len(MarginalTrendAdjustments.LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)) > 0:
# 		marginals[seat.name] = MarginalTrendAdjustments.LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)[0]

# print marginals

# ## For each marginal seat:

# for seat in marginals.keys():

# 	try:
# 		index = [value for value in range(0,len(results2010)) if results2010[value].name == seat][0]
# 		print seat
# 		#print results2010[index].results(2010)

# 		pref_flows = PreferenceCalculator.ComputePreferences(results2010[index].results(2010))

# 		after_swing = ApplySwings.ApplySwings(results2010[index],2010,swings,pref_flows)

# 		print RunoffElection.GetTPP(RunoffElection.Runoff(after_swing, pref_flows))



# 		print marginals[seat].tpp()['ALP']

# 	except KeyError:
# 		pass


# 	#print results2010

# 	## adjust the swing according to the marginal poll and the STM

# 	## perform runoffs to get result 

# ## For each non-marginal seat:

# 	## check if its in a cluster with a single marginal

# 	## if so, adjust the swing according to this poll and the STM

# 	## perform runoffs to get results