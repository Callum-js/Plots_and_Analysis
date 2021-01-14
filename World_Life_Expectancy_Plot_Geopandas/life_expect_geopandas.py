# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 20:09:57 2021

@author: Callum

Here I used a dataset from World Health Statistics 2020/Complete/Geo Analysis 
downloadable from Kaggle. I read in the file of Life Expectancy at Birth, 
selected the relevant data from 2019 and then produced a Choropleth style plot
using geopandas.
"""
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

"""Read a file where I have corrected country names in order to match the 
names in the geopandas world dataset. This allows the datasets to be merged
for plotting"""
df = pd.read_csv("lifeExpectancyAtBirth2.csv")
#drop the original file country names and select desired data
df.drop(["Location"], axis = 1, inplace = True)
df_19 = df[(df["Period"]==2019) & (df["Dim1"]=="Both sexes")]

#Set index to country name
df_19.set_index("name", inplace = True)
#Read in geopandas world dataframe and select populated countries/territories
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[(world.pop_est>0) & (world.name!="Antarctica")]
#Merge the world and life exp. dataframes on country
world = world.merge(df_19["First Tooltip"], how = "left", left_on = "name", right_index=True)

#Plot the map
fig, ax = plt.subplots(figsize=(10,6))
world.plot(ax = ax, column = "First Tooltip", edgecolor="black", linewidth = 0.3, \
           legend = True, \
           legend_kwds = {"label": "Avg. Life Expectancy at Birth (m/f)", \
                          'orientation': "horizontal"})

plt.savefig('world_life_expectancy_plot.pdf')
