import geopandas as gpd
import pandas as pd
import plotly.express as px
import polars as pl

df = pl.read_csv('C:/Users/diego/Desktop/licitaciones/licitaciones.csv')

# Creating a coropleth map for spanish country subentities
# We need to modify our data as the row data may be wrong
# In this case we have to modify the subentities names taking the information from city column and country subentity column

subentity_rename = {
    'COMUNIDAD DE MADRID': 'Madrid',
    'Gipuzkoa': 'Gipuzkoa/Gipúzcoa',
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
    'Extremadura': 'Cáceres',
}

city_to_subentity = {
    'Mérida': 'Badajoz',
    'Madrid': 'Madrid',
    'Valencia': 'València/Valencia',
    'Aljaraque': 'Huelva',
    'la laguna': 'Santa Cruz De Tenerife',
    'Burgos': 'Burgos',
    'Alicante': 'Alacant/Alicante',
    'OVIEDO': 'Asturias',
    'Sevilla': 'Sevilla',
    'Gijón': 'Cantabria',
    'Barcelona': 'Barcelona',
    'Pontevedra': 'Pontevedra',
    'Cartagena': 'Murcia',
    'Santa Cruz de Tenerife': 'Santa Cruz De Tenerife',
    'San Cristóbal de La Laguna -Santa Cruz de Tenerife': 'Santa Cruz De Tenerife',
    'Vigo': 'Pontevedra',
    'Santa Lucía de Tirajana (Gran Canaria)': 'Las Palmas',
    'Campo de Criptana ': 'Ciudad Real',
    'Zamora': 'Zamora',
    'Zaragoza': 'Zaragoza',
    'Badajoz': 'Badajoz',
    'Valladolid': 'Valladolid',
    'Teguise (Lanzarote)': 'Las Palmas',
    'Lugo': 'Lugo',
    'Reus': 'Tarragona',
    'Arrecife': 'Las Palmas',
    'A Coruña': 'A Coruña',
    'San Vicente del Raspeig': 'València/Valencia',
    'Villagonzalo de Tormes': 'Salamanca',
    'Mansilla de las Mulas (León)': 'León',
    'Elche': 'Alacant/Alicante',
    'Alberite': 'La Rioja',
    'Majadahonda (Madrid)': 'Madrid',
    'Santurtzi': 'Bizkaia/Vizcaya',
    'Castellón': 'Castelló/Castellón',
    'Siero': 'Asturias',
    'Granollers': 'Barcelona',
    'Las Palmas de Gran Canaria': 'Las Palmas',
    'Langreo': 'Asturias',
    'Rubayo, Cantabria': 'Cantabria',
    'Toledo': 'Toledo',
    'Vinarós': 'Castelló/Castellón',
    'Pasaia': 'Gipuzkoa/Guipúzcoa',
    'Oleiros': 'A Coruña',
    'Albacete': 'Albacete',
    'Palma de Mallorca': 'Illes Balears',
    'El Higuerón-Córdoba': 'Córdoba',
    'El Pardo (Madrid)': 'Madrid',
    'Bilbao': 'Bizkaia/Vizcaya',
    'Cartagena  (Murcia)': 'Murcia',
    'Pozuelo de Alarcón': 'Madrid',
    'Torrelavega': 'Cantabria',
    'Cubillos del Sil (León)': 'León',
    'Torrejón de Ardoz, Madrid': 'Madrid',
    'Logroño': 'La Rioja',
    'Lardero, La Rioja': 'La Rioja',
    'San Fernando': 'Cádiz',
    'Molina del Segura (Murcia)': 'Murcia',
    'Ferrol (Coruña)': 'A Coruña',
    'Guadalajara': 'Guadalajara',
    'Oviedo': 'Asturias',
    'Gijón ': 'Cantabria',
    'Zamudio. (Bizkaia)': 'Bizkaia/Vizcaya',
    'Muriedas - Camargo': 'Cantabria',
    'Culleredo': 'A Coruña',
    'Murcia': 'Murcia',
    'Almería': 'Almería',
    'León': 'León',
    'Algete': 'Madrid',
    'San Sebastián de la Gomera': 'Santa Cruz De Tenerife',
    'Tarragona': 'Tarragona',
    'MALAGA': 'Málaga',
    'Ampuero': 'Cantabria',
    'Aljaraque (Huelva)': 'Huelva',
    'El Escorial (Madrid)': 'Madrid',
    'Torrejón de Ardoz': 'Madrid',
    'Cuenca': 'Cuenca',
    'Girona': 'Girona',
    'ÁVILA': 'Ávila',
    'Melilla': 'Melilla',
    'Teruel': 'Teruel',
    'Rota (Cádiz)': 'Cádiz',
    'Huelva': 'Huelva',
    'San Vicente Raspeig (Alicante)': 'Alacant/Alicante',
    'Córdoba': 'Córdoba',
    'Posada de Llanera': 'Asturias',
    'Plasencia': 'Cáceres',
    'Cartagena': 'Murcia',
    'Medina del Campo ': 'Valladolid',
    'Calp (Alicante)': 'Alacant/Alicante',
    'Madrid ': 'Madrid',
    'Los Barrios': 'Cádiz',
    'Puerto del Rosario': 'Las Palmas',
    'la laguna': 'Santa Cruz De Tenerife',
    'Gijón (Asturias)': 'Asturias',
    'MADRID': 'Madrid',
    'Soria': 'Soria',
    'Sant Cugat del Vallès': 'Barcelona',
    'Santander': 'Cantabria',
    'Medina del Campo': 'Valladolid',
    'Navarrete (La Rioja)': 'La Rioja',
    'San Lorenzo de El Escorial': 'Madri',
    'Santa Eulária des Riu (Balears)': 'Illes Balears',
    'Mieres': 'Asturias',
    'Bergondo': 'A Coruña',
    'CASTELLON': 'Castelló/Castellón',
    'Jaén': 'Jaén',
    'Pamplona': 'Navarra',
    'Cádiz': 'Cádiz',
    'Cabañaquinta': 'Asturias',
    'VALENCIA': 'València/Valencia',
    'Salamanca': 'Salamanca',
    'Barakaldo': 'Bizkaia/Vizcaya',
    'Mazarrón (Murcia)': 'Murcia',
    'Cangas de Onís, Principado de Asturias': 'Asturias',
    'Cuéllar': 'Segovia',
    'San Martín de la Vega (Madrid)': 'Madrid',
    'Mislata': 'València/Valencia',
    'Huesca': 'Huesca',
    'Pájara (Fuerteventura)': 'Las Palmas',
    'Getafe': 'Madrid',
    'VIGO': 'Pontevedra',
    'Aranda de Duero (Burgos)': 'Burgos',
    'Jaca (Huesca)': 'Huesca',
    'Mislata (Valencia)': 'València/Valencia',
    'Cubas de la Sagra (Madrid)': 'Madrid',
    'Ourense': 'Ourense',
    'San Agustín del Guadalix': 'Madrid',
    'Vilagarcia de Arousa': 'Pontevedra',
    'Talavera de la Reina (Toledo)': 'Toledo',
    'Pozoblanco (Córdoba)': 'Córdoba',
    'HUESCA': 'Huesca',
    'Buniel (Burgos)': 'Burgos',
    'Palma Mallorca': 'Illes Balears',
    'Las Palmas': 'Las Palmas',
    'Amorebieta-Etxano': 'Bizkaia/Vizcaya',
    'Ceuta': 'Ceuta',
    'Zamudio (Vizcaya)': 'Bizkaia/Vizcaya',
    'Armilla ': 'Granada',
    'LUGO': 'Lugo',
    'Villabona Llanera': 'Asturias',
    'Colindres (Cantabria)': 'Cantabria',
    'Los Realejos': 'Santa Cruz De Tenerife',
    'Estremera (Madrid)': 'Madrid',
    'Granada': 'Granada',
    'Llanes': 'Asturias',
    'Vitoria': 'Araba/Álava',
    'CADIZ': 'Cádiz',
    'Cartagena (Murcia)': 'Murcia',
}

