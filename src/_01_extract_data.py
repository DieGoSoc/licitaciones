import polars 
import xml.etree.ElementTree as ET
import os
from tqdm import tqdm

def get_file_info (path = r'C:\Users\diego\Desktop\licitaciones\data\licitacionesPerfilesContratanteCompleto3_20201222_192258.atom'):
    tree = ET.parse(path)
    root = tree.getroot()
    print(root)
    for child in root:
        if child.tag == '{http://www.w3.org/2005/Atom}entry':
            print()
        print(child.tag, child.attrib)

def extract_data (folder = r'C:\Users\diego\Desktop\licitaciones\data'):
    files = os.listdir(folder)
    progress = tqdm(files)
    for f in progress:
        fpath = os.path.join(folder,f)
        get_file_info(fpath)
    print('hi')

