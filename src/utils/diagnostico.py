from pathlib              import Path
from utils.log            import log
from arquivos.ler_arquivo import ler_csv
from configs.caminhos     import (
    ARQUIVO_DIMENSAO_MUNICIPIOS,
    ARQUIVO_MUNICIPIOS_BI_ANUAL,
    ARQUIVO_MUNICIPIOS_BI_CRESC,
)

arquivos_finais = [
    ARQUIVO_DIMENSAO_MUNICIPIOS,
    ARQUIVO_MUNICIPIOS_BI_ANUAL,
    ARQUIVO_MUNICIPIOS_BI_CRESC,
]

def diagnosticar_csv(arquivo: Path) -> None:
    """Exibe um diagnóstico resumido de um arquivo CSV."""

    log(f"ARQUIVO: {arquivo.name}\n", separador_interno_antes=True)
    try:
        df = ler_csv(arquivo)

    except Exception as e:
        log(
            f"Erro em [{arquivo.name}]", mensagem=e, tipo="erro",
        )
        return

    linhas, colunas = df.shape
    log("Registros", linhas)
    log("Colunas", colunas)

    if "id_municipio" in df.columns:
        log("Municípios distintos", df["id_municipio"].nunique())

    if "ano" in df.columns:
        anos = df["ano"].dropna()

        if not anos.empty:
            log("Período", mensagem=f"{anos.min()} → {anos.max()}")
            log("Anos distintos", mensagem=anos.nunique())
            log("\n")
            log("Municípios por ano:")

            municipios_por_ano = (
                df.groupby("ano")["id_municipio"]
                .nunique()
                if "id_municipio" in df.columns
                else None
            )

            if municipios_por_ano is not None:
                for ano, quantidade in municipios_por_ano.items():
                    log(str(ano), mensagem=quantidade)

    nulos = df.isna().sum().sum()
    log(
        "Valores nulos",
        mensagem=nulos,
        tipo="sucesso" if nulos == 0 else "aviso",
    )

    duplicadas = df.duplicated().sum()
    log(
        "Linhas duplicadas",
        mensagem=duplicadas,
        tipo="sucesso" if duplicadas == 0 else "aviso",
    )
