import pandas as pd
import math
import re
from pandas import DataFrame
from datetime import datetime

pd.options.mode.chained_assignment = None  # default='warn'

sat = pd.read_csv('sat.csv')

sat = sat.dropna()
sat.index = range(0,len(sat))
sat.columns = ['PollRange', 'Satisfied', 'Dissatisfied', 'Uncommitted']

sat['PollStartDate'] = 0
sat['PollEndDate'] = 0
# for i in range(0,len(sat)):
# 	print sat['PollRange'][i], len(str(sat['PollRange'][i]).split())


month_list_part = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
month_list_full = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_list_four = ['Janu', 'Febr', 'Marc', 'Apri', 'May', 'June', 'July', 'Augu', 'Sept', 'Octo', 'Nove', 'Dece']


start_dates = []
end_dates = []

for i in range(0,len(sat)):
	if len(str(sat['PollRange'][i]).split(' ')) == 3:
		split = str(sat['PollRange'][i]).split(' ')
		dates = split[0].split('-')
		if len(split[1]) == 4:
			sat['PollStartDate'][i] = dates[0] + '/' + str(month_list_four.index(split[1])+1) + '/' + str(split[2])
			sat['PollEndDate'][i] = dates[1] + '/' + str(month_list_four.index(split[1])+1) + '/' + str(split[2])
		else:
			sat['PollStartDate'][i] = dates[0] + '/' + str(month_list_full.index(split[1])+1) + '/' + str(split[2])
			sat['PollEndDate'][i] = dates[1] + '/' + str(month_list_full.index(split[1])+1) + '/' + str(split[2])
	elif len(str(sat['PollRange'][i]).split(' ')) == 6 and '&' not in str(sat['PollRange'][i]).split(' '):
		split = str(sat['PollRange'][i]).split(' ')
		if len(split[1]) == 3:
			sat['PollStartDate'][i] = split[0] + '/' + str(month_list_part.index(split[1])+1) + '/' + str(split[5])
		elif len(split[1]) == 4:
			sat['PollStartDate'][i] = split[0] + '/' + str(month_list_four.index(split[1])+1) + '/' + str(split[5])
		else:
			sat['PollStartDate'][i] = split[0] + '/' + str(month_list_full.index(split[1])+1) + '/' + str(split[5])
		if len(split[4]) == 3:
			sat['PollEndDate'][i] = split[3] + '/' + str(month_list_part.index(split[4])+1) + '/' + str(split[5])
		elif len(split[4]) == 4:
			sat['PollEndDate'][i] = split[3] + '/' + str(month_list_four.index(split[4])+1) + '/' + str(split[5])
		else:
			sat['PollEndDate'][i] = split[3] + '/' + str(month_list_full.index(split[4])+1) + '/' + str(split[5])
	elif len(str(sat['PollRange'][i]).split(' ')) == 9:
		split = str(sat['PollRange'][i]).split(' ')
		if len(split[1]) == 3:
			sat['PollStartDate'][i] = split[0] + '/' + str(month_list_part.index(split[1])+1) + '/'+ str(split[8])
		else:
			sat['PollStartDate'][i] = split[0] + '/' + str(month_list_full.index(split[1])+1) + '/'+ str(split[8])
		if len(split[4]) == 3:
			sat['PollEndDate'][i] = split[3] + '/' + str(month_list_part.index(split[4])+1) + '/' + str(split[8])
		else:
			sat['PollEndDate'][i] = split[3] + '/' + str(month_list_full.index(split[4])+1) + '/' + str(split[8])
	elif len(str(sat['PollRange'][i]).split(' ')) == 5:
		split = str(sat['PollRange'][i]).split(' ')
		if len(str(split[0]).split('-')) == 2:
			sat['PollStartDate'][i] = str(split[0]).split('-')[0] + '/' + str(month_list_full.index(split[3])+1) + '/' + str(split[4])
			sat['PollEndDate'][i] = str(split[0]).split('-')[1] + '/' + str(month_list_full.index(split[3])+1) + '/' + str(split[4])
		else:
			split = str(sat['PollRange'][i]).split(' ')
			sat['PollStartDate'][i] = str(split[0]) + '/' + str(month_list_full.index(split[3])+1) + '/' + str(split[4])
			sat['PollEndDate'][i] = str(split[2]) + '/' + str(month_list_full.index(split[3])+1) + '/' + str(split[4])
	elif len(str(sat['PollRange'][i]).split(' ')) == 4:
		split = str(sat['PollRange'][i]).split(' ')
		if len(str(split[1]).split('-')[0]) == 3:
			sat['PollStartDate'][i] = str(split[0]) + '/' + str(month_list_part.index(str(split[1]).split('-')[0])+1) + '/' + str(split[3])
			sat['PollEndDate'][i] = str(str(split[1]).split('-')[1]) + '/' + str(month_list_four.index(split[2])+1) + '/' + str(split[3])
		else:
			sat['PollStartDate'][i] = str(split[0]) + '/' + str(month_list_full.index(str(split[1]).split('-')[0])+1) + '/' + str(split[3])
			sat['PollEndDate'][i] = str(str(split[1]).split('-')[1]) + '/' + str(month_list_full.index(split[2])+1) + '/' + str(split[3])
	elif len(str(sat['PollRange'][i]).split(' ')) == 6:
		split = str(sat['PollRange'][i]).split(' ')
		sat['PollStartDate'][i] = str(str(split[0]).split('-')[0]) + '/' + str(month_list_full.index(split[4])+1) + '/' + str(split[5])
		sat['PollEndDate'][i] = str(str(split[3]).split('-')[0]) + '/' + str(month_list_full.index(split[4])+1) + '/' + str(split[5])
	elif len(str(sat['PollRange'][i]).split(' ')) == 7:
		split = str(sat['PollRange'][i]).split(' ')
		if split[6] == '1988':
			sat['PollStartDate'][i] = '29/7/1988'
			sat['PollEndDate'][i] = '21/8/1988'
		else:
			sat['PollStartDate'][i] = '10/11/1989'
			sat['PollEndDate'][i] = '26/11/1989'
	elif len(str(sat['PollRange'][i]).split(' ')) == 8:
		split = str(sat['PollRange'][i]).split(' ')
		if split[7] == '1987':
			sat['PollStartDate'][i] = '13/2/1987'
			sat['PollEndDate'][i] = '1/3/1987'
		else:
			sat['PollStartDate'][i] = '8/4/1988'
			sat['PollEndDate'][i] = '1/4/1988'
	else:
		sat['PollStartDate'][i] = '29/6/1990'
		sat['PollEndDate'][i] = '29/7/1990'


median_dates = []
for i in range(0,len(sat)):
	try:
		median_dates.append(pd.to_datetime(sat['PollStartDate'][i], dayfirst = True) + (pd.to_datetime(sat['PollEndDate'][i],dayfirst = True) - pd.to_datetime(sat['PollStartDate'][i],dayfirst = True))/2)
	except TypeError:
		print pd.to_datetime(sat['PollStartDate'][i]), '\n', pd.to_datetime(sat['PollEndDate'][i])
		pass	

sat['PollMedianDate'] = 0
sat['NetSat'] = 0

for i in range(0,len(sat)):
	sat['PollMedianDate'][i] = median_dates[i]
	sat['NetSat'][i] = int(sat['Satisfied'][i]) - int(sat['Dissatisfied'][i])

sat = sat.drop('PollRange',1)

sat = sat[['PollStartDate', 'PollEndDate', 'PollMedianDate', 'Satisfied', 'Dissatisfied', 'NetSat', 'Uncommitted']]

sat.to_csv('leader_satisfaction.csv')

