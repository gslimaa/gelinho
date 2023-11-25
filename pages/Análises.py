import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import plotly.express as px




st.set_page_config(page_title='Análises',layout="wide", initial_sidebar_state="collapsed")
st.title('Análises')

#estabelecendo a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

#Puxando informações de vendas
@st.cache_data(ttl=1)
def ler_vendas():
    dados=conn.read(worksheet='Vendas',usecols=list(range(6)),ttl=1)
    dados=dados.dropna(how='all')
    return dados

@st.cache_data(ttl=1)
def ler_estoque():
    dados=conn.read(worksheet='Estoque',usecols=list(range(5)),ttl=1)
    dados=dados.dropna(how='all')
    return dados

vendas=ler_vendas()
estoque=ler_estoque()

with st.container():
    st.title('Estoque')
    mostrar_estoque=estoque[['Sabor','Quantidade_Estoque']].copy().rename(columns={'Quantidade_Estoque':'Quantidade'})
    col1, col2 = st.columns([3,7])

    with col1:
        st.write(mostrar_estoque)

    with col2:
        estoque_img = px.bar(mostrar_estoque,x='Sabor',y='Quantidade',text_auto=True)
        st.plotly_chart(estoque_img)

with st.container():
    st.title('Vendas')
    tab_vendas=vendas[['Quantidade','Data']].groupby(by=['Data']).sum().reset_index()
    venda_img = px.line(tab_vendas, x="Data", y="Quantidade")
    st.plotly_chart(venda_img)