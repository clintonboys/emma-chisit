import datetime
import SecondModel
import PollAggregator
import ClusterSeats
import MarginalTrendAdjustments

## Load 2010 results

results2010 = SecondModel.LoadNationalSimple(2010)

## Load polls and perform aggregate

poll_aggregate = PollAggregator.AggregatePolls('AUS', datetime.datetime(2013,9,7), 7, False, ['PUP'])

## Compute implied swing

swings = PollAggregator.GetSwings('AUS', poll_aggregate, datetime.datetime(2013,9,7), ['PUP'])

## Compute seat clusters

clusters = ClusterSeats.ClusterSeats(2006,6)

## Load marginal polls

marginals = {}

for seat in results2010:
	if len(MarginalTrendAdjustments.LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)) > 0:
		marginals[seat.name] = MarginalTrendAdjustments.LoadMarginals(2013, seat.name, top_two = ['ALP', 'COA'], is_primary = False)[0]

## For each marginal seat:

	## adjust the swing according to the marginal poll and the STM

	## perform runoffs to get result 

## For each non-marginal seat:

	## check if its in a cluster with a single marginal

	## if so, adjust the swing according to this poll and the STM

	## perform runoffs to get results