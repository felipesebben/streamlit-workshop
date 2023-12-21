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


def main():
    st.title("Dashboard de Preços de Produtos")

    engine = connect_to_db()
    query = "SELECT DISTINCT titulo, preco FROM produtos ORDER BY preco DESC"
    df = run_query(query, engine)

    st.write("Produtos:")
    st.dataframe(df)

    uploaded_file = st.file_uploader("Carregar arquivo Excel", type="xlsx")
    if uploaded_file is not None:
        excel_data = pd.read_excel(uploaded_file)
        df = pd.concat([df, excel_data])  # Combinar com os dados do banco.
        df = df.nlargest(
            5, "preco"
        )  # Selecionar os top 5 produtos com maior preço após concatenar.

    st.write("Top 5 Produtos (Atualizado):")
    st.dataframe(df)

    plot_types = ["bar", "line", "scatter", "pie"]
    plot_type = st.selectbox("Selecione o tipo de gráfico", plot_types)
    plot = create_plot(df, plot_type)
    st.plotly_chart(plot)

    # Adicionar uma imagem ao gráfico.
    # st.image("caminho_da_imagem.jpg", caption="Imagem de exemplo")

    # Função adicional 1: Seleção de data
    st.date_input("Selecione uma data")

    # Função adicional 2: Caixa de texto
    texto = st.text_input("Digite um texto")

    # Função adicional 3: Slider
    numero = st.slider("Escolha um número", 0, 100)

    # Função adicional 4: Botão de rádio
    opcao = st.radio("Escolha uma opção", ["Opção 1", "Opção 2", "Opção 3"])

    # Função adicional 5: Checkbox
    check = st.checkbox("Marque a opção")

    # Funlção adicional 6: Seletor de cor
    cor = st.color_picker("Escolha uma cor")

    # Mostrar as escolhas do usuário.
    st.write("Texto digitado", texto)
    st.write("Número escolhido", numero)
    st.write("Opção escolhida", opcao)
    st.write("Checkbox marcado", check)
    st.write("Cor escolhida", cor)


if __name__ == "__main__":
    main()
