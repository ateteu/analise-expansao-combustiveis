import warnings
from pipelines.senatran import executar as executar_senatran
from pipelines.pib      import executar as executar_pib


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

def main():
    """
    Executa todos os pipelines de tratamento de dados.
    """
    pipelines = [
        ("SENATRAN", executar_senatran),
        ("PIB"     , executar_pib),
    ]

    # Se um pipeline falhar, tenta o próximo
    for nome, pipeline in pipelines:
        try:
            pipeline()

        except Exception as erro:
            print(f"Falha em {nome}: {erro}")


if __name__ == "__main__":
    main()
