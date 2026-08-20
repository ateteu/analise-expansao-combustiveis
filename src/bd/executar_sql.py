import duckdb

from utils.log        import log
from configs.caminhos import (
    ARQUIVO_BD,
    DADOS_MODELADOS,
    DIR_SQL,
)


def executar_queries_sql():
    """
    Tenta executar as queries SQL e salva os arquivos csv na pasta adequada.
    """
    log("EXECUÇÃO DE QUERIES\n", separador_antes=True)

    conexao = duckdb.connect(ARQUIVO_BD)

    arquivos_sql = [
        DIR_SQL / "1-metricas" / "anuais" / "metricas_vendas.sql",
        DIR_SQL / "1-metricas" / "anuais" / "metricas_frota.sql",
        DIR_SQL / "1-metricas" / "anuais" / "metricas_economicas.sql",
        DIR_SQL / "1-metricas" / "anuais" / "metricas_logisticas.sql",
        DIR_SQL / "1-metricas" / "series-historicas" / "metricas_cresc_frota.sql",
        DIR_SQL / "1-metricas" / "series-historicas" / "metricas_cresc_vendas.sql",
        DIR_SQL / "2-pontuacoes" / "scores.sql",
        DIR_SQL / "3-tabelas-analiticas" / "dimensao_municipio.sql",
        DIR_SQL / "3-tabelas-analiticas" / "municipios_bi_anual.sql",
        DIR_SQL / "3-tabelas-analiticas" / "municipios_bi_crescimento.sql",
    ]

    for arquivo in arquivos_sql:
        log(rotulo="Query SQL", mensagem=f"Executando {arquivo.name}")

        sql = arquivo.read_text(encoding = "utf-8")

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
            rotulo="Arquivo final criado",
            mensagem=f"{caminho_saida.name}",
            tipo="sucesso",
        )
