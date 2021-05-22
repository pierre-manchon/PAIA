# -*-coding: utf8 -*
"""
PAIA tests

Tox: tests CI
Jenkins: Open source automation server
Devpi: PyPI server and packaging/testing/release tool
"""
from PAIA.processing import get_urban_extent
import pandas as pd
import geopandas as gpd
from shapely import speedups
speedups.disable()

# Really not important tho
# Use the qgis project to get the list of files and the list of legend files
# TODO Use a list of files to unpack rather than multiple line vars
# Appears to be impossible due to qgz project file being a binary type file

path_occsol = r'H:\Cours\M2\Cours\HGADU03 - Mémoire\Projet Impact PN Anophèles\Occupation du sol\Produit OS/' \
              r'ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2015-v2.0.7/' \
              r'ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2015-v2.0.7_AFRICA.tif'
path_urbain = r'H:\Cours\M2\Cours\HGADU03 - Mémoire\Projet Impact PN Anophèles\Population\population_dataset/' \
              r'gab_ppp_2020_UNadj_constrained.tif'
path_pa = r'H:/Cours/M2/Cours/HGADU03 - Mémoire/Projet Impact PN Anophèles/Occupation du sol/Aires protegees/' \
          r'WDPA_Mar2021_Public_AFRICA_Land_GABON.shp'
path_boundaries = r'H:/Cours/M2/Cours/HGADU03 - Mémoire/Projet Impact PN Anophèles/Administratif/' \
                  r'Limites administratives/africa_boundary.shp'
path_country_boundaries = r'H:\Cours\M2\Cours\HGADU03 - Mémoire\Projet Impact PN Anophèles\Administratif/' \
                          r'Limites administratives/african_countries_boundaries.shp'
path_decoupage = r'H:/Cours/M2/Cours/HGADU03 - Mémoire/Projet Impact PN Anophèles/Administratif/decoupe_3857.shp'
path_occsol_decoupe = r'H:/Cours/M2/Cours/HGADU03 - Mémoire/Projet Impact PN Anophèles/Occupation du sol/Produit OS/' \
                      r'ESACCI-LC-L4-LCCS-Map-300m-P1Y-1992_2015-v2.0.7/mask.tif'
path_urbain_gabon = r'H:\Cours\M2\Cours\HGADU03 - Mémoire\Projet Impact PN Anophèles\0/pop_polygonized_taille.shp'

"""
df, sf = read_shapefile_as_dataframe(path_country_boundaries)

In case the following contraption doesn'u work, this allows to get coordinates
for v in sf.__geo_interface__['features']:
    shape = v['geometry']['coordinates']

for x in zip(df.NAME, df.AREA, df.coords):
    if x[0] != '':
        cr = raster_crop(dataset=path_occsol, shapefile=sf.shp.name)
        get_categories(dataset=cr, shapefile_area=x[1], band=0)
        # plot_shape(shapefile=sf, dataframe=df, name=x)
    else:
        pass
"""


pa = gpd.read_file(path_pa)
ug = get_urban_extent(path_urbain_gabon, 360000)

centros = []
for r in zip(ug.fid, ug.DN, ug.Size, ug.geometry):
    if r[2] == 'small':
        centros.append([r[0], str(r[3].centroid)])
    else:
        centros.append([r[0]])
        pass
del r
df = pd.DataFrame(centros, columns=['fid', 'centro'])
del centros
df['centro'] = gpd.GeoSeries.from_wkt(df['centro'])
ug = ug.merge(df, on='fid')
del df

result = []
for u in zip(ug.fid, ug.DN, ug.Size, ug.geometry):
    min_dist = 100000
    name = None
    for p in zip(pa.WDPA_PID, pa.NAME, pa.GIS_AREA, pa.geometry):
        dist = p[1].distance(u[3])
        if dist < min_dist:
            min_dist = dist
            name = p[1]
    result.append([u[0], u[1], u[2], u[3], name, dist])
del dist, min_dist, name, p, u
df = pd.DataFrame(result, columns=['fid', 'DN', 'Size', 'geometry', 'pa_name', 'distance'])
ug.merge(df, on='fid')
del df

# https://automating-gis-processes.github.io/2017/lessons/L3/nearest-neighbour.html
# get_categories(dataset=path_occsol_decoupe, band=0)
# raster_crop(dataset=path_occsol, shapefile=path_decoupage)

"""
https://stackoverflow.com/questions/39995839/gis-calculate-distance-between-point-and-polygon-border
load every layers
Illustrer difference Gabon/Afrique (proportion occsol/pays = Surface catégories/surface pays)
Stats pour Afrique, Zone présence Anophèles, Pays (polygonize dominant vectors)
Lister lesx variables calculables: proportion par buffer
Lien proximité/pop/parcs/anophèles

QGIS
Convertir les pixels urbains de l'occsol en polygone
CODE
Convertir ces polygones en mono parties.
Associer puis séparer les villages gros des villages petits.

Dans le premier cas, mesurer dans un premier temps la distance entre le bord de l'aire urbaine et le parc.
Dans le second cas, utiliser le centroïde pour ensuite mesurer la distance avec la bordure du parc.
Puis, dans un second temps, mesurer au sein de cellules/patchs la fragmentation des tâches urbaines.
"""
