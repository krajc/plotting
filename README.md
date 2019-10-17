# plotting
plot_params_concentrations.py obsahuje okrem roznych uzitocnych funkcii pre vykreslovanie xarray (resp. netcdf) dat z mojich high resolution domen, funkcie na vykreslenie koncentracii NA POZADOVYCH MAPACH pomocou contextily a cartopy. 
Contextily je velmi jednoduche ale neviem tam vybrat druh pozadia, co sposobuje napr. pri jelsave problem, lebo su tam chybajuce tiles na serveri. Okrem toho Contextily vykresluje iba shapes, resp. geodataframes, takze raster treba predtym skonvertovat na gpd ... tiez tam mam na to funkciu. 
Odporucam pouzivat cartopy, mam tam 2 funkcie, jedna vykresluje na fotomape kontury, druha na terennej mape priesvitny raster.
Pozadove mapy mozno menit pomocou zadefinovania mapsource. S colormap sa treba pohrat aby to vyzeralo dobre. 
