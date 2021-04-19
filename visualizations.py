
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as go

def g_dd_du(df_data, df_estadisticos):
    """
    :param df_data: Dataframe con los datos diarios del portafolio
    :param df_estadisticos: Dataframe de los estadisticos de la funcion f_estadisticos_mad
    :return: Gráfica de linea con evolucion del capital acumulado, Draw Down maximo y Draw Up
    Debugging
    --------
    df_data = data5
    df_estadisticos = data6
    """

    # Encontrar fechas de inicio y fin del Draw Down y Draw Up usando la funcion de estadisticos MAD
    start_dd = pd.to_datetime(df_estadisticos['Valor'][3].split()[0].replace('"', ''))
    end_dd = pd.to_datetime(df_estadisticos['Valor'][3].split()[2].replace('"', ''))
    start_du = pd.to_datetime(df_estadisticos['Valor'][4].split()[0].replace('"', ''))
    end_du = pd.to_datetime(df_estadisticos['Valor'][4].split()[2].replace('"', ''))

    # Encontrar los valores de Y para la linea de DU y DD
    df_data.index = df_data.timestamp

    # Crear gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_data.timestamp, y=df_data.profit_acm_d + 5000, name="Capital Acumulado",
                             marker_color='Black'))
    fig.add_shape(type='line', x0=start_dd, x1=end_dd,
                  y0=df_data['profit_acm_d'][start_dd] + 5000, y1=df_data['profit_acm_d'][end_dd] + 5000,
                  line=dict(color="Red", width=4, dash="dashdot"),
                  name='Maximum Draw Down')
    fig.add_shape(type='line', x0=start_du, x1=end_du,
                  y0=df_data['profit_acm_d'][start_du] + 5000, y1=df_data['profit_acm_d'][end_du] + 5000,
                  line=dict(color="Green", width=4, dash="dashdot"),
                  name='Maximum Draw Up')
    fig.update_layout(title_text='Max DrawDown and DrawUp',
                      xaxis_title="Fecha", yaxis_title="$USD",
                      font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
                      showlegend=True)

    fig.show()

    return fig




def g_pastel(p_dict, title='Ranking of tickers in transactions'):

    def p2f(x):
        
        return float(x.strip('%')) / 100

    def pull_values(data):
        """
        :param data: arreglo de numpy de valores
        :return: arreglo de numpy de 0 y 0.2 en la posicion del valor mas grande de la cadena
        Debugging
        --------
        data = np.array([0, 1, 8, 3, 5, 0, 3])
        """
        largest_value = np.zeros_like(data)
        largest = data.argmax()
        largest_value[largest] = 0.2
        return largest_value

    symbols = np.array(p_dict['df_2_ranking']['Symbol'])
    values = np.array([p2f(x) for x in p_dict['df_2_ranking']['Rank']])
    pull = pull_values(values)
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=symbols, values=values, pull=pull))
    fig.layout.update(title_text=title, font=dict(family="Courier New, monospace", size=18, color="#8ab6d6"),
                      showlegend=True)
    fig.show()

    return fig
