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
GenerateForecastPage.py
-----------------------

Generates the web page containing the current Emma Chisit forecast. 
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
import PreferenceCalculator
import SecondModel
import os

image_name = 'sample-image-3.jpg'

header = '''---
layout: page
title: Current forecast
image:
  feature: {0}
---

# Current seat-by-seat forecast

'''.format(image_name)

body = ''

current_forecast = pd.read_csv('current_forecast.csv').sort('state')

for state in current_forecast.state.unique().tolist():
	body = body + '## ' + state +'\n \n'
	state_frame = current_forecast[current_forecast['state'] == state]
	state_frame.index = range(0,len(state_frame))
	for i in range(0,len(state_frame)):
		body = body + '*' + state_frame['seat'].iloc[i] + '*: ' + state_frame['winner'].iloc[i] + ' (' + str(state_frame['TPP'].iloc[i]) + ') \n \n'

markdown = header + body
print markdown
with open('test.md', 'w') as file:
	file.write(markdown)


