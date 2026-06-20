from pathlib            import Path

ENCODINGS_CANDIDATOS = [
    "utf-8-sig",
    "latin-1",
    "cp1252",
    "latin-1"
]

def detectar_encoding(caminho: Path, candidatos = ENCODINGS_CANDIDATOS) -> str:
    """
    Detecta o encoding de um arquivo de texto testando, em ordem,
    os encodings mais comuns em fontes governamentais brasileiras.
    Levanta erro explícito se nenhum candidato funcionar.
    """
    for enc in candidatos:
        try:
            with open(caminho, encoding=enc) as f:
                f.read()
            return enc
        
        except (UnicodeDecodeError, ValueError):
            continue

    raise ValueError(f"Não foi possível detectar o encoding de '{caminho}'.")
