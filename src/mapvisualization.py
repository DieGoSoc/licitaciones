import geopandas as gpd
import pandas as pd
import plotly.express as px
import polars as pl

from _01_extract_data import extract_data, get_file_info

df = extract_data('C:/Users/diego/Desktop/licitaciones/data')

# Creating a coropleth map for spanish country subentities
df1 = df.group_by('country subentity', maintain_order=True).count()
df1 = df1.filter(pl.col('country subentity') != 'ESPAÑA')
df1 = df1.filter(pl.col('country subentity') != 'CANARIAS')
df1 = df1.filter(pl.col('country subentity') != 'NORESTE')
df1 = df1.filter(pl.col('country subentity') != 'No country subentity available')
df1 = df1.filter(pl.col('country subentity') != 'CENTRO (ES)')
df1 = df1.filter(pl.col('country subentity') != 'ES')
df1 = df1.filter(pl.col('country subentity') != 'Castilla y León')
df1 = df1.filter(pl.col('country subentity') != 'Castilla-La Mancha')
df1 = df1.filter(pl.col('country subentity') != 'País Vasco')

subentity_rename = {
    'COMUNIDAD DE MADRID': 'Madrid',
    'Gipuzkoa': 'Gipúzcoa',
    'Tenerife': 'Santa Cruz De Tenerife',
    'La Gomera': 'Santa Cruz De Tenerife',
    'El Hierro': 'Santa Cruz De Tenerife',
    'La Palma': 'Santa Cruz De Tenerife',
    'Alicante (Alacant)': 'Alacant/Alicante',
    'Alicante / Alacant': 'Alacant/Alicante',
    'Valencia/València': 'València/Valencia',
    'Gran Canaria': 'Las Palmas',
    'Fuerteventura': 'Las Palmas',
    'Bizkaia': 'Bizkaia/Vizcaya',
    'Principado de Asturias': 'Asturias',
}
df1 = df1.to_pandas()
df1['subentity'] = df1['country subentity'].replace(subentity_rename)

gdf = gpd.read_file(
    'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson',
    crs='epsg:4326',
)

df_map = gdf.merge(df1, left_on='name', right_on='subentity', how='left')

fig = px.choropleth_mapbox(
    df_map,
    geojson=df_map['geometry'].__geo_interface__,
    locations=df_map.index,
    color='count',
    hover_name='name',
    range_color=(0, 25),
).update_layout(
    mapbox={
        'style': 'carto-positron',
        'center': {
            'lon': sum(gdf.total_bounds[[0, 2]]) / 2,
            'lat': sum(gdf.total_bounds[[1, 3]]) / 2,
        },
        'zoom': 4,
    },
    margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
)

fig.update_layout(title_text='Mapa de Coropletas en España')
fig.show()
