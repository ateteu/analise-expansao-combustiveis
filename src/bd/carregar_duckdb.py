import duckdb
from configs.caminhos import (
    ARQUIVO_BD,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    ARQUIVO_MUNICIPIOS_ATENDIDOS,
    ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    ARQUIVO_CONSOLIDADO_FROTA,
    ARQUIVO_CONSOLIDADO_DADOS_ECONOMICOS,
    ARQUIVO_CONSOLIDADO_COORD,
)

TABELAS = {
    "municipios"             : ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    "municipios_atendidos"   : ARQUIVO_MUNICIPIOS_ATENDIDOS,
    "vendas_anp"             : ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    "frota_senatran"         : ARQUIVO_CONSOLIDADO_FROTA,
    "dados_economicos"       : ARQUIVO_CONSOLIDADO_DADOS_ECONOMICOS,
    "coordenadas_municipios" : ARQUIVO_CONSOLIDADO_COORD,
}

def carregar_bd():
    conexao = duckdb.connect(ARQUIVO_BD)

    # Cria as tabelas relativas a cada um dos csvs intermediários
    # (elas são usadas nas queries SQL para criar as métricas derivadas)

    for nome_tabela, caminho_arquivo in TABELAS.items():

        conexao.execute(f"""
            CREATE OR REPLACE TABLE {nome_tabela} AS
            SELECT *
            FROM read_csv_auto('{str(caminho_arquivo)}')
        """)

    print("Tabelas intermediárias carregadas com sucesso no Banco de dados.")
    conexao.close() 
