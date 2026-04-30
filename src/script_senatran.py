import glob
from pathlib import Path
import re
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

pasta = BASE_DIR / "dados/brutos/frota-senatran"
pasta_saida = BASE_DIR / "dados/modificados"

arquivos = list(pasta.glob("*.xls*"))


dfs = []

for arquivo in arquivos:

    # Busca pelo ano no nome do arquivo
    ano = int(
        re.search(
            r'\d{4}', 
            str(arquivo)
        ).group()
    )

    # Tenta ler os arquivos da pasta
    try:
        if arquivo.suffix == ".xls":
            df = pd.read_excel(
                arquivo, 
                skiprows=2, 
                engine="xlrd"
            )
        elif  arquivo.suffix == ".xlsx":
            df = pd.read_excel(
                arquivo, 
                skiprows=2, 
                engine="openpyxl"
            )
        else:
            continue
        
        if "UF" not in df.columns:
            raise ValueError(f"Header inválido no arquivo: {arquivo}")
        
    except Exception as e:
        print(f"Erro no arquivo {arquivo}: {e}")
        continue
    
    # Cria a coluna ano e a deixa como 1a coluna
    df['ANO'] = ano
    cols = ["ANO"] + [c for c in df.columns if c != "ANO"]
    df = df[cols]

    dfs.append(df)

frota = pd.concat(dfs, ignore_index=True)

# Ordena por ano, UF e município
frota = frota.sort_values(
    ["ANO", "UF", "MUNICIPIO"]
)

# Salva como csv
frota.to_csv(
    pasta_saida / "frota-senatran.csv", 
    index=False
)
