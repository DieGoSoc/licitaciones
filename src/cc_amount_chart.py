# CHART 2: TOP 10 CITIES WITH HIGHER AMOUNT
import pandas as pd
import plotly_express as px

df = pd.read_csv(r'C:\Users\diego\Desktop\licitaciones\licitaciones.csv')

subentity_rename = {
    'COMUNIDAD DE MADRID': 'Madrid',
    'Comunidad de Madrid': 'Madrid',
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
    'Región de Murcia': 'Murcia',
}

cc_name = {
    'Teruel': 'Aragon',
    'Melilla': 'Melilla',
    'Girona': 'Cataluña',
    'Ceuta': 'Castilla la Mancha',
    'Ciudad Real': 'Castilla la Mancha',
    'Navarra': 'Navarra',
    'Huesca': 'Aragon',
    'Vizcaya': 'País Vasco',
    'Valladolid': 'Castilla y León',
    'Lleida': 'Cataluña',
    'Las Palmas': 'Canarias',
    'Almería': 'Andalucia',
    'Andalucía': 'Andalucia',
    'Salamanca': 'Castilla y León',
    'Santa Cruz de Tenerife': 'Canarias',
    'Segovia': 'Castilla y Leon',
    'Zaragoza': 'Aragon',
    'País Vasco': 'País Vasco',
    'Extremadura': 'Extremadura',
    'Pontevedra': 'Galicia',
    'Guadalajara': 'Castilla la Mancha',
    'Barcelona': 'Cataluña',
    'Cádiz': 'Andalucía',
    'Córdoba': 'Andalucía',
    'A Coruña': 'Galicia',
    'Alacant/Alicante': 'Comunidad Valenciana',
    'Sevilla': 'Andalucía',
    'Gipúzcoa': 'País Vasco',
    'Bizkaia/Vizcaya': 'País Vasco',
    'Burgos': 'Castilla y León',
    'Murcia': 'Región de Murcia',
    'Granada': 'Andalucía',
}


df['subentity'] = df['country subentity'].replace(subentity_rename)
df['cc'] = df['subentity'].replace(cc_name)

df = df[df['cc'] != 'ESPAÑA']
df = df[df['cc'] != 'NORESTE']
df = df[df['cc'] != 'Not country subentity available']
df = df[df['cc'] != 'FRANCE']

amount_cc_chart = df.groupby('cc')['total amount'].sum().reset_index().sort_values(by='total amount', ascending=True)
fig = px.bar(
    amount_cc_chart,
    x='cc',
    y='total amount',
    text='total amount',
    title='Total amount by C.C.',
    color='total amount',
)
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.show()
