
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


import pandas as pd

def f_leer_archivo(param_archivo,param_hoja):
    data = pd.read_excel('C:/Users/Andres/Desktop/Traiding/Laboratorio_3/Archivos/' + param_archivo , sheet_name=param_hoja)
    return data
