import warnings
from pipelines.senatran import executar
from pipelines.pib      import executar


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

def main():
    """
    Executa todos os pipelines de tratamento de dados.
    """
    pipelines = [
        ("SENATRAN", executar),
        ("PIB"     , executar),
    ]

    # Se um pipeline falhar, tenta o próximo
    for nome, pipeline in pipelines:
        try:
            pipeline()

        except Exception as erro:
            print(f"Falha em {nome}: {erro}")


if __name__ == "__main__":
    main()
