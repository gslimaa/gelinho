import pandas as pd

import streamlit as st
st.write('a')
from streamlit_gsheets import GSheetsConnection
from st_pages import show_pages_from_config


st.set_page_config(page_title='Sabores',layout="wide", initial_sidebar_state="collapsed")
show_pages_from_config()
st.title('Criação de Sabores')

#estabelecendo a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

#Puxando informações de produtos
@st.cache_data(ttl=1)
def ler_sabores():
    dados=conn.read(worksheet='Sabores',usecols=list(range(6)),ttl=1)
    dados=dados.dropna(how='all')
    return dados
dados=ler_sabores()

tipos=['Água','Leite']

with st.form(key="criacao_produtos"):
    Sabor=st.text_input(label='Sabor*')
    Custo=st.number_input(label='Custo*',min_value=0.0,value=1.16,step=1.0)
    Preco_bruto=st.number_input(label='Preço de Venda*',min_value=0.0,value=4.0,step=1.0)
    Tipo=st.selectbox('Tipo*',options=tipos)
    mkp=Preco_bruto/Custo
    id_sabor=dados['Id_Sabor'].max() +1

    st.markdown('**Obrigatório*')

    submitt_button = st.form_submit_button(label="Criar novo Sabor")

    if submitt_button:
        if not Sabor or not Custo or not Preco_bruto or not Tipo:
            st.warning('Preencha todos os campos')
            st.stop()
        elif dados['Sabor'].str.contains(Sabor).any():
            st.warning('Este sabor já existe.')
            st.stop()
        else:
            dados_do_novo_sabor=pd.DataFrame(
                [
                    {
                        'Id_Sabor':id_sabor,
                        'Sabor':Sabor,
                        'Custo':Custo,
                        'Preco_Bruto':Preco_bruto,
                        'Mkp':mkp,
                        'Tipo':Tipo
                    }
                ]
            )
            updated_df=pd.concat([dados,dados_do_novo_sabor],ignore_index=True)   
            #update google sheets
            conn.update(worksheet='Sabores',data=updated_df)
            st.success("Sabor adicionado.")
