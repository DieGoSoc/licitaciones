import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

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
    update_dates = []
    start_dates = []
    end_dates = []
    cities = []
    country_subentities = []
    overall_contract_amounts = []
    total_amounts = []
    tax_ex_amounts = []
    entries = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        postcode = entry.find('.//cbc:PostalZone', namespaces).text
        title = entry.find('{http://www.w3.org/2005/Atom}title', namespaces).text
        id = entry.find('{http://www.w3.org/2005/Atom}id', namespaces).text
        # id number extraction
        id = id.replace('https://contrataciondelestado.es/sindicacion/licitacionesPerfilContratante/', '')
        date = entry.find('{http://www.w3.org/2005/Atom}updated', namespaces).text
        date_re = re.search(r'\d{4}-\d{2}-\d{2}', date)
        date = datetime.strptime(date_re.group(), '%Y-%m-%d').date()
        city = entry.find('.//cbc:CityName', namespaces).text
        start_date = entry.find('.//cbc:StartDate', namespaces)

        if start_date is not None and start_date.text is not None:
            start_date = start_date.text
        else:
            start_date = 'No date available'

        end_date = entry.find('.//cbc:EndDate', namespaces)

        if end_date is not None and end_date.text is not None:
            end_date = end_date.text
        else:
            end_date = 'No date available'

        overall_contract_amount = entry.find('.//cbc:EstimatedOverallContractAmount', namespaces)

        if overall_contract_amount is not None and overall_contract_amount.text is not None:
            overall_contract_amount = overall_contract_amount.text
        else:
            overall_contract_amount = 'No amount available'

        total_amount = entry.find('.//cbc:TotalAmount', namespaces)

        if total_amount is not None and total_amount.text is not None:
            total_amount = total_amount.text
        else:
            total_amount = 'No amount available'

        tax_ex_amount = entry.find('.//cbc:TaxExclusiveAmount', namespaces)

        if tax_ex_amount is not None and tax_ex_amount.text is not None:
            tax_ex_amount = tax_ex_amount.text
        else:
            tax_ex_amount = 'No amount available'

        country_subentity = entry.find('.//cbc:CountrySubentity', namespaces)

        if country_subentity is not None and country_subentity is not None:
            country_subentity = country_subentity.text
        else:
            country_subentity = 'Not country subentity available'

        ids.append(id)
        titles.append(title)
        postcodes.append(postcode)
        update_dates.append(date)
        cities.append(city)
        start_dates.append(start_date)
        end_dates.append(end_date)
        overall_contract_amounts.append(overall_contract_amount)
        total_amounts.append(total_amount)
        tax_ex_amounts.append(tax_ex_amount)
        country_subentities.append(country_subentity)

    entries['id'] = ids
    entries['postcode'] = postcodes
    entries['title'] = titles
    entries['update date'] = update_dates
    entries['start date'] = start_dates
    entries['end_date'] = end_dates
    entries['country subentity'] = country_subentities
    entries['city'] = cities
    entries['estimate overall contract amount'] = overall_contract_amounts
    entries['total amount'] = total_amounts
    entries['tax excslusive amount'] = tax_ex_amounts
    df = pl.DataFrame(entries)
    return df


def extract_data(folder=r'C:\Users\diego\Desktop\licitaciones\data'):
    files = os.listdir(folder)
    progress = tqdm(files[0:3])  # just first 10 only to debug
    dfs = []
    for f in progress:
        fpath = os.path.join(folder, f)
        entry = get_file_info(fpath)
        dfs.append(entry)
    dataframes = pl.concat(dfs)
    csv_file_path = 'licitaciones.csv'
    dataframes.write_csv(csv_file_path)
    return dataframes
