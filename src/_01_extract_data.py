import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
import polars as pl

def get_file_info (path = r'C:\Users\diego\Desktop\licitaciones\data\licitacionesPerfilesContratanteCompleto3_20201222_192258.atom'):
    namespaces = {
        'cbc-place-ext':"urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonBasicComponents-2",
        'cac-place-ext':"urn:dgpe:names:draft:codice-place-ext:schema:xsd:CommonAggregateComponents-2",
        'cbc':"urn:dgpe:names:draft:codice:schema:xsd:CommonBasicComponents-2",
        'cac':"urn:dgpe:names:draft:codice:schema:xsd:CommonAggregateComponents-2",
        'ns1':"urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
    }
    tree = ET.parse(path)
    root = tree.getroot()
    entries = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        postcode = entry.find(".//cbc:PostalZone", namespaces).text
        title = entry.find('{http://www.w3.org/2005/Atom}title', namespaces).text
        id = entry.find('{http://www.w3.org/2005/Atom}id', namespaces).text
        #id number extraction
        entries [id] = {'title' : title, 'postcode' : postcode}
    return entries

def extract_data (folder = r'C:\Users\diego\Desktop\licitaciones\data'):
    files = os.listdir(folder)
    progress = tqdm(files[:10])
    data = []
    df = pd.DataFrame()
    for f in progress:
        fpath = os.path.join(folder,f)
        titles = get_file_info(fpath)
        data.append(titles)
    df['titles'] = data
    return df



