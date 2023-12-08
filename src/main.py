import pandas as pd
import polars as pl
from _00_download_data import download_data
from _01_unzip_data import unzip_data
from _02_extract_data import extract_data

# parameters for download_data: first year(from), (to) last year to download, folder where save files:
# COMPLETE without (#):
first_year = 2013
last_year = 2014
folder = 'zip_data'
download_data(first_year, last_year, folder)

# parameters for unzip_data: folder where the zip files are, folder where save the uzip files:
# COMPLETE without (#):
data_folder = 'unzip_data'
unzip_data(folder, data_folder)


# parameters for extract_data: folder where the files are:
extract_data(data_folder)
