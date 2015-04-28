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

'''

census <- read.csv('2006_census_data_by_division.csv')
summary(census)
pop <- as.numeric(as.character(census$Total_population[1:150]))
Var1 <- as.numeric(as.character(census$Labour_force_aged_45_years_and_over22[1:150]))/pop
Mig1 <- as.numeric(as.character(census$Overseas[1:150]))
Mig2 <- as.numeric(as.character(census$NonEngBorn.[1:150]))
Mig3 <- as.numeric(as.character(census$Persons_who_speak_English_not_well_or_not_at_all[1:150]))/pop
Mig4 <- as.numeric(as.character(census$Persons_speaking_a_language_other_than_English_at_home[1:150]))/pop
Var2 <- (Mig1+Mig2+Mig3+Mig4)/4
Var3 <- as.numeric(as.character(census$Persons_employed_in_agriculture[1:150]))/pop
Var4 <- as.numeric(as.character(census$Unemployed_persons[1:150]))/pop
Var5 <- as.numeric(as.character(census$Median_age[1:150]))
Var6 <- as.numeric(as.character(census$Total_dependency_ratio3[1:150]))
Var7 <- as.numeric(as.character(census$Persons_aged_15_to_24_years[1:150]))/pop
Var8 <- as.numeric(as.character(census$Catholic.[1:150]))
Var9 <- log(as.numeric(as.character(census$Population_density1[1:150])))
divs <- census$division[1:150]
df = data.frame(divs, Var1, Var2, Var3, Var4, Var5, Var6, Var7, Var8, Var9)

two_clusters <- kmeans(df[,2:10],2)
df$divs[two_clusters$cluster==1]
df$divs[two_clusters$cluster==2]

three_clusters <- kmeans(df[,2:9],3)
df$divs[three_clusters$cluster==1]
df$divs[three_clusters$cluster==2]
df$divs[three_clusters$cluster==3]

ten_clusters <- kmeans(df[,2:10],10)
df$divs[ten_clusters$cluster==1]
df$divs[ten_clusters$cluster==2]
df$divs[ten_clusters$cluster==3]
df$divs[ten_clusters$cluster==4]
df$divs[ten_clusters$cluster==5]
df$divs[ten_clusters$cluster==6]
df$divs[ten_clusters$cluster==7]
df$divs[ten_clusters$cluster==8]
df$divs[ten_clusters$cluster==9]
df$divs[ten_clusters$cluster==10]

six_clusters <- kmeans(df[,2:10],6)
six_clusters
df$divs[six_clusters$cluster==1]
df$divs[six_clusters$cluster==2]
df$divs[six_clusters$cluster==3]
df$divs[six_clusters$cluster==4]
df$divs[six_clusters$cluster==5]
df$divs[six_clusters$cluster==6]
'''