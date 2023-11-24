import polars as pl
from pandas import pandas as pd

from _00_download_data import download_data
from _01_unzip_data import unzip_data
from _02_extract_data import extract_data, get_file_info

download_data()
unzip_data()
extract_data()
