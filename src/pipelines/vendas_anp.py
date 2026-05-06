from arquivos.para_csv         import salvar_csv
from configs.caminhos          import (
    DADOS_MODIFICADOS,
    CAMINHO_VENDAS_ANP
)
from configs.constantes        import NOME_CSV_GERADO_VENDAS_ANP
from transformadores.dataframe import (
    concatenar,
    ordenar_linhas,
    reordenar_colunas
)
from configs.colunas           import (
    ORDEM_LINHAS, 
    ORDEM_COL_VENDAS_ANP
)
from dominios.d_anp            import processar_arquivo_anp
from arquivos.listagem         import listar_arquivos


def executar():
    """
    Pipeline completo da base de vendas da ANP:
    - lê todos os arquivos anuais
    - padroniza
    - consolida
    - salva csv final
    """
    print("=======================================================")
    print("BASE DE DADOS VENDAS ANP\n")

    # Lista arquivos da pasta
    arquivos = listar_arquivos(CAMINHO_VENDAS_ANP, padrao = "*.csv")

    if not arquivos:
        raise FileNotFoundError("Nenhum arquivo ANP encontrado.")

    dfs = []
    
    for arquivo in arquivos:
        try:
            df = processar_arquivo_anp(arquivo)
            dfs.append(df)
            print(f"✓ Processado:  [{arquivo.name}]")

        except Exception as erro:
            print(f"✗ Erro em:     [{arquivo.name}]:  {erro}")

    if not dfs:
        raise RuntimeError("Nenhum arquivo ANP foi processado com sucesso.")
    
    # Junta os dados dos diferentes arquivos em um só
    df_final = concatenar(dfs)

    # Ordena linhas e colunas
    df_final = ordenar_linhas(df_final, ORDEM_LINHAS)
    df_final = reordenar_colunas(df_final, ORDEM_COL_VENDAS_ANP)

    try:
        salvar_csv(
            df_final,
            pasta_saida  = DADOS_MODIFICADOS,
            nome_arquivo = NOME_CSV_GERADO_VENDAS_ANP
        )
    
    except Exception as erro:
        print(f"✗ Erro ao salvar CSV: {erro}")
        raise
