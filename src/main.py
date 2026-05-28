import warnings
from pipelines.senatran    import executar as executar_ppl_senatran
from pipelines.pib         import executar as executar_ppl_pib
from pipelines.vendas_anp  import executar as executar_ppl_vendas
from bd.carregar_duckdb    import carregar_bd
from bd.executar_sql       import executar_queries_sql


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

# OBS:
# O pipeline de tratamento de dados de vendas foi refeito de forma muito mais robusta,
# e o arquivo já executa tudo sozinho; Para rodar, basta executá-lo diretamente

def main():
    """
    Executa todos os pipelines de tratamento/limpeza de dados,
    carrega o BD e executa as queries SQL.
    """
    passos = [
        #("SENATRAN"     , executar_ppl_senatran),
        #("PIB"          , executar_ppl_pib),
        #("VENDAS ANP"   , executar_ppl_vendas), # Deixar comentado por enquanto
        ("BANCO DE DADOS", carregar_bd),
        ("QUERIES SQL"   , executar_queries_sql)
    ]

    # Se um processo falhar, tenta o próximo
    for nome, passo in passos:
        try:
            passo()

        except Exception as erro:
            print(f"\nFalha em {nome}: {erro}")


if __name__ == "__main__":
    main()
