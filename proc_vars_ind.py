
import pandas as pd
import numpy as np
import json

#########################################


def cambiar_valores_nulos_ciudad_establecimiento(df):
    
    df=df.fillna(value={'ciudad':'otra_ciudad'})
    df=df.fillna(value={'establecimiento':'otro_establecimiento'})
    
    return df

#########################################

def procesa_var_hora(df):
    
    df['hora_solar']=df['hora'].apply(lambda x: np.sin( x*(2*np.pi/24) - np.pi/2 ))
    df['hora_comp']=df['hora'].apply(lambda x: np.sin( x*(2*np.pi/24) ))	

    df['cashback_pct']=df['cashback']/df['monto']
    df['dcto_pct']=df['dcto']/df['monto']	

    df['dispositivo']=df['dispositivo'].str.replace("'",'"')
    df['dispositivo']=df['dispositivo'].apply(lambda x: json.loads(x))	

    aux=pd.json_normalize(df['dispositivo'])
    df=df.join(aux)
    
    return df

#########################################

def procesa_var_fecha(df):

    df['date']=df['fecha'].apply(lambda x: pd.to_datetime(x,format='%Y-%m-%d'))
    df['date_0']=(df['date']-pd.to_datetime('01/01/2000',format='%d/%m/%Y')).dt.days.astype(int)

    df['weekday']=df['date_0'].apply(lambda x: (x-4)%7 )
    df['weekday_0']=df['weekday'].apply(lambda x: np.cos( x*(2*np.pi/7) ) )
    
    return df
