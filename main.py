
import numpy as np
from flask import Flask, request
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger

import proc_vars_ind
import proc_vars_agg

import sklearn

app=Flask(__name__)
Swagger(app)

modelo = pickle.load(open('gbc_rappi_fraude.pkl','rb'))
threshold=0.228

@app.route('/')
def welcome():
    return '¡Bienvenido!'

@app.route('/predict_file',methods=['POST'])
def predict_note_file():
    """Bienvenido, introduzca los datos de los usuarios:
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
      
    responses:
        200:
            description: The output values
    """
    df=pd.read_csv(request.files.get('file'))
    
    df=proc_vars_ind.cambiar_valores_nulos_ciudad_establecimiento(df)
    df=proc_vars_ind.procesa_var_hora(df)
    df=proc_vars_ind.procesa_var_fecha(df)

    df_agg = proc_vars_agg.datos_gg(df)
    df_dummies = proc_vars_agg.datos_dummies(df)
    df_tjt= proc_vars_agg.datos_tarjeta(df)

    df_modelo = df_agg.merge(df_dummies,on='ID_USER')\
        .merge(df_tjt,on='ID_USER')

    proba=modelo.predict_proba(df_modelo.drop(columns='ID_USER'))
    proba_true = np.array( [i[1] for i in proba] )
    fraude=(proba_true > threshold)

    df_modelo['FRAUDE'] = 'NO FRAUDE'
    df_modelo.loc[fraude,'FRAUDE'] = 'FRAUDE'

    return dict(zip(df_modelo['ID_USER'], df_modelo['FRAUDE']))

if __name__=='__main__':
    app.run(debug=True)
    