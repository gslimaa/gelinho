import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
from datetime import datetime, timedelta


st.set_page_config(page_title='Venda',layout="wide", initial_sidebar_state="collapsed")
st.title('Criação de Venda')

#estabelecendo a conexão
conn = st.connection("gsheets", type=GSheetsConnection)
#lendo os dados das sheets
@st.cache_data(ttl=1)
def ler_sabores():
    dados=conn.read(worksheet='Sabores',usecols=list(range(6)),ttl=1)
    dados=dados.dropna(how='all')
    return dados

#lendo os dados das sheets
@st.cache_data(ttl=1)
def ler_vendas():
    dados=conn.read(worksheet='Vendas',usecols=list(range(6)),ttl=1)
    dados=dados.dropna(how='all')
    return dados

sabores=ler_sabores()
vendas=ler_vendas()

sabores_a_vender=np.sort(sabores.Sabor.unique())

with st.form(key="vender_sabores"):
    Sabor=st.selectbox('Sabor*',options=sabores_a_vender)
    Quantidade=st.number_input(label='Quantidade vendida*:',min_value=1,value=1,step=1)
    if np.isnan(vendas['Id_Venda'].max()):
        id_venda=1
    else:
        id_venda=vendas['Id_Venda'].max() +1

    st.markdown('**Obrigatório*')

    submitt_button = st.form_submit_button(label="Criar venda")

    if submitt_button:
        if not Sabor or not Quantidade :
            st.warning('Preencha todos os campos')
            st.stop()
        else:
            dados_da_nova_venda=pd.DataFrame(
                [
                    {
                        'Id_Venda':id_venda,
                        'Sabor':Sabor,
                        'Quantidade':Quantidade,
                        'Data':datetime.today().strftime('%Y-%m-%d')
                    }
                ]
            )
            novo_df=dados_da_nova_venda.merge(sabores,on='Sabor',how='left')
            novo_df=novo_df[['Id_Venda','Id_Sabor','Sabor','Preco_Bruto','Quantidade','Data']]
            #st.dataframe(novo_df)
            updated_df=pd.concat([vendas,novo_df],ignore_index=True)   
            #update google sheets
            conn.update(worksheet='Vendas',data=updated_df)
            st.success("Venda adicionada.")