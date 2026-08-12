import pandas as pd
from pathlib import Path

from arquivos.ler_arquivo      import ler_excel, ler_csv
from arquivos.salvar_arquivo   import salvar_csv
from arquivos.listagem         import listar_arquivos
from configs.caminhos          import (
    CAMINHO_FROTA_SENATRAN,
    ARQUIVO_CONSOLIDADO_FROTA,
    ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE,
    AUDITORIA_FROTA,
)
from configs.constantes        import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    NOME_ABA_FROTA_2015,
    STRINGS_NULAS,
    UFS_ESCOPO,
)
from configs.mapeamentos       import (
    MAPA_UF_SIGLA,
    CORRECOES_MUNICIPIOS
)
from configs.colunas           import (
    COLUNAS_CRITICAS_FROTA, 
    COLUNAS_INT_FROTA,
    COMPONENTES_FROTA,
    COLUNAS_IDENTIFICADORAS_FROTA,
    COLUNAS_SAIDA_FROTA,
)
from configs.esquemas          import ESQUEMA_FROTA
from transformadores.arquivos  import extrair_ano
from transformadores.texto     import normalizar_texto
from transformadores.tipos     import (
    colunas_para_inteiro,
    colunas_para_string,
)
from transformadores.dataframe import (
    concatenar,
    ordenar_linhas,
    selecionar_colunas,
)
from utils.validacoes          import validar_esquema
from utils.auditoria           import (
    separar_nulos,
    validar_dominio,
    validar_intervalo,
    tratar_duplicidades,
    identificar_outliers,
    validar_soma_componentes,
)
from utils.log                 import (
    log,
)


# =========================================================
# CONFIGURAÇÕES
# =========================================================

UFS_VALIDAS = set(MAPA_UF_SIGLA.values())

# Nomes das colunas na tabela de referência de municípios usados para o join
# Ajustar se o output do pipeline de municípios usar nomes diferentes
COL_REF_SIGLA_UF  = "sigla_uf"
COL_REF_NOME_MUN  = "nome_municipio"


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def _encontrar_linha_cabecalho(df_bruto: pd.DataFrame) -> int:
    """
    Localiza a linha do cabeçalho real nos arquivos de frota.
    Identifica a linha que contém simultaneamente UF, MUNIC e TOTAL.
    """
    for indice, linha in df_bruto.iterrows():
        valores = linha.astype(str).str.upper()
        if (
            valores.str.contains("UF",    na=False).any()
            and valores.str.contains("MUNIC", na=False).any()
            and valores.str.contains("TOTAL", na=False).any()
        ):
            return indice
    
    raise ValueError("Cabeçalho não encontrado no arquivo.")


def _remover_linhas_invalidas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove linhas vazias, cabeçalhos repetidos e registros sem UF válida (2 chars).
    """
    df = df.dropna(how="all")
    df = df[df["uf"].notna()]
    df = df[df["uf"].astype(str).str.upper() != "UF"]
    df = df[df["uf"].astype(str).str.len() == 2]

    return df.copy()


def _corrigir_municipios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica o dicionário CORRECOES_MUNICIPIOS para padronizar nomes de
    municípios grafados de forma errada ou inconsistente na fonte.
    A correção usa como chave o par (sigla_uf, nome_normalizado).
    """
    chaves = list(zip(df["uf"], df["municipio"]))
    df["municipio"] = [
        CORRECOES_MUNICIPIOS.get(chave, nome)
        for chave, nome in zip(chaves, df["municipio"])
    ]
    return df


