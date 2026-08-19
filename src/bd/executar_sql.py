import duckdb

from pathlib          import Path
from utils.log        import log
from configs.caminhos import (
    ARQUIVO_BD,
    DADOS_MODELADOS
)


def executar_queries_sql():
    """
    Tenta executar as queries SQL e salva os arquivos csv na pasta adequada.
    """
    conexao = duckdb.connect(ARQUIVO_BD)

    arquivos_sql = [
        "sql/1-metricas/anuais/metricas_vendas.sql",
        "sql/1-metricas/anuais/metricas_frota.sql",
        "sql/1-metricas/anuais/metricas_economicas.sql",
        "sql/1-metricas/anuais/metricas_logisticas.sql",
        "sql/1-metricas/series-historicas/metricas_cresc_frota.sql",
        "sql/1-metricas/series-historicas/metricas_cresc_vendas.sql",
        "sql/2-pontuacoes/scores.sql",
        "sql/3-tabelas-analiticas/dimensao_municipio.sql",
        "sql/3-tabelas-analiticas/municipios_bi_anual.sql",
        "sql/3-tabelas-analiticas/municipios_bi_crescimento.sql",
    ]

    for arquivo in arquivos_sql:
        log(rotulo="Queries SQL", mensagem=f"Executando {arquivo}")

        sql = Path(arquivo).read_text(encoding = "utf-8")

        try:
            conexao.execute(sql)
        
        except Exception as e:
            raise RuntimeError(
                f"Erro ao executar SQL [{arquivo}]: {e}"
            ) from e

    exports = [
        "dimensao_municipio",
        "municipios_bi_anual",
        "municipios_bi_crescimento",
    ]

    DADOS_MODELADOS.mkdir(parents = True, exist_ok = True)

    for tabela in exports:

        caminho_saida = DADOS_MODELADOS / f"{tabela}.csv"

        conexao.execute(f"""
            COPY {tabela}
            TO '{caminho_saida}'
            (HEADER, DELIMITER ';');
        """)

        log(
            "Queries SQL",
            f"CSV final criado. Caminho: {caminho_saida}",
            tipo="sucesso",
        )