# In this case given the size of our data we can use pandas to make it easier:
df1 = df.to_pandas()

# I created a coropleth map indicating the amount of licitations by subentitie:

df1['subentity'] = df1['country subentity'].replace(subentity_rename)
df1['subentity'] = df1['city'].replace(city_to_subentity)
df1 = df1.groupby('subentity').size().reset_index(name='count')

# I dropped some values that are wrong:

df1 = df1[
    ~df1['subentity'].isin(
        [
            'ESPAÑA',
            'CANARIAS',
            'NORESTE',
            'No country subentity available',
            'CENTRO (ES)',
            'ES',
            'Castilla y León',
            'Castilla-La Mancha',
            'País Vasco',
        ]
    )
]

# I merge the geometry information in a JSON file:

gdf = gpd.read_file(
    'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson',
    crs='epsg:4326',
)

df_map = gdf.merge(df1, left_on='name', right_on='subentity', how='left')

# I rename NaN in subentity and count columns:

df_map.loc[df_map['name'] == 'Lleida', 'subentity'] = 'Lleida'
df_map.loc[df_map['name'] == 'Palencia', 'subentity'] = 'Palencia'
df_map['count'] = df_map['count'].fillna(0).astype(int)

# I create the coropleth mal with plotly:

fig = px.choropleth_mapbox(
    df_map,
    geojson=df_map['geometry'].__geo_interface__,
    locations=df_map.index,
    color='count',
    hover_name='subentity',
    range_color=(0, 25),
    color_continuous_scale='oranges',
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
