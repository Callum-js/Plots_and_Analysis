# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 20:44:40 2021

@author: Callum

Reads a file that contains daily weather data for 2017 from Environment and 
Climate Change Canada for CYUL (Montreal-Trudeau Airport), calculates a Linear
Regression between the Max and Min Temperatures and plots the data.
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib.ticker import AutoMinorLocator

df = pd.read_csv('http://www.cdmccray.com/python_tutorial/eng-daily-01012017-12312017.csv')

"""Select necessary Tmin and Tmax data and remove null values"""

nf = df[["Tmin", "Tmax"]]
nf.dropna(inplace = True)

"""Perform Linear Regression by fitting data to model"""
model = LinearRegression()
x = nf[["Tmin"]]
y = nf[["Tmax"]]
model.fit(x, y)
xfit = np.linspace(-30, 25, 550)
yfit = model.predict(xfit.reshape(-1,1))
score = model.score(x,y)


"""Plot the data as a scatter chart along with the 
Least Squares Regression Line"""

fig, ax = plt.subplots(figsize =  (10, 6))
nf.plot.scatter(x = "Tmin", y = "Tmax", ax = ax)
ax.plot(xfit, yfit, color = "black")
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

degree_sign= u'\N{DEGREE SIGN}'

ax.set(xlabel=f"Min. Temperature ({degree_sign}C)",
       ylabel=f"Max. Temperature ({degree_sign}C)",
       title="Montreal Daily Tmax/Tmin Least Squares Linear Regression")

print(f"Regression Coefficient: {model.coef_[0][0]:.2f}")


plt.savefig("temp_linear_regression.png")
plt.show()
plt.close(fig)