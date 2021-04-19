
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf

mt5.initialize(login=41671422, server='MetaQuotes-Demo', password='LLWs@4MnzdWM4vf')


# -----------------------------------------------------------------------------------------------------------------------------------------------


def f_pip_size(Ticker):
    pip_size = mt5.symbol_info(Ticker)._asdict().get('trade_tick_size')*10
    n = 1/pip_size
    return int(n)


# -----------------------------------------------------------------------------------------------------------------------------------------------


def f_columnas_tiempos(param_data):     
    param_data['open_time'] = pd.to_datetime(param_data['Time'])
    param_data['close_time'] = pd.to_datetime(param_data['Time.1'])
    param_data['time'] = [i.total_seconds() for i in (param_data['close_time']-param_data['open_time'])]
    return param_data    


# -----------------------------------------------------------------------------------------------------------------------------------------------


def f_columnas_pips(DF):
    pipsize = DF['Symbol'].apply(f_pip_size)
    pips = []
    for i in range(len(DF)):
        if DF['Type'][i] == 'buy':
            pips.append(pipsize[i]*(DF['Price.1'][i]-DF['Price'][i]))
        else: 
            pips.append(pipsize[i]*(DF['Price'][i]-DF['Price.1'][i]))
        
    DF['pips'] = pips
    DF['pips_acm'] = DF['pips'].cumsum()
    DF['profit_acm'] = DF['Profit'].cumsum()
    return DF


# -----------------------------------------------------------------------------------------------------------------------------------------------


def f_estadisticas_ba(param_data):
    Ops_totales = len(param_data) 
    Ganadoras = len(param_data[param_data['Profit']>0])
    Ganadoras_c = len(param_data[(param_data['Profit']>0) & (param_data['Type']=='buy')])
    Ganadoras_v = len(param_data[(param_data['Profit']>0) & (param_data['Type']=='sell')])
    Perdedoras = len(param_data[param_data['Profit']<0])
    Perdedoras_c = len(param_data[(param_data['Profit']<0) & (param_data['Type']=='buy')])
    Perdedoras_v = len(param_data[(param_data['Profit']<0) & (param_data['Type']=='sell')])
    if len(param_data)%2 == 0:
        Mediana_Profit = np.array((param_data.sort_values(by='Profit')['Profit'][int(len(param_data)/2)-1:int((len(param_data)/2)+1)])).mean()
        Mediana_Pips = np.array((param_data.sort_values(by='pips')['pips'][int(len(param_data)/2)-1:int((len(param_data)/2)+1)])).mean()
    
    else:
        Mediana_Profit = param_data.sort_values(by='Profit')['Profit'][int(len(param_data)/2)]
        Mediana_Pips = param_data.sort_values(by='pips')['pips'][int(len(param_data)/2)]
          
    r_efectividad = Ganadoras/Ops_totales
    r_proporcion = Ganadoras/Perdedoras
    r_efectividad_c = Ganadoras_c/Ops_totales
    r_efectividad_v = Ganadoras_v/Ops_totales
    
    df_1_tabla = pd.DataFrame({'medida':['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c',
                        'Perdedoras_v','Mediana(Profit)','Mediana(Pips)','r_efectividad','r_proporcion','r_efectividad_c','r_efectividad_v'],
                               'valor':[Ops_totales, Ganadoras, Ganadoras_c, Ganadoras_v, Perdedoras,Perdedoras_c, Perdedoras_v, 
                                        Mediana_Profit, Mediana_Pips,r_efectividad,r_proporcion,r_efectividad_c,r_efectividad_v],
                               'descripcion':['Operaciones totales','Operaciones ganadoras','Operaciones ganadoras de compra',
                                              'Operaciones ganadoras de venta','Operaciones perdedoras','Operaciones perdedoras de compra',
                                              'Operaciones perdedoras de venta','Mediana de profit de operaciones','Mediana de pips de operaciones',
                                              'Ganadoras Totales/Operaciones Totales','Ganadoras Totales/Perdedoras Totales',
                                              'Ganadoras Compra/Operaciones Totales','Ganadoras Venta/Operaciones Totales']})

    rank = [str(np.round(len(param_data[(param_data['Symbol']==i) & (param_data['Profit']>0)])/len(param_data[(param_data['Symbol']==i)])*100,2)) + '%' for i in param_data['Symbol'].unique()]
    df_2_ranking = pd.DataFrame({'Symbol':param_data['Symbol'].unique(),
                                 'Rank':rank})
    
    return {'df_1_tabla':df_1_tabla,'df_2_ranking':df_2_ranking}



