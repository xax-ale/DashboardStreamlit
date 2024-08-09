import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Título do aplicativo
st.title("Dashboard Interativo de Vendas")

# Carregar os dados
try:
    df = pd.read_csv("Planilha de Produtos.csv", sep=",", decimal=",")
except FileNotFoundError:
    st.error("Arquivo 'Planilha de Produtos.csv' não encontrado.")
else:
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

    # Filtro de mês
    month = st.sidebar.selectbox("Mês", df["Month"].unique())
    df_filtered = df[df["Month"] == month]

    # Layout das colunas
    col1 = st.columns(1)[0]  # Obtém a primeira coluna da lista de colunas
    col2, col3 = st.columns(2)  # Desembrulha duas colunas
    col4, col5 = st.columns(2)  # Desembrulha duas colunas

    # Gráficos sem tema personalizado
    fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
    col1.plotly_chart(fig_date, use_container_width=True)

    fig_prod = px.bar(df_filtered, x="Date", y="Product line", color="City", title="Faturamento por tipo de produto", orientation="h")
    col2.plotly_chart(fig_prod, use_container_width=True)

    city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
    fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
    col3.plotly_chart(fig_city, use_container_width=True)
    

    fig_kind = px.pie(df_filtered,hole=0.6, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
    col5.plotly_chart(fig_kind, use_container_width=True)

    city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
    fig_rating = px.bar(city_total, y="Rating", x="City", title="Avaliação")
    col4.plotly_chart(fig_rating, use_container_width=True)
