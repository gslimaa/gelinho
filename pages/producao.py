import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta

st.set_page_config(page_title='Produção',layout="wide", initial_sidebar_state="collapsed")
st.title('Criação de Produção')
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
def ler_producao():
    dados=conn.read(worksheet='Produção',usecols=list(range(4)),ttl=1)
    dados=dados.dropna(how='all')
    return dados





sabores=ler_sabores()
producao=ler_producao()
#st.dataframe(sabores)
#st.dataframe(producao)

sabores_a_produzir=sabores.Sabor.unique()
#sabores_a_produzir


with st.form(key="produzir_sabores"):
    Sabor=st.selectbox('Sabor*',options=sabores_a_produzir)
    Quantidade=st.number_input(label='Quantidade produzida*:',min_value=1,value=1,step=1)

    st.markdown('**Obrigatório*')

    submitt_button = st.form_submit_button(label="Criar produção")

    if submitt_button:
        if not Sabor or not Quantidade :
            st.warning('Preencha todos os campos')
            st.stop()
        else:
            dados_da_nova_produção=pd.DataFrame(
                [
                    {
                        
                        'Sabor':Sabor,
                        'Quantidade':Quantidade,
                        'Data':datetime.today().strftime('%Y-%m-%d')
                    }
                ]
            )
            novo_df=dados_da_nova_produção.merge(sabores,on='Sabor',how='left')
            novo_df=novo_df[['Id_Sabor','Sabor','Quantidade','Data']]
            #st.dataframe(novo_df)
            updated_df=pd.concat([producao,novo_df],ignore_index=True)   
            #update google sheets
            conn.update(worksheet='Produção',data=updated_df)
            st.success("Produção adicionada.")