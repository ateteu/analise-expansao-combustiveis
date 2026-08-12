# Excluir depois

import duckdb
import pandas as pd
import matplotlib.pyplot as plt

from arquivos.salvar_arquivo import salvar_csv
from pathlib                 import Path
from configs.caminhos        import (
    ARQUIVO_BD,
    ARQUIVO_EDA_SQL,
    DADOS_ANALISES,
)

# =========================================================
# CONFIGURAÇÃO DOS GRÁFICOS
# =========================================================

CONFIG_GRAFICOS = {

    "PERGUNTA_1": {
        "tipo": "scatter",
        "x": "pib_per_capita",
        "y": "vol_vendido_total_m3",
        "titulo": "PIB per capita x Consumo de combustível"
    },

    "PERGUNTA_2": {
        "tipo": "scatter",
        "x": "frota_pesada",
        "y": "pct_diesel",
        "titulo": "Frota pesada x Diesel"
    },

    "PERGUNTA_3": {
        "tipo": "scatter",
        "x": "dist_base_atendimento_km",
        "y": "score_final_medio",
        "titulo": "Distância base-município x Score do município"
    },

    "PERGUNTA_4": {
        "tipo": "barh",
        "x": "cagr_vol_vendido_3a",
        "y": "nome_municipio",
        "titulo": "Municípios com melhor índice CAGR"
    },

    "PERGUNTA_5": {
        "tipo": "barh",
        "x": "score_final_norm",
        "y": "nome_municipio",
        "titulo": "Municípios não atendidos mais atrativos"
    }
}


# =========================================================
# FUNÇÕES DE APOIO
# =========================================================

def carregar_queries(caminho_sql):
    """
    Carrega as queries do arquivo perguntas_investigativas.sql.
    """

    texto = Path(caminho_sql).read_text(
        encoding="utf-8"
    )

    blocos = texto.split("-- PERGUNTA_")
    queries = {}

    for bloco in blocos[1:]:

        linhas = bloco.strip().splitlines()
        numero = linhas[0].strip()
        sql = "\n".join(linhas[1:]).strip()
        queries[f"PERGUNTA_{numero}"] = sql

    return queries


def gerar_grafico(
    df            : pd.DataFrame,
    tipo          : str,
    x             : str,
    y             : str,
    titulo        : str,
    caminho_saida : str
) -> None:
    """
    Gera um gráfico a partir de um DataFrame.
    """

    plt.figure(figsize=(10, 6))

    if tipo == "scatter":

        plt.scatter(
            df[x],
            df[y]
        )

        plt.xlabel(x)
        plt.ylabel(y)

    elif tipo == "barh":

        plt.barh(
            df[y].astype(str),
            df[x]
        )

        plt.xlabel(x)
        plt.ylabel(y)

    else:
        raise ValueError(f"Tipo de gráfico não suportado: {tipo}")

    plt.title(titulo)
    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_eda():
    """
    Executa as perguntas investigativas e gera os gráficos.
    """

    DADOS_ANALISES.mkdir(
        parents=True,
        exist_ok=True
    )

    # Carrega o BD e as queries SQL
    conexao = duckdb.connect(ARQUIVO_BD)
    queries = carregar_queries(ARQUIVO_EDA_SQL)

    # Para cada query, gera uma análise gráfica e salva um csv
    for nome, sql in queries.items():

        print(f"Gerando análise: {nome}")

        df = conexao.execute(sql).df()

        print(nome)
        print(df.shape)
        print(df.head())

        config = CONFIG_GRAFICOS[nome]

        gerar_grafico(
            df=df,
            tipo=config["tipo"],
            x=config["x"],
            y=config["y"],
            titulo=config["titulo"],
            caminho_saida=DADOS_ANALISES / f"{nome.lower()}.png"
        )

        salvar_csv(df, DADOS_ANALISES / f"{nome.lower()}.csv")

    conexao.close()
    print("Análises exploratórias concluídas.")
