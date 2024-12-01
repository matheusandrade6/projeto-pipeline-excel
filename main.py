import pandas as pd
from src.controller import load_excel, add_data_to_database, trim_column_names, trim_text_columns

file_path = './excel-file/data.xlsx'

sheet_dict = load_excel(file_path)

add_data_to_database(sheet_dict)