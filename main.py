import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from plotly import graph_objects as go
from sqlalchemy import create_engine

# Carregar as variáveis de ambiente.
load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


# Abrir conexão com o banco
def connect_to_db():
    """
    Função para conectar ao banco de dados.
    """
    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    return engine


# Função para rodar query.
def run_query(query, engine):
    """
    Função para rodar query no banco de dados.
    """
    with engine.connect() as conn:
        return pd.read_sql(query, conn)  # Pandas dataframe


def create_plot(df, plot_type):
    """
    Criar gráfico com base no dataframe.
    """
    if plot_type == "bar":
        return go.Figure(data=[go.Bar(x=df["titulo"], y=df["preco"])])
    elif plot_type == "line":
        return go.Figure(
            data=[go.Scatter(x=df.index, y=df["preco"], mode="lines+markers")]
        )
    elif plot_type == "scatter":
        return go.Figure(
            data=[go.Scatter(x=df["titulo"], y=df["preco"], mode="markers")]
        )
    elif plot_type == "pie":
        return go.Figure(data=[go.Pie(labels=df["titulo"], values=df["preco"])])
    # Adicione outros tipos de gráficos conforme necessário.
