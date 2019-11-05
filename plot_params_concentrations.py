#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 14:35:25 2019

Niektore parametre pre vykreslovanie rocnych poli koncentracii

@author: p2993
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.geometry import Polygon
import xarray as xr
import contextily as ct
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import cartopy.feature as cfeature


# Limit values for filtering:
lim = {
       'BaP': 2.0,
       'PM10': 25.0,
       'PM25': 15.0,
       'NOx': 2.0,
       'SO2':1.75
       }
stations = {
        'jelsava250':(254582, 103817),
        'ruzomberok250':(185574, 153372 ),
        'bystrica250':(174629, 115175),
        'bystrica250z':(171700, 114981)
}
stname = {
        'jelsava250':'AMS Jesenského',
        'ruzomberok250': 'AMS Riadok',
        'bystrica250': 'AMS Štefánik.náb.'
        }
domname = {
        'jelsava250':'Jelšava',
        'ruzomberok250': 'Ružomberok',
        'bystrica250': 'Banská Bystrica'
        }

crsLCC = {
  'proj': 'lcc',
 'lat_1': 48.75,
 'lat_2': 49,
 'lat_0': 47.7,
 'lon_0': 19.5,
 'x_0': 200000,
 'y_0': 0,
 'ellps': 'WGS84',
 'units': 'm',
 'no_defs': True
 }

# Vytvorenie gpd objektu z dictionary stanic:
def stanice(stations):
    st = pd.Series(stations, name='points')
    st = st.to_frame()
    st['geometry'] = st.points.apply(Point)
    st = gpd.GeoDataFrame(st, geometry='geometry', crs=crsLCC)
    
    return st

# Zistenie extentu z xarray Con a jeho projekcia do lat/lon(pre cartopy):
def get_lalo_extent_from_xarray(Con):
    x, y = Con.x.values, Con.y.values
    bb = {'ll':(x.min(),y.min()),
          'ur':(x.max(),y.max())
          }
    bb = pd.Series(bb, name='points')
    bbdf = bb.to_frame()
    bbdf['geometry'] = bbdf.points.apply(Point)
    bbgdf = gpd.GeoDataFrame(bbdf, geometry='geometry', crs=crsLCC)
    bbgdf = bbgdf.to_crs(epsg=4326)
    b = bbgdf.total_bounds
    extent = [b[0], b[2], b[1], b[3]]
    return extent

levely = {
        'PM10':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60,160],
        'PM25':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60,160],
        'NOx':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60,160],
        'NO2':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60]
        }
levely_lab = {
        'PM10':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60],
        'PM25':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60],
        'NOx':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50,60],
        'NO2':[1,2,4,6,8,10,12,14,16,18,20,22,25,26,28,30,32,36,40,50]
        }

# Zadefinovanie stringu pre jednotky
def unit_string(spc):
    # add unit text string
    if spc == 'BaP':
        unit = '$ng /m^3$'
    else:
        unit = '$\mu g /m^3$'
    return unit    

# Konverzia xarray v LCC projekcii do geodataframe (bez zmeny projekcie):
def xarray_to_gdf (C, res):
    '''
    C - xarray, res - jeho rozlisenie
    '''
    con = C.to_dataframe()
    # Vytvorenie geometrie:
    d = res/2
    for i in list(con.index):
        
        # Construction of the polygons:
        xplus = i[1]+d
        xminus = i[1]-d
        yplus = i[0]+d
        yminus = i[0]-d
        p = '[[{}, {}], [{}, {}], [{}, {}], [{}, {}], [{}, {}]]'.format(xminus, yminus,
             xminus, yplus, xplus, yplus, xplus, yminus, xminus, yminus )
        con.loc[i,'poly'] = p
    
    con['geometry'] = con.poly.apply(lambda x: Polygon(eval(x)))
    # konverzia df na gdf:
    consh = gpd.GeoDataFrame(con, geometry='geometry', crs=crsLCC)
    return consh


def plot_context (C, spc, figtitle, amsx, amsy, amsname, outfile, aspect):
    '''
    Funkcia na vykreslovanie rastra zoshapovanehoj do geodataframe. Parametre:
    C - geodataframe s mriezkou a hodnotami na zobrazenie v stlpci 'col'
    unit - string s jednotkami 
    figtitle - nazov mapy ktory chceme zobrazit
    ams - tuple alebo list s x a y suradnicou stanice ktoru chceme zobrazit
    amsname - string s nazvom stanice ktory chceme zobrazit
    outfile - cesta k vyslednemu obrazku
    aspect - pomer vysky a sirky domeny
    '''    
    cmap = 'hot_r'
        
    plt.rcParams.update({'xtick.labelsize': 16})
    plt.rcParams.update({'ytick.labelsize': 16})
    
    fig, ax = plt.subplots(1, figsize = (15, 15*aspect))
    
    C.plot(column=spc, ax=ax , cmap=cmap, alpha=0.4, edgecolor=None, legend=True)
    ax.axis('off')
    ct.add_basemap(ax)
    ax.set_title(figtitle, fontdict={'fontsize': '20', 'fontweight' : '4'})
    
    plt.plot(amsx, amsy,'o', markerfacecolor='red', markeredgecolor='black')
    plt.text(amsx-400, amsy+150 , amsname, color='black', fontsize=12)
    plt.tight_layout()
    
    plt.savefig(outfile, dpi=300, bbox_inches='tight')

