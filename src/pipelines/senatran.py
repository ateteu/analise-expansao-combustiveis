from arquivos.para_csv         import salvar_csv
from configs.caminhos          import (
    CAMINHO_SENATRAN,
    DADOS_MODIFICADOS
)
from configs.constantes        import NOME_CSV_GERADO_SENATRAN
from dominios.d_senatran       import processar_arquivo_senatran
from transformadores.dataframe import (
    concatenar,
    ordenar_linhas,
    reordenar_colunas
)
from dominios.d_ibge           import adicionar_codigo_ibge
from configs.colunas           import (
    PRIMEIRAS_COL_SENATRAN,
    ORDEM_LINHAS
)
from arquivos.listagem         import listar_arquivos


def executar():
    """
    Pipeline completo da base SENATRAN:
    - lê todos os arquivos anuais
    - padroniza
    - consolida
    - adiciona códigos IBGE
    - salva csv final
    """
    print("=======================================================")
    print("BASE DE DADOS SENATRAN\n")

    # Lista arquivos da pasta
    arquivos = listar_arquivos(CAMINHO_SENATRAN)

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo SENATRAN encontrado.")

    dfs = []
    
    for arquivo in arquivos:
        try:
            df = processar_arquivo_senatran(arquivo)
            dfs.append(df)
            print(f"✓ Processado:  [{arquivo.name}]")

        except Exception as erro:
            print(f"✗ Erro em:     [{arquivo.name}]:  {erro}")

    if not dfs:
        raise RuntimeError("Nenhum arquivo SENATRAN foi processado com sucesso.")

    # Junta os dados dos diferentes arquivos em um só
    df_final = concatenar(dfs)

    # Adiciona códigos IBGE a cada município
    df_final = adicionar_codigo_ibge(df_final)

    # Deixa apenas ID_MUNICIPIO como identificador do município
    df_final = df_final.drop(columns = "MUNICIPIO")

    # Ordena linhas e colunas
    df_final = ordenar_linhas(df_final, ORDEM_LINHAS)
    df_final = reordenar_colunas(df_final, PRIMEIRAS_COL_SENATRAN)

    try:
        salvar_csv(
            df_final,
            pasta_saida  = DADOS_MODIFICADOS,
            nome_arquivo = NOME_CSV_GERADO_SENATRAN
        )
    
    except Exception as erro:
        print(f"✗ Erro ao salvar CSV: {erro}")
        raise
