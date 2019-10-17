#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 08:06:04 2019

@author: p2993
"""

###################
import sys
sys.path.append('/home/KOL/p2993/python/libs')
import plot_params_concentrations

import xarray as xr
import numpy as np

# Nacitanie vseobecnych dat z externeho skriptu:
crsLCC = plot_params_concentrations.crsLCC
stations = plot_params_concentrations.stations
stgpd = plot_params_concentrations.stanice(stations)
levely = plot_params_concentrations.levely
levely_lab = plot_params_concentrations.levely_lab
lim = plot_params_concentrations.lim
# Dictionary s civilnymi nazvami domen:
domname = plot_params_concentrations.domname
stname = plot_params_concentrations.stname

domena = 'bystrica250'
year = 2017
data = "/data/oko/krajc/calpost/{}/Totals".format(domena)
picdir = "/data/oko/krajc/calpost/CALPUFF_PICS_{}/NewPics".format(year)

totalf = "{}/annual-{}.nc".format(data, year)
total = xr.open_dataset(totalf)

# Aspect ratio:
nx, ny = total.PM10.shape
asp = ny/nx

spc = 'PM25'
c = total[spc]

# odfiltrovanie nizkych hodnot:
#c = c.where(c > lim[spc])
extent = plot_params_concentrations.get_lalo_extent_from_xarray(c)

# Import projekcie do cartopy:
lcc = ccrs.LambertConformal(central_longitude=crsLCC['lon_0'], central_latitude=crsLCC['lat_0'],
                            standard_parallels=(crsLCC['lat_1'], crsLCC['lat_2']), 
                            false_easting=crsLCC['x_0'])

# Interpolacia kvoli plot.contour: 
nx = np.linspace(c.x[0], c.x[-1],c.shape[1]*5)
ny = np.linspace(c.y[0], c.y[-1],c.shape[0]*5)
ci = c.interp(x=nx, y=ny)

# prevod gpd stanic do cielovej projekcie na zobrazenie:
stgpd = stgpd.to_crs(crsLCC)

# Vytiahnutie suradnic stanic v domene:
amsx, amsy = stgpd.geometry.loc[domena].x, stgpd.geometry.loc[domena].y
# Nazov stanice ktory chceme zobrazit:
amsname = stname[domena]

figtitle = "Priemerné ročné koncentrácie {} \n{} - {}".format(spc, domname[domena], year)

# Vykreslovanie koncentracii - CONTOURS:
outfile = "{}/{}-{}-{}-total-contour.png".format(picdir, domena, spc, year)
plot_params_concentrations.plot_cartopy_cont (lcc, ci, spc, figtitle, amsx, amsy, 
                                              amsname, outfile, asp)

# Vykreslovanie koncentracii - RASTER:
outfile = "{}/{}-{}-{}-total-raster.png".format(picdir, domena, spc, year)
plot_params_concentrations.plot_cartopy_rast (lcc, ci, spc, figtitle, amsx, amsy, 
                                              amsname, outfile, asp)


