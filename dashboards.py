import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("Planilha de Produtos.csv", sep=";", decimal=",")
df.columns = df.columns.str.strip()  # Remove espaços extras dos nomes das colunas

if "Data" in df.columns:
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
else:
    st.error("A coluna 'Data' não foi encontrada no arquivo CSV.")
    st.stop()

df = df.sort_values("Data")
df["Month"] = df["Data"].apply(lambda x: f"{x.year}-{x.month:02d}")

month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Data", y="Total", color="Cidade", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Tipo de Produto", y="Total", color="Cidade", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

city_total = df_filtered.groupby("Cidade")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="Cidade", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Total", names="Tipo de pagamento", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

if "Avaliação" in df.columns:
    city_rating = df_filtered.groupby("Cidade")[["Avaliação"]].mean().reset_index()
    fig_rating = px.bar(city_rating, x="Cidade", y="Avaliação", title="Avaliação")
    col5.plotly_chart(fig_rating, use_container_width=True)
else:
    st.error("A coluna 'Avaliação' não foi encontrada no arquivo CSV.")
    col5.write("A coluna 'Avaliação' não está disponível.")
