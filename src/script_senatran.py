from pathlib import Path
import funcoes_utilitarias as f

# Obtém diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

pasta_entrada = BASE_DIR / "dados/1-brutos/frota-senatran"
pasta_destino = BASE_DIR / "dados/2-intermediarios"

# Carrega dados da tabela de códigos do IBGE
caminho_codigos_ibge = BASE_DIR / "dados/1-brutos/codigos-ibge/RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
df_ibge = f.carregar_codigos_ibge(caminho_codigos_ibge)

# Encontra arquivos excel (.xls, .xlsx, .xlsb) na pasta
arquivos = list(pasta_entrada.glob("*.xls*"))
dfs = []

for arquivo in arquivos:

    ano = f.extrair_ano_do_nome_arquivo(arquivo.name)

    try:
        df_bruto = f.ler_arquivo_bruto(arquivo)
        indice_cabecalho = f.encontrar_linha_cabecalho(df_bruto)
        df = f.ler_arquivo(arquivo, indice_cabecalho)
        df = f.padronizar_colunas(df)
        f.verificar_se_existem_colunas_essenciais(df, arquivo)
        df = f.limpar_dados(df)
        df = f.criar_coluna_ano(df, ano)

    except Exception as e:
        print(f"Erro no arquivo {arquivo}: {e}")
        continue
    
    dfs.append(df)

df_final = f.concatenar_dfs_e_ordenar(dfs)
df_final = f.adicionar_codigo_ibge(df_final, df_ibge)

# Ordena a ordem final das colunas
primeiras_col = ["ANO", "UF", "MUNICIPIO", "ID_MUNICIPIO"]
colunas = primeiras_col + [c for c in df_final.columns if c not in primeiras_col]
df_final = df_final[colunas]

f.salvar_como_csv(df_final, pasta_destino, "frota-senatran.csv")
