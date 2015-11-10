__author__ = 'Amir487'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


mapdata = np.loadtxt("../input_data/mapdata_copyright_openstreetmap_contributors.txt")
plt.imshow(mapdata, cmap = plt.get_cmap('gray'))

filePath = "../input_data/train/train2007.csv"
traps = pd.read_csv(filePath)[['Species', 'Longitude', 'Latitude']].values

lon_lat_box = (-88, -87.5, 41.6, 42.1)

species = traps[:,0]
lat = traps[:,1]
lon = traps[:,2]
i = 0

plt.figure(figsize=(12., 12.))
plt.gca().set_title('Distribution of species for each trap in 2007')
plt.imshow(mapdata, extent=lon_lat_box, cmap=plt.get_cmap('gray'))

for specie in species:
    if specie == "CULEX PIPIENS/RESTUANS":
        plt.scatter(lat[i], lon[i], s=60, marker=r'$\clubsuit$', c='blue', edgecolors='blue', alpha=0.1)
    if specie == "CULEX RESTUANS":
        plt.scatter(lat[i], lon[i], s=180, marker='+', c='yellow', edgecolors='yellow', alpha=0.2)
    if specie == "CULEX PIPIENS":
        plt.scatter(lat[i], lon[i], s=100, marker='x', c='red', edgecolors='red', alpha=0.3)
    if specie == "CULEX SALINARIUS":
        plt.scatter(lat[i], lon[i], s=40, marker='o', c='black', edgecolors='black', alpha=0.3)
    if specie == "CULEX TERRITANS":
        plt.scatter(lat[i], lon[i], s=500, marker='o', c='green', edgecolors='green', alpha=0.3)
    if specie == "TARSALIS":
        plt.scatter(lat[i], lon[i], s=70, marker='o', c='pink', edgecolors='pink', alpha=0.3)
    if specie == "CULEX ERRATICUS":
        plt.scatter(lat[i], lon[i], s=90, marker='o', c='white', edgecolors='white', alpha=0.3)
    i = i + 1

plt.savefig('../plots/specie_distribution_'+"2007"+'.png')