# -----------------------------------------------------------------------------------------------------------------------------------------------



def f_evolucion_capital(data3, init_invest=100000):
    
    daily = data3[['close_time', 'Profit']]
    daily.rename(columns={'close_time': 'timestamp', 'Profit': 'profit_d'}, inplace=True)
    daily.index = daily.timestamp
    daily = daily.resample("d").sum().reset_index()
    daily.index = daily.timestamp
    daily.index = pd.to_datetime(daily.index ).strftime('%Y-%m-%d')
    
    if len(daily['timestamp']) > 11:
        daily1 = daily.drop(index =['2021-02-20'])
        daily1 = daily1.drop(index =['2021-02-21'])
        daily1 = daily1.drop(index =['2021-02-27'])
        daily1 = daily1.drop(index =['2021-02-28'])
    
    elif len(daily['timestamp']) < 11:
        daily1 = daily.drop(index =['2021-02-27'])
        daily1 = daily1.drop(index =['2021-02-28'])
        
    daily2 = daily1.reset_index(drop=True)
    
    # calcular la ganancia o perdida acumulada de la cuenta
    daily2['profit_acm_d'] = daily2['profit_d'].cumsum() + init_invest

    return daily2


# -----------------------------------------------------------------------------------------------------------------------------------------------


def f_estadisticas_mad(daily):
    rf = 0.05
    
    rendimientos_logV2 = np.log(daily['profit_acm_d'] / daily['profit_acm_d'].shift()).dropna()
    rendimientos_logV3 = rendimientos_logV2.reset_index()
    rendimientos_logV4 = rendimientos_logV3.drop(columns='index')
    rendimientos_logV5 = rendimientos_logV4['profit_acm_d'].values.tolist()
    
    
    ratio_d = rendimientos_logV2.mean() * 300
    des = rendimientos_logV2.std()
    sharpe = (ratio_d - rf) / des
        
        
    #precios del sp500
    p_sp500 = yf.download('^GSPC',start='2021-02-19', end='2021-03-06',interval='1d')
    p_sp500.drop(['Open','High','Low','Volume','Adj Close'], axis=1, inplace=True)
    #Sharpe actualizado
    ren_sp500_log = [np.log(p_sp500['Close'][i]/p_sp500['Close'][i-1]) for i in range(1,len(p_sp500['Close']))]
    
    resta = [rendimientos_logV5[i] - ren_sp500_log[i] for i in range (len(rendimientos_logV2))]
    
    
    rendimientos_logv6 = pd.DataFrame(rendimientos_logV5)
    ren_sp500_logv2 = pd.DataFrame(ren_sp500_log)
    restav2 = pd.DataFrame(resta)
    
    sharpe_actualizado = round((rendimientos_logv6.mean()-ren_sp500_logv2.mean())/restav2.std(),2)    



    # Draw Down
    cap_max = daily['profit_acm_d'].max()
    indi = daily[daily.profit_acm_d == cap_max].index
    pos = indi[0]
    if pos < (len(daily['profit_acm_d']) - 1):
        posmax = daily['timestamp'][pos]
        cap_min = daily['profit_acm_d'][pos:].min()
        pmin = daily['timestamp'][daily[daily.profit_acm_d == cap_min].index[0]]
        drawdown_capi = (cap_min - cap_max) / cap_max
    
    else:
       capi_evo = daily.shift().dropna().reset_index()
       cap_maxn = capi_evo['profit_acm_d'].max()
       indin = capi_evo[capi_evo.profit_acm_d == cap_maxn].index
       posn = indin[0]
       posmax = capi_evo['timestamp'][posn]
       cap_minn = capi_evo['profit_acm_d'][posn:].min()
       pmin = capi_evo['timestamp'][capi_evo[capi_evo.profit_acm_d == cap_minn].index[0]]
       drawdown_capi = (cap_minn - cap_maxn) / cap_maxn
    
    # Draw Up
    
    cap_min = daily['profit_acm_d'].min()
    indi = daily[daily.profit_acm_d == cap_min].index
    pos = indi[0]
    if pos < (len(daily['profit_acm_d']) - 1):
        posmin = daily['timestamp'][pos]
        cap_max = daily['profit_acm_d'][pos:].max()
        pmax = daily['timestamp'][daily[daily.profit_acm_d == cap_max].index[0]]
        drawup_capi = (cap_max - cap_min)
    
    else:
       capi_evo = daily.shift().dropna().reset_index()
       cap_minn = capi_evo['profit_acm_d'].min()
       indin = capi_evo[capi_evo.profit_acm_d == cap_minn].index
       posn = indin[0]
       posmin = capi_evo['timestamp'][posn]
       cap_maxn = capi_evo['profit_acm_d'][posn:].min()
       pmax = capi_evo['timestamp'][capi_evo[capi_evo.profit_acm_d == cap_maxn].index[0]]
       drawup_capi = (cap_maxn - cap_minn)
    
    
    # Dataframe MAD
    MAD = pd.DataFrame(columns=['Metrica', 'Valor', 'Descripción'])
    MAD['Metrica'] = ['sharpe', 'sharpe_actualizado','drawdown_capi_Fech_Ini','drawdown_capi_Fech_Fin','drawdown_capi', 'drawup_capi_Fech_Ini','drawup_capi_Fech_Fin','drawup_capi']
    MAD['Valor'] = [sharpe,sharpe_actualizado, posmax, pmin, drawdown_capi, posmin, pmax, drawup_capi]
    MAD['Descripción'] = ['Sharpe Ratio','Sharpe Ratio Fórmula Ajustada', 'Fecha inicial del DrawDown de Capital','Fecha final del DrawDown de Capital', 'Máxima pérdida flotante registrada','Fecha inicial del DrawUp de Capital', 'Fecha final del DrawUp de Capital','Máxima ganancia flotante registrada']

    return MAD