def _preparar_referencia_municipios(df_municipios: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara a tabela de referência do IBGE para o join com os dados de frota.
    Normaliza nome do município e sigla da UF no mesmo formato usado nos dados de frota,
    garantindo que ambos os lados do merge sejam comparáveis.
    """
    ref = df_municipios[[COL_REF_SIGLA_UF, COL_REF_NOME_MUN, "id_municipio"]].copy()

    ref[COL_REF_NOME_MUN] = ref[COL_REF_NOME_MUN].apply(
        lambda x: normalizar_texto(
            x,
            remover_acentos=True,
            maiusculo=True
        )
    )
    ref[COL_REF_SIGLA_UF] = ref[COL_REF_SIGLA_UF].apply(
        lambda x: normalizar_texto(
            x,
            remover_acentos=False,
            maiusculo=True
        )
    )
    return ref


def _mapear_id_municipio(
    df: pd.DataFrame,
    ref_municipios: pd.DataFrame,
) -> pd.DataFrame:
    """
    Adiciona a coluna id_municipio via merge com a tabela de referência do IBGE.
    Linhas sem correspondência ficam com id_municipio nulo e são capturadas
    pela etapa seguinte de separar_nulos.
    """
    df = df.merge(
        ref_municipios,
        left_on=["uf", "municipio"],
        right_on=[COL_REF_SIGLA_UF, COL_REF_NOME_MUN],
        how="left",
    )
    # Remove colunas auxiliares trazidas pelo merge
    df = df.drop(columns=[COL_REF_SIGLA_UF, COL_REF_NOME_MUN], errors="ignore")
    return df


# =========================================================
# PIPELINE DE UM ARQUIVO INDIVIDUAL
# =========================================================

def processar_arquivo(
    caminho: Path,
    ref_municipios: pd.DataFrame,
) -> pd.DataFrame:
    """
    Carrega, limpa e padroniza um arquivo anual de frota do DENATRAN/SENATRAN.
    Inclui detecção dinâmica do cabeçalho, correção de nomes de municípios
    e mapeamento de id_municipio via tabela de referência do IBGE.
    """
    origem = caminho.name

    # Arquivo de 2015 é o único com mais de uma aba
    ano = extrair_ano(caminho.name)
    aba = NOME_ABA_FROTA_2015 if ano == 2015 else 0

    # Primeiro localizar o cabeçalho, depois para ler os dados
    try:
        df_bruto = ler_excel(caminho, aba=aba, cabecalho=None)
        linha_cab = _encontrar_linha_cabecalho(df_bruto)
        
        df = ler_excel(caminho, aba=aba, pular_linhas=linha_cab)

    except Exception as e:
        raise RuntimeError(f"Erro ao ler [{caminho.name}]: {e}")

    df["ano"] = ano

    # Normaliza nomes das colunas para snake_case sem acentos
    df.columns = df.columns.map(
        lambda col: normalizar_texto(
            col, 
            separador="_",
            maiusculo=False
        )
    )

    df = _remover_linhas_invalidas(df)
    validar_esquema(
        df.drop(columns=["ano"]),
        esperado=ESQUEMA_FROTA,
        origem=origem
    )
    
    # Normaliza uf e municipio para comparação
    df = colunas_para_string(df, ["uf", "municipio"])

    df["uf"] = df["uf"].apply(
        lambda x: normalizar_texto(
            x,
            remover_acentos=False,
            maiusculo=True,
            strings_nulas=STRINGS_NULAS
        )
    )
    df["municipio"] = df["municipio"].apply(
        lambda x: normalizar_texto(
            x,
            remover_acentos=True,
            maiusculo=True,
            strings_nulas=STRINGS_NULAS
        )
    )

    df = colunas_para_inteiro(df, COLUNAS_INT_FROTA)

    df = separar_nulos(
        df,
        colunas=COLUNAS_CRITICAS_FROTA,
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo=origem
    )
    df = validar_dominio(
        df,
        coluna="uf",
        valores_validos=UFS_VALIDAS,
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo=origem
    )
    df = validar_dominio(
        df,
        coluna="uf",
        valores_validos=UFS_ESCOPO,
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo=f"{origem}_escopo"
    )
    df = validar_intervalo(
        df,
        coluna="ano",
        minimo=ANO_INICIO_ESCOPO_PROJETO,
        maximo=ANO_FIM_ESCOPO_PROJETO,
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo=origem
    )

    # Corrige grafias erradas antes do join com o IBGE
    df = _corrigir_municipios(df)
    df = _mapear_id_municipio(df, ref_municipios)

    # Linhas sem correspondência no IBGE vão para quarentena
    df = separar_nulos(
        df,
        colunas=["id_municipio"],
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo=f"{origem}_sem_ibge"
    )
    
    # UF e municipio não são mais necessários
    df = selecionar_colunas(df, COLUNAS_SAIDA_FROTA)

    df = tratar_duplicidades(
        df,
        COLUNAS_IDENTIFICADORAS_FROTA,
        AUDITORIA_FROTA,
        origem
    )
    return df


# =========================================================
# EXECUÇÃO PRINCIPAL
# =========================================================

def executar_ppl_frota() -> None:
    """
    Executa o pipeline completo de limpeza dos dados de frota.
    """
    log("PIPELINE FROTA\n", separador_antes=True)

    try:
        df_municipios = ler_csv(ARQUIVO_CONSOLIDADO_MUNICIPIOS_IBGE)
    
    except Exception as e:
        raise RuntimeError(
            f"Falha ao carregar base de referência de municípios: {e}"
        )

    ref_municipios = _preparar_referencia_municipios(df_municipios)

    # Lista e processa cada arquivo de frota individualmente
    arquivos = listar_arquivos(CAMINHO_FROTA_SENATRAN)
    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum arquivo de frota encontrado em: {CAMINHO_FROTA_SENATRAN}"
        )

    dfs = []
    for arquivo in arquivos:
        try:
            df = processar_arquivo(arquivo, ref_municipios)
            dfs.append(df)
        
        except Exception as e:
            log(f"Erro em [{arquivo.name}]: {e}", tipo="erro")

    if not dfs:
        raise RuntimeError(
            "Nenhum arquivo de frota foi processado com sucesso."
        )

    # Consolida todos os anos em um único DataFrame
    df_final = concatenar(dfs)
    df_final = ordenar_linhas(df_final, COLUNAS_IDENTIFICADORAS_FROTA)

    # Auditoria: total deve ser igual à soma dos tipos de veículo (sem remoção)
    validar_soma_componentes(
        df_final,
        coluna_total="total",
        colunas_componentes=COMPONENTES_FROTA,
        pasta_auditoria=AUDITORIA_FROTA,
        prefixo="consolidado",
    )

    resultado_outliers = identificar_outliers(
        df_final,
        coluna="total",
        pasta_auditoria=AUDITORIA_FROTA,
        sufixo="_consolidado"
    )

    # Verificação final de unicidade da chave de negócio
    n_dupl = df_final.duplicated(subset=COLUNAS_IDENTIFICADORAS_FROTA).sum()
    if n_dupl > 0:
        raise ValueError(
            f"Duplicidade lógica no dataset final: {n_dupl} linhas. "
            f"Verifique os arquivos em {AUDITORIA_FROTA}."
        )

    try:
        salvar_csv(
            df_final,
            ARQUIVO_CONSOLIDADO_FROTA,
        )
    
    except Exception as e:
        raise RuntimeError(f"Falha ao salvar output final: {e}")

    # Printa a mensagem final de resumo do pipeline
    log("Processamento finalizado:\n", separador_interno_antes=True)
    log("Total de registros finais", len(df_final))
    log(
        "Anos cobertos", 
        f"{int(df_final['ano'].min())} a {int(df_final['ano'].max())}"
    )
    if resultado_outliers is not None:
        limiar, quantidade = resultado_outliers
        log(
            f"P99 total (veículos)",
            f"{limiar:,.2f} ({quantidade} linhas acima do limiar)",
            tipo="aviso",
        )
    log("Municípios distintos", df_final['id_municipio'].nunique())
    log("Auditoria", AUDITORIA_FROTA / "", separador_final=True)
    log("Arquivo salvo em", ARQUIVO_CONSOLIDADO_FROTA)


if __name__ == "__main__":
    executar_ppl_frota()
