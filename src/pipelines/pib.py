from arquivos.ler_arquivo      import ler_excel
from arquivos.salvar_arquivo   import salvar_csv
from configs.caminhos          import (
    DADOS_MODIFICADOS,
    ARQUIVO_PIB
)
from configs.constantes        import NOME_CSV_GERADO_PIB
from transformadores.dataframe import (
    ordenar_linhas,
    reordenar_colunas
)
from configs.colunas           import (
    ORDEM_LINHAS,
    ORDEM_COL_PIB,
    COLUNAS_NUM_PIB,
    COLUNAS_STR_PIB
)
from configs.esquemas          import ESQUEMA_PIB
from transformadores.tipos     import (
    colunas_para_string,
    colunas_para_inteiro,
    colunas_para_float
)


def executar():
    """
    Pipeline completo da base PIB | IBGE:
    - lê o arquivo
    - extrai colunas desejadas
    - padroniza e ordena
    - salva csv final
    """
    print("=======================================================")
    print("BASE DE DADOS PIB IBGE\n")

    try:
        df = ler_excel(
            ARQUIVO_PIB, 
            usar_colunas = ESQUEMA_PIB.keys()
        )
        print(f"✓ Processado:  [{ARQUIVO_PIB.name}]")
    
    except Exception as erro:
        print(f"✗ Erro em:     [{ARQUIVO_PIB.name}]:  {erro}")

    # Renomeia as colunas segundo o esquema
    df = df.rename(columns = ESQUEMA_PIB)

    # Padroniza os tipos dos dados
    df = colunas_para_string(df, COLUNAS_STR_PIB)
    df = colunas_para_inteiro(df, ["ano"])
    df = colunas_para_float(df, COLUNAS_NUM_PIB)

    # Ordena colunas e linhas
    df = ordenar_linhas(df, ORDEM_LINHAS)
    df = reordenar_colunas(df, ORDEM_COL_PIB)

    try:
        salvar_csv(
            df, 
            pasta_saida  = DADOS_MODIFICADOS, 
            nome_arquivo = NOME_CSV_GERADO_PIB
        )
    
    except Exception as erro:
        print(f"✗ Erro ao salvar CSV:  {erro}")
