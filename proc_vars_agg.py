
import pandas as pd
import numpy as np

################################################################################  

def datos_gg(df):
    
    df_agg=df.groupby('ID_USER').agg(
      monto_total=('monto',sum),
      monto_median=('monto', lambda x: np.median(x)),
      monto_std=('monto', lambda x: np.std(x)),
      trans_count=('monto', lambda x: x.count()),
      dcto_pct=('dcto_pct', lambda x: np.mean(x)),
      cashback_pct=('cashback_pct', lambda x: np.mean(x)),
      establecimiento_count=('establecimiento', lambda x: x.drop_duplicates().count()),
      hora_solar= ('hora_solar', lambda x: np.mean(x)),
      hora_comp= ('hora_comp', lambda x: np.mean(x)),
      weekday= ('weekday_0', lambda x: np.mean(x)),
      linea_tc= ('linea_tc', lambda x: np.mean(x)),
      interes_tc= ('interes_tc', lambda x: np.mean(x)),
      device_score= ('device_score', lambda x: np.mean(x))
      ).reset_index() 
        
    return df_agg

  ################################################################################  

def datos_dummies(df):

    df_dummies=df[['ID_USER','genero','ciudad','is_prime']].drop_duplicates()
    df_dummies['is_prime']=df_dummies['is_prime']*1

    for var in ['genero','ciudad']:
        aux=pd.get_dummies(df_dummies[var]).iloc[:,1:]
        df_dummies=df_dummies.join(aux) 

    df_dummies=df_dummies.drop(columns=['genero','ciudad'])
    df_dummies=df_dummies.reset_index().drop(columns='index') 

    return df_dummies

  ################################################################################  

def datos_tarjeta(df):

    df['aux']=1 

    aux=df[['ID_USER','tipo_tc','aux']].drop_duplicates().pivot(index='ID_USER',columns='tipo_tc')['aux'].reset_index().fillna(0) 

    auxx=df[['ID_USER','status_txn','aux']].drop_duplicates().pivot(index='ID_USER',columns='status_txn')['aux'].reset_index().fillna(0)  

    auxxx=df[['ID_USER','os','aux']].drop_duplicates().pivot(index='ID_USER',columns='os')['aux'].reset_index().fillna(0) 

    df_tjt=aux\
        .merge(auxx,on='ID_USER')\
        .merge(auxxx,on='ID_USER')  
        
    return df_tjt
    