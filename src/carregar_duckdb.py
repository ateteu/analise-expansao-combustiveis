import duckdb
from configs.caminhos import (
    ARQUIVO_BD,
    ARQUIVO_MUNICIPIOS_ATENDIDOS,
    ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    ARQUIVO_CONSOLIDADO_FROTA,
    ARQUIVO_CONSOLIDADO_PIB,
    ARQUIVO_CONSOLIDADO_COORD
)

TABELAS = {
    "municipios_atendidos"   : ARQUIVO_MUNICIPIOS_ATENDIDOS,
    "vendas_anp"             : ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    "frota_senatran"         : ARQUIVO_CONSOLIDADO_FROTA,
    "pib_ibge"               : ARQUIVO_CONSOLIDADO_PIB,
    "coordenadas_municipios" : ARQUIVO_CONSOLIDADO_COORD
}

conexao = duckdb.connect(ARQUIVO_BD)

# Cria as tabelas relativas a cada um dos csvs intermediários
for nome_tabela, caminho_arquivo in TABELAS.items():

    conexao.execute(f"""
        CREATE OR REPLACE TABLE {nome_tabela} AS
        SELECT *
        FROM read_csv_auto('{str(caminho_arquivo)}')
    """)

print("Tabelas carregadas com sucesso.")
conexao.close() 
