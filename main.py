
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

from functions import f_columnas_tiempos,f_columnas_pips,f_estadisticas_ba
from functions import f_evolucion_capital , f_estadisticas_mad, f_be_de
from data import f_leer_archivo
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------------------- Parte 1

#Funcion desde regresa un dataframe con toda la informacion del archivo.
data = f_leer_archivo('MyST_LAB2_J.xlsx','Historico MT4')

#Funcion donde el mismo Dataframe convertimos las columnas a tipo Datetime
data2 = f_columnas_tiempos(data)

#Funcion para obtener el número multiplicador para expresar la diferencia de precios en pips.
data3 = f_columnas_pips(data2)
param_data1 = f_columnas_pips(data2)
param_data = param_data1.rename(str.lower, axis='columns')
param_data = param_data.rename(columns={"profit_acm": "capital_acum" , 
                                        "open_time": "opentime" , 
                                        "close_time": "closetime"})

#Funcion donde obtenemos un diccionario con dos dataframes donde nos dice las estadisticas basicas y raking.
data4 = f_estadisticas_ba(data3)



# ---------------------------------------------------------------------------------------- Parte 2

#funcion cuya salida contiene un dataframe con fechas dia a dia que se hizo taiding (Quitando fines de semana)
data5 = f_evolucion_capital(data3)

#Función que regrese un DataFrame con los resultados de cada MAD expresadas en términos diarios   
data6 = f_estadisticas_mad(data5)

# ---------------------------------------------------------------------------------------- Parte 3

data7 = f_be_de(data3)


