import os
import xml.etree.ElementTree as ET

import polars as pl
from tqdm import tqdm


def get_file_info(
    path=r'C:\Users\diego\Desktop\licitaciones\data\licitacionesPerfilesContratanteCompleto3_20201222_192258.atom'
):
    namespaces = {
        'cbc-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2',
        'cac-place-ext': 'urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2',
        'cbc': 'urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2',
        'cac': 'urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2',
        'ns1': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
    }
    tree = ET.parse(path)
    root = tree.getroot()
    ids = []
    postcodes = []
    titles = []
    entries = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        postcode = entry.find('.//cbc:PostalZone', namespaces).text
        title = entry.find('{http://www.w3.org/2005/Atom}title', namespaces).text
        id = entry.find('{http://www.w3.org/2005/Atom}id', namespaces).text
        # id number extraction
        id = id.replace('https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/', '')
        ids.append(id)
        titles.append(title)
        postcodes.append(postcode)
    entries['id'] = ids
    entries['postcode'] = postcodes
    entries['title'] = titles
    df = pl.DataFrame(entries)
    return df


def extract_data(folder=r'C:\Users\diego\Desktop\licitaciones\data'):
    files = os.listdir(folder)
    progress = tqdm(files[:10])  # just first 10 only to debug
    dfs = []
    for f in progress:
        fpath = os.path.join(folder, f)
        entry = get_file_info(fpath)
        dfs.append(entry)
    dataframe = pl.concat(dfs)
    return dataframe
