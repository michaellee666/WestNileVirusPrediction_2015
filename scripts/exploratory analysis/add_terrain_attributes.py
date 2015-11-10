
import pandas as pd
import numpy as np
import math ;

from scipy.spatial import distance
import collections ;

import sys 
import csv ;


    
def calculateMinDistance(terrainLocations, trapLocation):
    l=len(terrainLocations);
    minDist=sys.maxint ;
    for i in range(0,l):
        point1=np.array([terrainLocations['Latitude'][i],terrainLocations['Longitude'][i]]) ;
        point2=np.array(trapLocation);
        #dist=distance.euclidean(point1 , point2);
        lat1Rad=math.radians(point1[0]);
        lat2Rad=math.radians(point2[0]);
        
        
        latDiff = math.radians(point1[0]-point2[0]);
        longDiff= math.radians(point1[1] - point2[1]) ;
        a=math.sin(latDiff/2) *math.sin(latDiff/2) + math.cos(lat1Rad) * math.cos(lat2Rad) * math.sin(longDiff/2)*math.sin(longDiff/2);
        c=2 * math.atan2(math.sqrt(a),math.sqrt(1-a));
        R=6371000 ; #in meters
        dist=R*c ;
        if(dist < minDist):
            minDist=dist ;   
    return minDist ;


traps = pd.read_csv('../input_data/train.csv')[['Trap','Latitude','Longitude']]

#forest_locations=[(41.95166,-87.84708),(41.95714,-87.82648),(41.94974,-87.82287),(41.93403,-87.83884),(41.91500,-87.83043),(41.96480, -87.85283),(41.97808,-87.85454),(41.99332,-87.85386),(41.89648, -87.83025),(41.96557,-87.79291),(41.99645,-87.77420),(41.97948,-87.73077),(41.988892,-87.68133),(41.98190,-87.68631),(41.95817,-87.66039),(41.97501,-87.64820),(41.96493,-87.64339),(41.95191,-87.64168),(41.93518,-87.63412),(41.91526,-87.63052),(41.87433,-87.76880),(41.85754,-87.69936),(41.86585,-87.69936),(41.88317,-87.61944),(41.87384,-87.61953),(41.86662,-87.61618),(41.86655,-87.63274),(41.86042,-87.63266),(41.85428,-87.61309),(41.84635,-87.61008),(41.86604,-87.66476),(41.86208,-87.66184),(41.83299,-87.60596),(41.82506,-87.68347),(41.82486,-87.67592),(41.84047,-87.62047),(41.73232,-87.71875),(41.732068,-87.70605),(41.76895,-87.71086),(41.76869,-87.69541),(41.77509,-8765696),(41.76171,-87.63747),(41.74122,-87.65996),(41.80114,-87.61224),(41.79525,-87.61310),(41.78693,-87.61378),(41.79192,-87.58426), (41.77669,-87.58202),(41.769015,-87.60091),(41.76824,-87.56417),(41.75326,-87.54666),(41.72213,-87.52864),(41.66801,-87.73704),(41.66353,-87.73094),(41.67564,-87.70871),(41.67058,-87.70828),(41.68417,-87.73377),(41.68718,-87.72442),(41.69052,-87.72476),(41.68885,-87.69335),(41.70422,-87.69407),(41.68871,-87.59119),(41.69564,-87.58192),(41.7,-87.59154),(41.67552,-87.53043),(41.68975,-87.52682),(41.65307,-87.58948),(41.66282,-87.50159),(41.64102,-87.55137)];
#river_locations=[(33.5,72.5),(28.6,76.3)];


forest_locations =  pd.read_csv('green.csv');
river_locations =  pd.read_csv('water.csv');



uniquieTrapPoints=traps.drop_duplicates().values;
totalTraps=len(uniquieTrapPoints);
print "Total traps are";
print totalTraps;


s=np.sort(uniquieTrapPoints) ;
sorted_uniq_traps = sorted(uniquieTrapPoints, key=lambda tup: tup[0])

#two traps are repeated..total 138 traps
for x in sorted_uniq_traps:
    print (x)

dic_forest=dict();
dic_river=dict();

rows1=[None] *totalTraps ;
rows2=[None] *totalTraps;

for i in range(0, totalTraps):
    trapNumber=sorted_uniq_traps[i][0];
    trapLocation=(sorted_uniq_traps[i][1],sorted_uniq_traps[i][2]);   
    
    df=calculateMinDistance(forest_locations,trapLocation); 
    dic_forest[(trapNumber,str(sorted_uniq_traps[i][1]),str(sorted_uniq_traps[i][2]))]=df; #Dictinary key is (trap number, latitude and longitude). Some traps are found to have more than one lat,long
    rows1[i]=[trapNumber,sorted_uniq_traps[i][1],sorted_uniq_traps[i][2],df];

    dr=calculateMinDistance(river_locations,trapLocation)
    dic_river[(trapNumber,str(sorted_uniq_traps[i][1]),str(sorted_uniq_traps[i][2]))]=dr ;
    rows2[i]=[trapNumber,sorted_uniq_traps[i][1],sorted_uniq_traps[i][2],dr];
    

fileForest=open('dictForest.csv', 'wb') ;
forestWriter = csv.writer(fileForest)
print 'Forest distance from traps'


for row in rows1:
    #print(key,value);
    forestWriter.writerow(row)
fileForest.close ;

#od = collections.OrderedDict(sorted(dic_forest.items()))

# for key, value in od.items():
#     #print(key,value);
#     forestWriter.writerow([key, value])
# fileForest.close ;

fileRiver=open('dictRiver.csv', 'wb') ;
riverWriter = csv.writer(fileRiver)
print 'River distance from traps'
  
  
#od1 = collections.OrderedDict(sorted(dic_river.items()))  
for row in rows2:
    #print(key,value);
    riverWriter.writerow(row)
fileRiver.close();

in_file = open("../input_data/train.csv", "rb");
out_file = open("../input_data/train_with_terrain_attr.csv", "w")
writer = csv.writer(out_file)
reader = csv.reader(in_file)
next(reader);
header=["Date","Address","Species","Block","Street","Trap","AddressNumberAndStreet","Latitude","Longitude","AddressAccuracy","NumMosquitos","WnvPresent","Forests","WaterBodies"];
writer.writerow(header)

for row in reader:
    row_new = [None] * 14
    for i in range(0,12):
        row_new[i]=row[i];
    row_new[12]=(dic_forest[row[5],row[7],row[8]]) ;#get distance from dictionary
    row_new[13] = dic_river[row[5],row[7],row[8]]  ; #get distance from dictionary  
    writer.writerow(row_new)
in_file.close()    
out_file.close()
   


# od1 = collections.OrderedDict(sorted(dic_river.items()))  
# for key, value in od1.items():
#     #print(key,value);
#     riverWriter.writerow([key, value])
# fileRiver.close();
    
       

   
   
#     
# print 'River distance from traps'
# for key,value in dic_river.items():    
#     print(key,value)
    
  



 
