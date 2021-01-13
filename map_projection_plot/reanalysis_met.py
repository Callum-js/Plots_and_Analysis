# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:45:05 2021

@author: Callum

Here I have completed a worked example tutorial from Chris McCray https://www.cdmccray.com/python.html. 
The data file used is a NetCDF of Climate Forecast System Reanalysis (CFSR) pressure level data 
from 12 UTC 14 March 1993 on a 0.5° x 0.5° lat-lon grid (downloaded/subset from NCDC).

Through the example, xarray is used to import NetCDF data. A map projection is created using Cartopy 
and plotted with matplotlib. This example is a plot of 500hPa geopotential height (countour lines),
absolute voricity (filled contours) and wind barbs. 
"""
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage


dataFile = 'pgbh00.gdas.1993031412.nc'
#Open the dataset and print out metadeta
#print(ds)
ds = xr.open_dataset(dataFile)

"""Dataset has 4 co-ords (time, lat, lon, pressure) + 6 variables. 
   Change pressure co-ord from Pa to hPa by div. by 100"""
ds["pressure"] = ds["pressure"]/100

"""Call out necessary fields: in this case we use geopotential height
   and absolute vorticity. sel points to index of pressure field at 500hpa,
   isel uses integer index to only time value t = 0"""

lat = ds["lat"]
lon = ds["lon"]
hgt = ds["Geopotential_height"].sel(pressure = 500).isel(time=0)
avor = ds['Absolute_vorticity'].sel(pressure=500).isel(time=0)

"""Check the ranges of gph and avor using maxmin to get an idea of required range for plots""" 
#print(hgt.min())
#print(hgt.max())
#print("Avor Max: ", avor.max())
#print(avor.min())

def plotMap():
    """This function sets-up the desired map projection details using Cartopy. The function 
    returns a figure with a background map on which to plot the data"""
    
    #setup projection with map centre
    proj = ccrs.LambertConformal(central_longitude=-97.0,central_latitude=53, standard_parallels=[53])
    #Create a figure with an axes object on which we will plot. Pass the projection to that axes.
    fig, ax = plt.subplots(subplot_kw=dict(projection=proj), figsize = (10,6))
    
    #Set area we want to see
    ax.set_extent([-45, -155, 10, 90])
    
    #Add map features
    ax.add_feature(cfeature.LAND, facecolor='0.9') #Grayscale colors can be set using 0 (black) to 1 (white)
    ax.add_feature(cfeature.LAKES, alpha=0.9)  #Alpha sets transparency (0 is transparent, 1 is solid)
    ax.add_feature(cfeature.BORDERS, zorder=10)
    ax.add_feature(cfeature.COASTLINE, zorder=10)

    #We can use additional features from Natural Earth (http://www.naturalearthdata.com/features/)
    states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',  name='admin_1_states_provinces_lines',
        scale='50m', facecolor='none')
    ax.add_feature(states_provinces, edgecolor='gray', zorder=10)
    
    #Add lat/lon gridlines every 20° to the map
    ax.gridlines(xlocs=np.arange(0,361,20), ylocs=np.arange(-80,90,20)) 
    
    return fig, ax
    
fig, ax = plotMap()

"""Set the levels for the contour plot. Use a Guassian filter to smooth out the data for plotting"""
hgt_levels = np.arange(4320,6000,60)
hgt_smooth = ndimage.gaussian_filter(hgt, sigma=3, order=0)
hgt_contour = ax.contour(lon, lat, hgt_smooth, colors='k', levels=hgt_levels, linewidths=1, zorder=3, transform = ccrs.PlateCarree())

"""Now plot absolute vorticity as filled contours underneath height field, only values above 1.5e-4 /s, 
   and use the YlOrRd colormap."""
avor_levels = np.linspace(15e-5,60e-5, 10)
#Smooth the vorticity field
avor_smooth = ndimage.gaussian_filter(avor, sigma=1.5, order=0)
avor_contour = ax.contourf(lon, lat, avor_smooth, levels = avor_levels,  
                           cmap=plt.cm.YlOrRd, zorder=2, transform = ccrs.PlateCarree())

plt.clabel(hgt_contour,  hgt_levels, inline=True, fmt='%1i', fontsize=12)

#Create a colorbar and shrink it to fit
cb = plt.colorbar(avor_contour, shrink=0.5)
#Change the tick labels for appearance: Multiply avor_levels by 10^5 and round
c_avor_levels = np.around(avor_levels*10**5, 0)
cb.set_ticklabels(c_avor_levels)

"""Now pull u and v wind vector components to plot wind barbs """
urel = ds['U-component_of_wind'].sel(pressure=500).isel(time=0).values*1.944
vrel = ds['V-component_of_wind'].sel(pressure=500).isel(time=0).values*1.944

#Plot the barbs
ax.barbs(lon, lat, urel, vrel, regrid_shape=12, zorder=20, transform=ccrs.PlateCarree())

#Set the title
ax.set_title('500-hPa GPH, Wind (kts), Absolute Vorticity ($10^{-5} s^{-1}$)\n 14-03-1993 12UTC', fontsize=14)
#Show the figure
fig

plt.savefig('500_heights_winds_vort_930313_00.png', bbox_inches='tight')