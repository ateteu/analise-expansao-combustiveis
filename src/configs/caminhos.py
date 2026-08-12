from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Diretórios base
DADOS_BRUTOS      = BASE_DIR / "dados" / "1-brutos"
DADOS_MODIFICADOS = BASE_DIR / "dados" / "2-intermediarios"
DADOS_MODELADOS   = BASE_DIR / "dados" / "3-modelados"
DADOS_ANALISES    = BASE_DIR / "dados" / "4-analises"
DADOS_DOMINIO     = BASE_DIR / "dados" / "dominio"
DIR_SQL           = BASE_DIR / "sql"


# Diretórios das bases de dados brutos
CAMINHO_FROTA_SENATRAN   = DADOS_BRUTOS / "frota-senatran"
CAMINHO_VENDAS_ANP       = DADOS_BRUTOS / "vendas-anp"
CAMINHO_PIB              = DADOS_BRUTOS / "pib-ibge"
CAMINHO_CODIGOS_IBGE     = DADOS_BRUTOS / "codigos-ibge"
CAMINHO_COORD_MUNICIPIOS = DADOS_BRUTOS / "lat-lon-github"


# Arquivos brutos
ARQUIVO_DADOS_ECONOMICOS = CAMINHO_PIB / "PIB dos Municipios - base de dados 2010-2023.xlsx"
ARQUIVO_CODIGOS_IBGE     = CAMINHO_CODIGOS_IBGE / "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
ARQUIVO_COORD_MUNICIPIOS = CAMINHO_COORD_MUNICIPIOS / "municipios.csv"
ARQUIVO_VENDAS_ETANOL    = CAMINHO_VENDAS_ANP / "vendas-anuais-de-etanol-hidratado-por-municipio.csv"
ARQUIVO_VENDAS_DIESEL    = CAMINHO_VENDAS_ANP / "vendas-anuais-de-oleo-diesel-por-municipio.csv"
ARQUIVO_VENDAS_GASOLINA  = CAMINHO_VENDAS_ANP / "vendas-anuais-de-gasolina-c-por-municipio.csv"


# Arquivos limpos/tratados
ARQUIVO_CONSOLIDADO_VENDAS_ANP       = DADOS_MODIFICADOS / "vendas_anp.csv"
ARQUIVO_CONSOLIDADO_DADOS_ECONOMICOS = DADOS_MODIFICADOS / "dados_economicos_ibge.csv"
ARQUIVO_CONSOLIDADO_FROTA            = DADOS_MODIFICADOS / "frota_senatran.csv"
ARQUIVO_CONSOLIDADO_PIB              = DADOS_MODIFICADOS / "pib_ibge.csv"
ARQUIVO_CONSOLIDADO_COORD            = DADOS_MODIFICADOS / "coordenadas_municipios.csv"
ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE  = DADOS_MODIFICADOS / "municipios_ibge.csv"


# Arquivos de domínio do projeto
ARQUIVO_MUNICIPIOS_ATENDIDOS = DADOS_DOMINIO / "municipios_atendidos.csv"
ARQUIVO_BASES_LOGISTICAS     = DADOS_DOMINIO / "bases_logisticas.csv"
ARQUIVO_REFINARIAS           = DADOS_DOMINIO / "refinarias.csv"
ARQUIVO_TIPOS_COMBUSTIVEL    = DADOS_DOMINIO / "tipos_combustivel.csv"
ARQUIVO_UFS_ESCOPO           = DADOS_DOMINIO / "ufs_em_escopo.csv"


# Arquivo do banco de dados DuckDB
ARQUIVO_BD      = BASE_DIR / "dados" / "banco_dados.duckdb"


# Arquivos SQL
ARQUIVO_EDA_SQL = DIR_SQL / "4-analise" / "perguntas_investigativas.sql"


# Diretórios das pastas de auditoria (quarentenas/limpezas)
AUDITORIA                  = DADOS_MODIFICADOS / "auditoria-dados"
AUDITORIA_VENDAS           = AUDITORIA / "aud-vendas"
AUDITORIA_COORD_MUNICIPIOS = AUDITORIA / "aud-coord-municipios"
AUDITORIA_MUNICIPIOS       = AUDITORIA / "aud-municipios-ibge"
AUDITORIA_DADOS_ECONOMICOS = AUDITORIA / "aud-dados-economicos"
AUDITORIA_FROTA            = AUDITORIA / "aud-frota"
