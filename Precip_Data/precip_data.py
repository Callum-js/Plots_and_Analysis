# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:42:08 2021

@author: Callum

Read a file that contains daily weather data for 2017 from Environment and 
Climate Change Canada for CYUL (Montreal-Trudeau Airport) and produce a bar plot 
of Daily precip.values over the year.

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np

df = pd.read_csv('http://www.cdmccray.com/python_tutorial/eng-daily-01012017-12312017.csv')

"""Set index to datetime"""
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace = True)
nf = df[["Month","Precip"]]

#Sum over each month
#print(nf.groupby(["Month"]).sum())
#Total year precip
#print(nf["Precip"].sum())

"""Plot the data as a bar chart"""
fig, ax = plt.subplots(figsize =  (10, 6))
df["Precip"].plot.bar(ax = ax)

"""Align xticks with each month and alter format"""
months = mdates.MonthLocator()
ax.xaxis.set_major_locator(months)
date_form = DateFormatter("%b")
ax.xaxis.set_major_formatter(date_form)

ax.set(xlabel="2017",
       ylabel="Precipitation (mm)",
       title="Montreal Daily Precipitation 2017")

plt.grid()

plt.savefig("precip_data.png")
plt.show()
plt.close(fig)