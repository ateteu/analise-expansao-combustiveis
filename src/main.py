import warnings
import traceback

from utils.log                      import log
from pipelines.ppl_frota            import executar_ppl_frota
from pipelines.ppl_dados_economicos import executar_ppl_dados_economicos
from pipelines.ppl_vendas           import executar_ppl_vendas
from pipelines.ppl_coordenadas      import executar_ppl_coordenadas
from pipelines.ppl_municipios       import executar_ppl_municipios
from bd.carregar_duckdb             import carregar_bd
from bd.executar_sql                import executar_queries_sql
from utils.diagnostico              import diagnosticar_csv, arquivos_finais


# Ignorar avisos sobre headers e footers
warnings.filterwarnings("ignore", category = UserWarning, module = "openpyxl")

def main():
    """
    Executa todos os pipelines de tratamento/limpeza de dados,
    carrega o BD e executa as queries SQL.
    """
    passos = [
        #("Pipeline de limpeza [coord. municípios]", executar_ppl_coordenadas),
        #("Pipeline de limpeza [municipios]", executar_ppl_municipios),
        #("Pipeline de limpeza [frota]", executar_ppl_frota),
        #("Pipeline de limpeza [dados econômicos]", executar_ppl_dados_economicos),
        #("Pipeline de limpeza [vendas]", executar_ppl_vendas),
        #("Pipeline do banco de dados", carregar_bd),
        #("Queries SQL", executar_queries_sql),
    ]

    # Se um processo falhar, tenta o próximo
    for nome, passo in passos:
        try:
            passo()

        except Exception:
            log(
                "Função principal (main)",
                f"Falha em: {nome}",
                tipo="erro",
            )
            traceback.print_exc()

    # Faz uma verificação dos arquivos finais gerados para o BI
    log("DIAGNÓSTICO DOS DADOS FINAIS GERADOS", separador_antes=True)
    for arquivo in arquivos_finais:
        diagnosticar_csv(arquivo)

if __name__ == "__main__":
    main()
