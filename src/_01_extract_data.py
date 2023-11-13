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
    entries = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        postcode = entry.find('.//cbc:PostalZone', namespaces).text
        title = entry.find('{http://www.w3.org/2005/Atom}title', namespaces).text
        id = entry.find('{http://www.w3.org/2005/Atom}id', namespaces).text
        # id number extraction
        id = id.replace('https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/', '')
        if id in entries:
            continue  # there are some idetical values
        entries[id] = {'title': title, 'postcode': postcode}
    return entries


def extract_data(folder=r'C:\Users\diego\Desktop\licitaciones\data'):
    files = os.listdir(folder)
    progress = tqdm(files[:10])  # just first 10 only to debug
    data = {}
    for f in progress:
        fpath = os.path.join(folder, f)
        entries = get_file_info(fpath)
        data = {**data, **entries}
    new_list = []
    for k, v in data.items():
        v['id'] = k
        new_list.append(v)
    df = pl.DataFrame(new_list, orient='row')
    return df
