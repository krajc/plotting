#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 14:34:40 2019

@author: p2993
"""
import sys
sys.path.append('/home/KOL/p2993/python/libs')
import plot_params_concentrations
import xarray as xr

domena = 'ruzomberok250'
res = 250

year = 2017

data = "/data/oko/krajc/calpost/{}/Totals".format(domena)
totalf = "{}/annual-{}.nc".format(data, year)
small2f = "{}/annual-small2-{}.nc".format(data, year)
roadf = "{}/annual-road-{}.nc".format(data, year)
pointf = "{}/annual-point-{}.nc".format(data, year)

picdir = "/data/oko/krajc/calpost/CALPUFF_PICS_{}/NewPics".format(year)

# Nacitanie vseobecnych dat z externeho skriptu:
# dictionary s projekciou LCC:
crsLCC = plot_params_concentrations.crsLCC
# dictionary so suradnicami stanic v LCC:
stations = plot_params_concentrations.stations
# Geodataframe so suradnicami stanic v LCC:
stgpd = plot_params_concentrations.stanice(stations)
# Dictionary s civilnymi nazvami domen:
domname = plot_params_concentrations.domname
stname = plot_params_concentrations.stname
# Dictionares s levelmi na vykreslovanie izociar a barplotu 
levely = plot_params_concentrations.levely
levely_lab = plot_params_concentrations.levely_lab
# Limity pre filtrovanie pola na zobrazovanie:
lim = plot_params_concentrations.lim

# Otvorenie datasetu pre celkove rocne konc. danej domeny
total = xr.open_dataset(totalf)
# Odbocka: zistenie aspect ratio pre domenu kvoli obrazkom:
nx, ny = total.PM10.shape
asp = ny/nx

spc = 'PM25'

# Nacitanie rastra pollutantu
c = total[spc]
# odfiltrovanie nizkych hodnot:
c = c.where(c > lim[spc])

#### Vytvorenie geodataframe z xarray rastra ktory chceme zobrazit:
conshp = plot_params_concentrations.xarray_to_gdf(c, res)

# Konverzia geodataframe do cielovej projekcie na zobrazovanie:
C = conshp.to_crs(epsg=3857)

figtitle = "Priemerné ročné koncentrácie {} - {} - {}".format(spc, domname[domena], year)

# Konverzia geodataframe poloh stanic do cielovej projekcie:
stgpd = stgpd.to_crs(epsg=3857)
# Vytiahnutie suradnic stanic v domene:
amsx, amsy = stgpd.geometry.loc[domena].x, stgpd.geometry.loc[domena].y
# Nazov stanice ktory chceme zobrazit:
amsname = stname[domena]
# Nazov vysledneho suboru:
outfile = "{}/{}-{}-{}-total.png".format(picdir, domena, spc, year)


# Vykreslenie obrazka s pozadovou mapou pomocou contextily
plot_params_concentrations.plot_context (C, spc, figtitle, amsx, amsy, amsname, outfile, asp)


'''
fig, ax = plt.subplots(1, figsize=(13, 13))
im = C.plot(column='BaP', ax=ax, cmap=cmap, alpha=0.4, edgecolor=None, legend=True)
ax.axis('off')
ax.set_title('Priemerné ročné koncentrácie BaP v Banskej Bystrici\n', fontdict={
        'fontsize': '20', 'fontweight' : '4'})
ct.add_basemap(ax)
'''


'''
for i in  list(con.index):
    # x a y su vymenene, preto ich treba prehodit
    p = i[::-1]
    con.loc[i, 'geom'] = str(p)

con['geometry'] = con.geom.apply(lambda x: Point(eval(x)))
'''