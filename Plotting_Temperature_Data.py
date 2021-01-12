# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 15:37:05 2021

@author: Callum

Reads a file that contains daily weather data for 2017 from Environment and 
Climate Change Canada for CYUL (Montreal-Trudeau Airport) and produces a graph 
of Daily Max/Min and rolling mean Temperatures over the year. 

"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np

df = pd.read_csv('http://www.cdmccray.com/python_tutorial/eng-daily-01012017-12312017.csv')

months = mdates.MonthLocator()
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace = True)

"""Interpolate for null values"""
nf = df["Tmax"].interpolate()
mf = df["Tmean"].interpolate()

"""Calculate 30 day rolling average of Tmean"""
mf["Roll_av"] = mf.rolling(window = 30, min_periods= 2, center = True).mean()
z = pd.DataFrame(np.zeros(len(nf)), index = nf.index, columns =["_"])

"""Plot the data"""
fig, ax = plt.subplots(figsize=(10, 6))

nf.plot(ax = ax, color = "red", label = "Tmax")
df["Tmin"].plot(ax = ax, color = "blue", label = "Tmin")
mf["Roll_av"].plot(ax = ax, color = "black", label = "30 day avg. Tmean")
z.plot(ax = ax, color = "black", label = "None")

"""Align the xaxis ticks with the start of each month and alter labels"""
ax.xaxis.set_major_locator(months)
date_form = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(interval = 1))

degree_sign= u'\N{DEGREE SIGN}'

ax.set(xlabel="2017",
       ylabel=f"Temperature ({degree_sign}C)",
       title="Montreal Daily Temperatures 2017")

plt.grid()
plt.legend()
plt.show()