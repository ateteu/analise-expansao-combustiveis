import warnings
from pipelines.senatran    import executar as executar1
from pipelines.pib         import executar as executar2
from pipelines.vendas_anp  import executar as executar3


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

# OBS:
# O pipeline de tratamento de dados de vendas foi refeito de forma muito mais robusta,
# e o arquivo já executa tudo sozinho; Para rodar, basta executá-lo diretamente

def main():
    """
    Executa todos os pipelines de tratamento de dados.
    """
    pipelines = [
        ("SENATRAN"   , executar1),
        ("PIB"        , executar2),
        #("VENDAS_ANP" , executar3), # Utilizar o outro pipeline, mais robusto
    ]

    # Se um pipeline falhar, tenta o próximo
    for nome, pipeline in pipelines:
        try:
            pipeline()

        except Exception as erro:
            print(f"\nFalha em {nome}: {erro}")


if __name__ == "__main__":
    main()
