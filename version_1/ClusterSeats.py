'''
ClusterSeats.py
---------------

For a given year and a given number of clusters,
this module clusters seats together using k-means
clustering on the relevant census data (currently 
only 2006 census data)

'''

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

def ClusterSeats(census, num_clusters):

	path = 'data/demographic_data/{0}_census_data_by_division.csv'.format(census)

	census = pd.read_csv(path)
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

	kmeans = KMeans(num_clusters)
	kmeans.fit(census_data[['Var1', 'Var2', 'Var3', 'Var4', 'Var5', 'Var6', 'Var7', 'Var8', 'Var9']])

	census_data['clusters'] = kmeans.labels_

	cluster_list = []
	for i in range(0,num_clusters):
		seat_list = []
		this_data = census_data.divisions[census_data['clusters'] == i]
		for j in range(0,len(this_data)):
			seat_list.append(this_data.iloc[j])
		cluster_list.append(seat_list)
	return cluster_list

#print ClusterSeats(2006,4)