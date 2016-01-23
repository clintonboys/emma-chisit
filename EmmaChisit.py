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

-------------
EmmaChisit.py
-------------

The Emma Chisit model for predicting the upcoming 2016 
Australian federal election.
'''

import pandas as pd
import numpy as np
import datetime
import Polls
import Seats
import PollsterWeights
import ClusterSeats
import RunoffElection
import PollAggregator
import ApplySwings
import MarginalTrendAdjustments

todays_date = datetime.datetime.today().date()
print todays_date

## Import pollster weights

weights = PollsterWeights.Weights

## Import preference flows



## Import seat clusters

clusters = ClusterSeats.Clusters

## Check for recent polls on the Ghost Who Tweets feed

## Compute poll aggregate

## Compute implied swing

## Adjust individual seat swings for polled marginals

## Add further adjustments for personal member effects

## Runoff each seat and provide forecast








