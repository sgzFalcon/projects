import os

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

datafile = os.path.expanduser('data/API_IT.NET.USER.ZS_DS2_en_csv_v2.csv')
shapefile = os.path.expanduser('maps/ne_10m_admin_0_countries.shp')

colors = 9
cmap = 'Blues'
figsize = (16, 10)
year = '2016'
cols = ['Country Name', 'Country Code', year]
title = 'Individuals using the Internet (% of population) in {}'.format(year)
imgfile = 'img/{}.png'.format(''.join(title.split()))

descripton = '''
Individuals who have used the Internet from any location in the last 3 months via any device based on the International Telecommunication Union,
World Telecommunication/ICT Development Report and database. Data: World Bank - worldbank.org • Author: Ramiro Gómez - ramiro.org'''.strip()

gdf = gpd.read_file(shapefile)[['ADM0_A3', 'geometry']].to_crs('+proj=robin')
gdf.sample(5)

df = pd.read_csv(datafile, skiprows=4, usecols=cols)
df.sample(5)

merged = gdf.merge(df, left_on='ADM0_A3', right_on='Country Code')
merged.describe()