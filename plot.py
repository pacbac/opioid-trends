# -*- coding: utf-8 -*-
"""plot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AUPvFP0MMr0siziFfLGg1QfGjqGCX4nW
"""

import csv
import matplotlib.pyplot as plt

with open("latlng.csv") as counties:
      countyReader = csv.DictReader(counties)

      for county in countyReader:
          plt.plot(float(county['Longitude']),float(county['Latitude']),'b.')
 
plt.show()