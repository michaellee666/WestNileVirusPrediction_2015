import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st_1 = [-87.933, 41.995]
st_2 = [-87.752, 41.786]

mapdata = np.loadtxt("../input_data/mapdata_copyright_openstreetmap_contributors.txt")

lon_lat_box = (-88, -87.5, 41.6, 42.1)
plt.figure(figsize=(6,6))
plt.title("Locations of the weather stations")
plt.imshow(mapdata, extent=lon_lat_box, cmap=plt.get_cmap('gray'))
plt.scatter(st_1[0], st_1[1], marker='x', s=80, c=u'r')
plt.scatter(st_2[0], st_2[1], marker='x', s=80, c=u'b')
plt.savefig('../plots/weather_stations.png')
