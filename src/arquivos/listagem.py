from pathlib import Path
from typing import List


def listar_arquivos(
    caminho: Path,
    padrao: str = "*.xls*",
    ignorar_prefixos: tuple[str, ...] = (".~lock",)
) -> List[Path]:
    """
    Lista arquivos de uma pasta com base em um padrão,
    ignorando arquivos com prefixos indesejados.
    """
    return [
        arquivo
        for arquivo in caminho.glob(padrao)
        if not any(arquivo.name.startswith(p) for p in ignorar_prefixos)
    ]
