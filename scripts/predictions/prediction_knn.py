'''
Created on Jun 16, 2015

@author: bhartimunjal
'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing, metrics, ensemble, svm,neighbors

def test_classifier(clf, train):
    """Leaves one year out and trains the classifier on the rest
       then makes the prediction for the remaining year"""
    years = [2007, 2009, 2011, 2013]
    accuracies = []

    for year in years:
        # Split the training set
        new_train = train[train['Date'].apply(lambda x: x.year) != year]
        train_target = new_train['WnvPresent']
        new_train = new_train.drop('WnvPresent', axis=1)
        
        test = train[train['Date'].apply(lambda x: x.year) == year]
        test_target = test['WnvPresent']
        test = test.drop('WnvPresent', axis=1)
        
        [new_train,test]=normalizeColumns(new_train,test);
        
     
        # Train the classifier
        clf.fit(new_train.drop('Date', axis=1), train_target)
        
        # Make predictions for the left-out year
        predictions = clf.predict_proba(test.drop('Date', axis=1))[:,1]
        
        # Calculate AUC
        accuracies.append(metrics.roc_auc_score(test_target, predictions))
        
    return {'for_separate_years' : accuracies, 'average': float(sum(accuracies))/len(accuracies)}


def interpolate_params(data, attributes):
    # This version uses vectorization and is a lot faster
    # Chicago is small enough that we can treat coordinates as rectangular.
    station = np.array([[41.995, -87.933],
                         [41.786, -87.752]])
    # The distances from each training example to the weather stations:
    data['Dist1'] = (((1 - data[['Latitude', 'Longitude']] + station[0]))**2).sum(axis=1)**0.5
    data['Dist2'] = (((1 - data[['Latitude', 'Longitude']] + station[1]))**2).sum(axis=1)**0.5
    data['TotDist'] = data['Dist1'] + data['Dist2']
         
    # Take the weighted average of the attributes
    for attr in attributes:
        data[attr] = data[attr + '_x']*data['Dist1']/data['TotDist'] + data[attr + '_y']*data['Dist2']/data['TotDist']
        # Data from 2 stations is no longer needed
        data = data.drop([attr + '_x', attr + '_y'], axis=1)
    
    data = data.drop(['Dist1', 'Dist2', 'TotDist'], axis=1)

    return data

def species_vector(species):
    species_map = {'CULEX RESTUANS' : "100000",
                  'CULEX TERRITANS' : "010000",
                  'CULEX PIPIENS'   : "001000",
                  'CULEX PIPIENS/RESTUANS' : "101000",
                  'CULEX ERRATICUS' : "000100",
                  'CULEX SALINARIUS': "000010",
                  'CULEX TARSALIS' :  "000001",
                  'UNSPECIFIED CULEX': "001100"}
    return pd.Series([b for b in species_map[species]])

def normalizeColumns(train,test):
    #columns_to_be_normalised=['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']
    #data_to_be_normalised=train['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays'];
    std_scale = preprocessing.StandardScaler().fit(train[['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']]);
    train[['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']] = std_scale.transform(train[['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']]);
    #train.drop(['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays'],axis=1);
    #final_data=[train,stand_data];
    test[['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']] = std_scale.transform(test[['Latitude','Longitude','DayNumber','PrecipTotal','CumulativeHeat','CumulativePrecip','TavgOverNDays']]);
    return train,test ;

weather = pd.read_csv('../input_data/weather_clean.csv')
#spray = pd.read_csv('input_data/spray.csv')
train = pd.read_csv('../input_data/train.csv')
test = pd.read_csv('../input_data/test.csv')
sample = pd.read_csv('../input_data/sampleSubmission.csv')

weather = weather.drop(['Depart', 'DewPoint', 'WetBulb', 'CodeSum', 'Heat', 'Cool',
                        'StnPressure', 'SeaLevel', 'ResultSpeed', 'ResultDir', 'AvgSpeed', 'Sunrise', 'Sunset'], axis=1)
train = train.drop(['NumMosquitos', 'Address', 'Block', 'Street', 'AddressNumberAndStreet', 'AddressAccuracy', 'Trap'], axis=1)
test = test.drop(['Id', 'Address', 'Block', 'Street', 'AddressNumberAndStreet', 'AddressAccuracy', 'Trap'], axis=1)


weather['Date'] = weather['Date'].apply(pd.to_datetime)
# spray['Date'] = spray['Date'].apply(pd.to_datetime)
train['Date'] = train['Date'].apply(pd.to_datetime)
test['Date'] = test['Date'].apply(pd.to_datetime)

# Split data for each station
weather_st1 = weather[weather['Station'] == 1]
weather_st2 = weather[weather['Station'] == 2]

# Restore indexing
weather_st1.reset_index(drop=True, inplace=True)
weather_st2.reset_index(drop=True, inplace=True)

# Remove the station row
weather_st1 = weather_st1.drop('Station', axis=1)
weather_st2 = weather_st2.drop('Station', axis=1)



weather_st1['Heat'] = 0
weather_st2['Heat'] = 0
weather_st1['CumulativeHeat'] = 0
weather_st2['CumulativeHeat'] = 0

t_base = 72 #degrees Fahrenheit
weather_st1['Heat'] = weather_st1['Tavg'] - t_base
weather_st2['Heat'] = weather_st2['Tavg'] - t_base


# Accumulate degree days for st1 & st2
for index, row in weather_st1.iterrows():
    year = row['Date'].year
    first_row_of_year = weather_st1['Date'][weather_st1['Date'] == pd.datetime(year, 5, 1)].index[0]
    weather_st1.loc[index, 'CumulativeHeat'] = weather_st1['Heat'][first_row_of_year:index].sum()

for index, row in weather_st2.iterrows():
    year = row['Date'].year
    first_row_of_year = weather_st2['Date'][weather_st2['Date'] == pd.datetime(year, 5, 1)].index[0]
    weather_st2.loc[index, 'CumulativeHeat'] = weather_st2['Heat'][first_row_of_year:index].sum()

# 'Heat' is not needed anymore
weather_st1 = weather_st1.drop('Heat', axis=1)
weather_st2 = weather_st2.drop('Heat', axis=1)

# Transform into degree weeks
weather_st1['CumulativeHeat'] /= 7
weather_st2['CumulativeHeat'] /= 7


weather_st1['CumulativePrecip'] = 0
weather_st2['CumulativePrecip'] = 0

N_days = 14

# The predictions only begin in June while the weather is from May, 
# so it doesn't matter that calculation is overlapping on the year boundaries

for index, row in weather_st1.iterrows():
    weather_st1.loc[index, 'CumulativePrecip'] = weather_st1['PrecipTotal'][max(index-N_days, 0):index].sum()

for index, row in weather_st2.iterrows():
    weather_st2.loc[index, 'CumulativePrecip'] = weather_st2['PrecipTotal'][max(index-N_days, 0):index].sum()
    
    
    weather_st1['TavgOverNDays'] = 0
weather_st2['TavgOverNDays'] = 0

N_days = 14

# The predictions only begin in June while the weather is from May, 
# so it doesn't matter that calculation is overlapping on the year boundaries


for index, row in weather_st1.iterrows():
    weather_st1.loc[index, 'TavgOverNDays'] = weather_st1['Tavg'][max(index-N_days, 0):index].sum()/N_days

for index, row in weather_st2.iterrows():
    weather_st2.loc[index, 'TavgOverNDays'] = weather_st2['Tavg'][max(index-N_days, 0):index].sum()/N_days
    
weather = weather_st1.merge(weather_st2, on='Date')

weather['DayNumber'] = 0
for index, row in weather.iterrows():
    year = row['Date'].year
    first_day_of_summer = pd.datetime(year, 6, 1)
    weather.loc[index, 'DayNumber'] = (row['Date'] - first_day_of_summer).days
    
    
train = train.merge(weather, on='Date')
test = test.merge(weather, on='Date')


columns = ['Tmax', 'Tmin', 'PrecipTotal', 'Tavg', 'CumulativeHeat', 'CumulativePrecip', 'TavgOverNDays']
train = interpolate_params(train, columns)
test = interpolate_params(test, columns)



test[['Tmax', 'Tmin', 'Tavg', 'CumulativeHeat', 'CumulativePrecip']] = \
test[['Tmax', 'Tmin', 'Tavg', 'CumulativeHeat', 'CumulativePrecip']].applymap(round)
train[['Tmax', 'Tmin', 'Tavg', 'CumulativeHeat', 'CumulativePrecip']] = \
train[['Tmax', 'Tmin', 'Tavg', 'CumulativeHeat', 'CumulativePrecip']].applymap(round)

num_species = 6
for i in range(num_species):
    train['s' + str(i)] = 0
    test['s' + str(i)] = 0
    
train[['s0', 's1', 's2', 's3', 's4', 's5']] = train['Species'].apply(species_vector)
test[['s0', 's1', 's2', 's3', 's4', 's5']] = test['Species'].apply(species_vector)

train = train.drop('Species', axis=1)
test = test.drop('Species', axis=1)

train = train.drop(['Tmax', 'Tmin', 'Tavg'], axis=1) 
test = test.drop(['Tmax', 'Tmin', 'Tavg'], axis=1) 

clf = neighbors.KNeighborsClassifier(n_neighbors=100,weights='distance',algorithm='auto');

out=test_classifier(clf, train)
print out ;


[train.drop('WnvPresent', axis=1).columns[x] for x in [0,1,2,-1]]

train.drop('WnvPresent', axis=1).columns

train = train.drop('Date', axis=1)
test = test.drop('Date', axis=1)
clf.fit(train.drop('WnvPresent', axis=1), train['WnvPresent'])

file_name = 'temp_over_14_onehot_knn.csv'
predictions = clf.predict_proba(test)[:,1]
sample['WnvPresent'] = predictions


sample.to_csv(file_name, index=False)









