# Este arquivo contém caminhos utilizados nos códigos

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


DADOS_BRUTOS         = BASE_DIR / "dados" / "1-brutos"
DADOS_MODIFICADOS    = BASE_DIR / "dados" / "2-intermediarios"


ARQUIVO_PIB          = DADOS_BRUTOS / "pib-ibge" / "PIB dos Municipios - base de dados 2010-2023.xlsx"
ARQUIVO_CODIGOS_IBGE = DADOS_BRUTOS / "codigos-ibge" / "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"


CAMINHO_SENATRAN     = DADOS_BRUTOS / "frota-senatran"
CAMINHO_VENDAS_ANP   = DADOS_BRUTOS / "vendas-anp"


ARQUIVO_BD                     = BASE_DIR / "dados" / "banco_dados.duckdb"
ARQUIVO_MUNICIPIOS_ATENDIDOS   = DADOS_BRUTOS / "municipios_atendidos" / "municipios_atendidos.csv"
ARQUIVO_CONSOLIDADO_VENDAS_ANP = DADOS_MODIFICADOS / "vendas_anp.csv"
ARQUIVO_CONSOLIDADO_FROTA      = DADOS_MODIFICADOS / "frota_senatran.csv"
ARQUIVO_CONSOLIDADO_PIB        = DADOS_MODIFICADOS / "pib_ibge.csv"
ARQUIVO_CONSOLIDADO_COORD      = DADOS_MODIFICADOS / "coordenadas_municipios.csv"