def f_be_de(param_data):
 
    param_data = param_data.loc[:,('Symbol','Type','Volume','Price','Price.1',
                   'Profit','open_time','close_time','pips','profit_acm')]
    
    #Se seleccionan las operaciones anclas(aquellas con profit positivo)
    df_anclas = param_data[param_data['Profit']>0].reset_index(drop=True) #reiniciar contador de índices
    
    #Checar si hubo operaciones abiertas al cerrar un ancla
    ocurrencias = pd.concat([param_data.iloc[j,:] for i in range(len(df_anclas)) for j in range(len(param_data)) if 
               param_data['close_time'][j]>df_anclas['close_time'][i] and 
               param_data['open_time'][j]<df_anclas['close_time'][i]],1).transpose()
    #Incluir la fecha de cierre de la operación ancla
    times_ancla = [df_anclas.loc[i,('close_time')] for i in range(len(df_anclas)) for j in range(len(param_data)) if 
               param_data['close_time'][j]>df_anclas['close_time'][i] and 
               param_data['open_time'][j]<df_anclas['close_time'][i]]
    #Se añade la columna con los tiempos de cierre del ancla
    ocurrencias['close_ancla'] = times_ancla

    precio_flotante = []
    for i in range(len(ocurrencias)):
        from_date = datetime(ocurrencias['close_ancla'].iloc[i].year,
                             ocurrencias['close_ancla'].iloc[i].month,
                             ocurrencias['close_ancla'].iloc[i].day)

        to_date = from_date + timedelta(1)
        sym = ocurrencias['Symbol'].iloc[i]

        ticks =  mt5.copy_ticks_range(sym, from_date, to_date, mt5.COPY_TICKS_ALL)
        df_t = pd.DataFrame(ticks)
        df_t['time']=pd.to_datetime(df_t['time'], unit='s')
        if ocurrencias['Type'].iloc[i] == 'buy':
            tipo = 'bid'
        else:
            tipo = 'ask'
        precio_flotante.append(df_t[f'{tipo}'][df_t['time']>=ocurrencias['close_ancla'].iloc[0]].iloc[0])
    ocurrencias['precio_flotante'] = precio_flotante
    ocurrencias['pip_value'] = abs(ocurrencias['Profit']/ocurrencias['Price']-ocurrencias['Price.1'])
    #profit flotante, lo que ganas o pierdes en ese momento que cerró el ancla
    p_flotante = [ocurrencias['pip_value'].iloc[i]*(ocurrencias['precio_flotante'].iloc[i]-ocurrencias['Price'].iloc[i]) 
                  if ocurrencias['Type'].iloc[i]=='buy' else 
                  ocurrencias['pip_value'].iloc[i]*(ocurrencias['Price'].iloc[i]-ocurrencias['precio_flotante'].iloc[i]) 
                  for i in range(len(ocurrencias))]

    ocurrencias['profit_flotante'] = p_flotante
    ocurrencias = ocurrencias[ocurrencias['profit_flotante']<0].reset_index(drop=True)
    
    #Diccionario
    
    diccionario = {'ocurrencias': {'cantidad':len(ocurrencias)}}

    for i in range(len(ocurrencias)):
        ganadora = df_anclas[ocurrencias['close_ancla'].iloc[i]==df_anclas['close_time']]
        diccionario['ocurrencias'][f'ocurrencia_{i+1}'] = {'timestamp':ocurrencias['close_ancla'].iloc[i],
                                                          'operaciones':{
                                                              'ganadoras':{
                                                                  'instrumento':ganadora['Symbol'].iloc[0],
                                                                  'volumen':ganadora['Volume'].iloc[0],
                                                                  'sentido':ganadora['Type'].iloc[0],
                                                                  'profit_ganadora':ganadora['Profit'].iloc[0]
                                                              },
                                                              'perdedoras':{
                                                                  'instrumento':ocurrencias['Symbol'].iloc[i],
                                                                  'volumen':ocurrencias['Volume'].iloc[i],
                                                                  'sentido':ocurrencias['Type'].iloc[i],
                                                                  'profit_perdedora':ocurrencias['profit_flotante'].iloc[i]
                                                              }
                                                          },'ratio_cp_profit_acm':abs(ocurrencias['profit_flotante'].iloc[i]/ganadora['profit_acm'].iloc[0]),'ratio_cg_profit_acm':abs(ganadora['Profit'].iloc[0]/ganadora['profit_acm'].iloc[0]),'ratio_cp_cg':abs(ocurrencias['profit_flotante'].iloc[i]/ganadora['Profit'].iloc[0])
                                                         }

    status_quo = 0
    aversion_perdida = 0
    for i in range(len(ocurrencias)):
        if diccionario['ocurrencias'][f'ocurrencia_{i+1}']['ratio_cp_profit_acm'] < diccionario['ocurrencias'][f'ocurrencia_{i+1}']['ratio_cg_profit_acm']:
            status_quo += 1
        if diccionario['ocurrencias'][f'ocurrencia_{i+1}']['ratio_cp_cg']>2:
            aversion_perdida += 1

    sensibilidad_decreciente = 0
    if df_anclas['profit_acm'].iloc[-1] > df_anclas['profit_acm'].iloc[0]:
        sensibilidad_decreciente += 1
    if df_anclas['Profit'].iloc[-1] > df_anclas['Profit'].iloc[0] and ocurrencias['profit_flotante'].iloc[-1] > ocurrencias['profit_flotante'].iloc[0]:
        sensibilidad_decreciente += 1
    if diccionario['ocurrencias'][f'ocurrencia_{len(ocurrencias)}']['ratio_cp_cg'] > 2:
        sensibilidad_decreciente += 1

    if sensibilidad_decreciente >= 2:
        final = 'Si'
    else:
        final = 'No'

    diccionario['resultados'] = {'dataframe':pd.DataFrame({
        'ocurrencias':len(ocurrencias),
        'status_quo':str(round(100*status_quo/len(ocurrencias),2))+'%',
        'aversion_perdida':str(round(100*aversion_perdida/len(ocurrencias),2))+'%',
        'sensibilidad_decreciente':[final]})}
    
    diccionario2 = pd.DataFrame({'ocurrencias':len(ocurrencias),
                    'status_quo':str(round(100*status_quo/len(ocurrencias),2))+'%',
                    'aversion_perdida':str(round(100*aversion_perdida/len(ocurrencias),2))+'%',
                   'sensibilidad_decreciente':[final]},columns=['ocurrencias', 'status_quo','aversion_perdida','sensibilidad_decreciente'])
    
    return diccionario2
