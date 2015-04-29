'''
ClusterSeats.py
---------------


'''

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

census = pd.read_csv('data/demographic_data/2006_census_data_by_division.csv')
census = census.ix[:149]

census['pop'] = census['Total_population'].astype(int)
census['var1'] = np.round(census['Labour_force_aged_45_years_and_over22'].astype(float)/census['pop'].astype(float),4)
census['var2'] = np.round((census['Overseas%'].astype(float) + 
				census['NonEngBorn%'].astype(float) + 
				census['Persons_who_speak_English_not_well_or_not_at_all'].astype(float)/census['pop'].astype(float) + 
				census['Persons_speaking_a_language_other_than_English_at_home'].astype(float)/census['pop'].astype(float))/4,4)
census['var3'] = np.round(census['Persons_employed_in_agriculture'].astype(float)/census['pop'].astype(float),4)
census['var4'] = np.round(census['Unemployed_persons'].astype(float)/census['pop'].astype(float),4)
census['var5'] = census['Median_age']
census['var6'] = census['Total_dependency_ratio3']
census['var7'] = np.round(census['Persons_aged_15_to_24_years'].astype(float)/census['pop'].astype(float),4)
census['var8'] = np.round(census['Catholic%'].astype(float),4)
census['var9'] = np.round(np.log(census['Population_density1'].astype(float)),4)

divisions = census['division']

census_data = pd.DataFrame([divisions, census['var1'], census['var2'], census['var3'], census['var4'], census['var5'], census['var6'], census['var7'], census['var8'], census['var9']]).transpose()
census_data.columns = ['divisions', 'Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']

print census_data.head()

kmeans = KMeans(2)
kmeans.fit(census_data[['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']])

census_data['2clusters'] = kmeans.labels_

kmeans = KMeans(3)
kmeans.fit(census_data[['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']])

census_data['3clusters'] = kmeans.labels_

kmeans = KMeans(6)
kmeans.fit(census_data[['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']])

census_data['6clusters'] = kmeans.labels_

kmeans = KMeans(10)
kmeans.fit(census_data[['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']])

census_data['10clusters'] = kmeans.labels_

print census_data.divisions[census_data['6clusters'] == 0]
print census_data.divisions[census_data['6clusters'] == 1]
print census_data.divisions[census_data['6clusters'] == 2]
print census_data.divisions[census_data['6clusters'] == 3]
print census_data.divisions[census_data['6clusters'] == 4]
print census_data.divisions[census_data['6clusters'] == 5]




