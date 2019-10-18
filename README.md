# plotting
plot_params_concentrations.py obsahuje okrem roznych uzitocnych funkcii pre vykreslovanie xarray (resp. netcdf) dat z mojich high resolution domen, funkcie na vykreslenie koncentracii NA POZADOVYCH MAPACH pomocou contextily a cartopy. 
Contextily je velmi jednoduche ale neviem tam vybrat druh pozadia, co sposobuje napr. pri jelsave problem, lebo su tam chybajuce tiles na serveri. Okrem toho Contextily vykresluje iba shapes, resp. geodataframes, takze raster treba predtym skonvertovat na gpd ... tiez tam mam na to funkciu. 
Odporucam pouzivat cartopy, mam tam 2 funkcie, jedna vykresluje na fotomape kontury, druha na terennej mape priesvitny raster.
Pozadove mapy mozno menit pomocou zadefinovania mapsource. S colormap sa treba pohrat aby to vyzeralo dobre. 

Tahak k xarray: https://docs.google.com/document/d/1tclnMRhYSEzMzZxYdjBIM0mSD7E4yUKYqYpBxHgZxPQ/edit?usp=sharing
Tahak na cartopy: https://docs.google.com/document/d/19KnrjI1rPdVItFe13PGurLCIoIFauQiZ2lsvx9htc6g/edit?usp=sharing
Guide na contrextily: https://github.com/darribas/contextily/blob/master/contextily_guide.ipynb 
