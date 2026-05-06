import warnings
from pipelines.senatran    import executar as executar1
from pipelines.pib         import executar as executar2
from pipelines.vendas_anp  import executar as executar3


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

def main():
    """
    Executa todos os pipelines de tratamento de dados.
    """
    pipelines = [
        ("SENATRAN"   , executar1),
        #("PIB"        , executar2),
        #("VENDAS_ANP" , executar3),
    ]

    # Se um pipeline falhar, tenta o próximo
    for nome, pipeline in pipelines:
        try:
            pipeline()

        except Exception as erro:
            print(f"\nFalha em {nome}: {erro}")


if __name__ == "__main__":
    main()
