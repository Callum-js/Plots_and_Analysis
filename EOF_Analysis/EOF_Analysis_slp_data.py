# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 20:25:24 2021

@author: Callum
"""
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from eofs.xarray import Eof


datafile = 'ds010.1.19800100.20200131.nc'
#Open the dataset and print out metadeta
#print(ds)
ds = xr.open_dataset(datafile)
#print(ds)

lat = ds["lat"]
slp = ds["slp"]
time = ds["time"]

#Reassign longitude coords from 0-360 to -180 to 180 for easier analysis across meridian.
#Select desired subset of data. Here lon from 60W - 30E
slp = slp.assign_coords(lon=(((slp.lon + 180) % 360) - 180)).sortby('lon')
slp = slp.sel(lon = slice(-60, 30))
lon = slp["lon"]

#Select winter slp data
slp_DJF = slp.where(slp['time.season'] == 'DJF')

#find a rolling mean to group and average of each winter
#A min of three periods mean loose Jan/Feb in first year and Dec in the last
slp_DJF = slp_DJF.rolling(min_periods=3, center=True, time=3).mean()
# make annual mean for each winter
slp_DJF = slp_DJF.groupby('time.year').mean('time')

#average over time to get climatology and subtract for anomalies
DJF_climo = slp_DJF.mean(dim="year")
DJF_anoms = slp_DJF - DJF_climo
DJF_anoms = DJF_anoms.sel(year = slice("1981","2019"))

DJF_anoms = DJF_anoms.rename({"year":"time"})

# Create an EOF solver to do the EOF analysis. Square-root of cosine of
# latitude weights are applied before analysis to equate contribution from lats.
coslat = np.cos(np.deg2rad(lat.values))

wgts = np.sqrt(coslat)[..., np.newaxis]

solver = Eof(DJF_anoms, weights=wgts)

#Extract the leading EOF, expressed as the correlation between the leading
#PC time series and the input DJF slp anomalies at each grid point.
eof1 = solver.eofsAsCorrelation(neofs=1)

#Find the leading EOF PC time series and the variance explained by the leading EOF
pc1 = solver.pcs(npcs=1, pcscaling=1)
var = solver.varianceFraction(neigs = 1)


def Plot_map():
    #create projections
    proj = ccrs.LambertConformal(central_longitude=0.0, central_latitude=50.0, standard_parallels=[45])
    fig, ax = plt.subplots(subplot_kw = dict(projection = proj), figsize=(10,8))
    
    #Set area we want to see
    ax.set_extent([-65, 40, 10, 80])
    
    #map features
    ax.add_feature(cfeature.LAND, facecolor = "0.9")
    ax.add_feature(cfeature.LAKES, alpha = 0.9)
    ax.add_feature(cfeature.BORDERS, zorder=10)
    ax.add_feature(cfeature.COASTLINE, zorder=10)
    
    
    ax.gridlines(xlocs=np.arange(0,361,20), ylocs=np.arange(-80,90,20))
    
    return fig, ax

fig, ax = Plot_map()

clevs = np.linspace(-1, 1, 11)


eof_contour = ax.contourf(lon, lat, eof1[0], cmap=plt.cm.jet, levels = clevs, zorder=2, transform = ccrs.PlateCarree())

#Create a colorbar and shrink it to fit
cb = plt.colorbar(eof_contour, shrink=0.5)

ax.set_title(f'First EOF of DJF slp data 1981-2019 - variance: {var[0].values*100:.1f}%', fontsize=14)

# Plot the leading PC time series.
plt.figure()
pc1[:, 0].plot(color='b', linewidth=2)
ax = plt.gca()
ax.axhline(0, color='k')
ax.set_ylim(-3, 3)
ax.set_xlabel('Year')
ax.set_ylabel('Normalized Units')
ax.set_title('EOF1 Time Series', fontsize=16)

fig

plt.show()