def plot_cartopy_cont (proj, C, spc, figtitle, amsx, amsy, amsname, outfile, aspect):
    '''
    Funkcia na vykreslovanie rastra xarray, CONTOURS Parametre:
    C - geodataframe s mriezkou a hodnotami na zobrazenie v stlpci 'col'
    unit - string s jednotkami 
    figtitle - nazov mapy ktory chceme zobrazit
    ams - tuple alebo list s x a y suradnicou stanice ktoru chceme zobrazit
    amsname - string s nazvom stanice ktory chceme zobrazit
    outfile - cesta k vyslednemu obrazku
    aspect - pomer vysky a sirky domeny
    '''    
    cmap = 'CMRmap_r'
    plt.rcParams.update({'font.size': 16})        
    plt.rcParams.update({'xtick.labelsize': 16})
    plt.rcParams.update({'ytick.labelsize': 16})
    plt.rcParams['figure.figsize'] = 15, 15*aspect
    
    mapsource = cimgt.GoogleTiles(style='satellite')
    extent = get_lalo_extent_from_xarray(C)
    
    ax = plt.axes(projection=proj)
    ax.set_extent(extent)
    ax.add_image(mapsource, 13, interpolation='bilinear')
    a = C.plot.contour(cmap=cmap, add_colorbar=False, linewidths=3)
    # a = c.plot( levels=levely[spc], alpha=0.5, cmap=cmap, add_colorbar=False)
    cb = plt.colorbar(a,label=unit_string(spc), orientation="vertical", shrink=0.62)
    cb.outline.set_visible(False)
    ax.set_title(figtitle, fontdict={'fontsize': '20', 'fontweight' : '4'})
    
    plt.plot(amsx, amsy,'o', markerfacecolor='red', markeredgecolor='black')
    plt.text(amsx-400, amsy+150 , amsname, color='white', fontsize=12)
    
    plt.tight_layout()
    
    plt.savefig(outfile, dpi=300, bbox_inches='tight')    
    
def plot_cartopy_rast (proj, C, spc, figtitle, amsx, amsy, amsname, outfile, aspect):
    '''
    Funkcia na vykreslovanie rastra xarray, CONTOURS Parametre:
    C - xarray s mriezkou a hodnotami na zobrazenie v stlpci 'col'
    unit - string s jednotkami 
    figtitle - nazov mapy ktory chceme zobrazit
    ams - tuple alebo list s x a y suradnicou stanice ktoru chceme zobrazit
    amsname - string s nazvom stanice ktory chceme zobrazit
    outfile - cesta k vyslednemu obrazku
    aspect - pomer vysky a sirky domeny
    '''    
    #cmap = 'CMRmap_r'
    cmap = 'cubehelix_r'      
    plt.rcParams.update({'font.size': 16})
    plt.rcParams.update({'xtick.labelsize': 16})
    plt.rcParams.update({'ytick.labelsize': 16})
    plt.rcParams['figure.figsize'] = 15, 15*aspect
    
    mapsource = cimgt.Stamen(style='terrain')
    extent = get_lalo_extent_from_xarray(C)
    
    ax = plt.axes(projection=proj)
    ax.set_extent(extent)
    ax.add_image(mapsource, 13, interpolation='bilinear')
    a = C.plot.pcolormesh( alpha = 0.5, cmap=cmap,linewidth=0, antialiased=True,add_colorbar=False)
    # a = c.plot( levels=levely[spc], alpha=0.5, cmap=cmap, add_colorbar=False)
    cb = plt.colorbar(a,label=unit_string(spc), orientation="vertical", shrink=0.62)
    
    ax.set_title(figtitle, fontdict={'fontsize': '20', 'fontweight' : '4'})
    
    plt.plot(amsx, amsy,'o', markerfacecolor='red', markeredgecolor='black')
    plt.text(amsx-400, amsy+150 , amsname, color='black', fontsize=12)
    
    plt.tight_layout()
    
    plt.savefig(outfile, dpi=300, bbox_inches='tight')    
