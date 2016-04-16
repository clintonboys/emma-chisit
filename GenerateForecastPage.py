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
---

![image](imager.jpg)

# Current seat-by-seat forecast (Mackerras pendulum)


'''

body = ''

current_forecast = pd.read_csv('current_forecast.csv').sort('state')

this_time = datetime.datetime.now() - datetime.timedelta(hours = -7)
current_day = str(this_time.day)
current_month = str(this_time.month)
current_year = str(this_time.year)
current_time = this_time.time()
current_hour = str(this_time.hour)
current_minutes = '0'*(2-len(str(this_time.minute)))+str(this_time.minute)

body = body +"Forecast last updated on %s/%s/%s at %s:%s AEST \n\n"%(current_day, current_month, current_year, current_hour, current_minutes) 

# for state in current_forecast.state.unique().tolist():
# 	body = body + '## ' + state +'\n \n'
# 	state_frame = current_forecast[current_forecast['state'] == state]
# 	state_frame.index = range(0,len(state_frame))
state_frame = current_forecast.sort('TPP')
state_frame_ALP = state_frame[state_frame['winner'] == 'ALP']
state_frame_COA = state_frame[state_frame['winner'] == 'COA']
state_frame_OTH = state_frame[state_frame['winner'] != 'ALP'][state_frame['winner'] != 'COA']

ALP_seats = len(state_frame_ALP)
state_frame_ALP.index = range(0,ALP_seats)
COA_seats = len(state_frame_COA)
state_frame_COA.index = range(0,COA_seats)

print state_frame_ALP.head()

if ALP_seats >= COA_seats:
	for i in range((COA_seats),(ALP_seats)):
		state_frame_COA.loc[i] = [i, '','','',np.nan]
else:
	for i in range((ALP_seats),(COA_seats)):
		state_frame_ALP.loc[i] = [i, '','','',np.nan]

# print state_frame_ALP
# print state_frame_COA

lengths = []
for i in range(0,ALP_seats):
	lengths.append(len(state_frame_ALP.seat.iloc[i])+15)
for i in range(0,COA_seats):
	lengths.append(len(state_frame_COA.seat.iloc[i])+15)

body = body + '| ALP'+ ' '*(max(lengths)-4)+ '| COA' + ' '*(max(lengths)-4) + '|\n'
body = body + '|'+ '-'*max(lengths) + '|' + '-'*max(lengths) + '|\n'

for i in range(0,len(state_frame_ALP)):
	body = body + '|*' + state_frame_ALP.seat.iloc[i] + '*: ' + state_frame_ALP.state.iloc[i] + ' (' + str(state_frame_ALP.TPP.iloc[i])+ ')' + ' '*(max(lengths) - 7 - len(state_frame_ALP.seat.iloc[i]) - len(state_frame_ALP.state.iloc[i]) - len(str(state_frame_ALP.TPP.iloc[i]))) + '|*' +state_frame_COA.seat.iloc[i] + '*: ' + state_frame_COA.state.iloc[i] + ' (' + str(state_frame_COA.TPP.iloc[i]) + ')' + ' '*(max(lengths) - 7 - len(state_frame_COA.seat.iloc[i]) - len(state_frame_COA.state.iloc[i]) - len(str(state_frame_COA.TPP.iloc[i]))) + '|\n'
body = body.replace('**:  (nan)','          ')
# for i in range(0,len(state_frame)):
# 	body = body + '*' + state_frame['seat'].iloc[i] + '*: ' + state_frame['winner'].iloc[i] + ' (' + str(state_frame['TPP'].iloc[i]) + ') \n \n'

markdown = header + body
print markdown
with open('test.md', 'w') as file:
	file.write(markdown)


