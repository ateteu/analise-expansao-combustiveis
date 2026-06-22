import pandas as pd

from arquivos.ler_arquivo    import ler_csv, ler_excel
from arquivos.salvar_arquivo import salvar_quarentena
from configs.caminhos        import (
    ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    ARQUIVO_CODIGOS_IBGE,
    AUDITORIA_VENDAS,
    ARQUIVO_VENDAS_ETANOL,
    ARQUIVO_VENDAS_DIESEL,
    ARQUIVO_VENDAS_GASOLINA,
)
from configs.esquemas        import (
    ESQUEMA_VENDAS_ANP,
    ESQUEMA_ORIGINAL_VENDAS,
)
from configs.constantes      import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    UFS_ESCOPO,
    STRINGS_NULAS,
)
from configs.mapeamentos     import MAPA_UF_SIGLA
from configs.colunas         import COLUNAS_CRITICAS_VENDAS
from transformadores.texto   import normalizar_texto
from transformadores.tipos   import (
    colunas_para_inteiro,
    colunas_para_string,
    converter_decimal_br,   
)
from transformadores.dataframe import (
    concatenar,
    ordenar_linhas,
)
from utils.log        import log_etapa
from utils.validacoes import validar_esquema
from utils.auditoria  import (   
    separar_nulos,
    validar_regex,
    validar_dominio,
    validar_intervalo,
    validar_minimo,
    tratar_duplicidades,
    validar_consistencia_grupo,
    identificar_outliers,
)


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ARQUIVOS = {
    "ETANOL":   ARQUIVO_VENDAS_ETANOL,
    "DIESEL":   ARQUIVO_VENDAS_DIESEL,
    "GASOLINA": ARQUIVO_VENDAS_GASOLINA,
}

UFS_VALIDAS      = set(MAPA_UF_SIGLA.values())
COMBUSTIVEIS_VALIDOS = {"ETANOL", "DIESEL", "GASOLINA"}
CHAVE_LOGICA     = ["ano", "uf", "id_municipio", "tipo_combustivel"]


# =========================================================
# ETAPA 1 - CARREGAMENTO DA TABELA DE REFERÊNCIA DO IBGE
# =========================================================

def carregar_ibge(caminho_ibge):
    """
    Carrega e valida a tabela de referência do IBGE.
    Usada para validar código e UF de cada município.

    O skiprows=6 descarta o cabeçalho descritivo do arquivo.
    """
    df_ibge = ler_excel(caminho_ibge, pular_linhas=6)

    validar_esquema(
        df_ibge,
        esperado={"UF", "Código Município Completo", "Nome_Município"},
        origem="IBGE",
    )

    df_ibge = df_ibge.rename(columns={
        "UF":                       "uf",
        "Código Município Completo": "id_municipio",
        "Nome_Município":           "nome_municipio_ibge",
    })

    df_ibge = df_ibge[["uf", "id_municipio", "nome_municipio_ibge"]].copy()
    df_ibge["uf"] = df_ibge["uf"].apply(normalizar_texto)
    df_ibge["id_municipio"] = (
        df_ibge["id_municipio"]
        .str.strip()
        .apply(lambda x: x.zfill(7) if pd.notna(x) and x.strip() != "" else pd.NA)
    )
    df_ibge = df_ibge.dropna(subset=["uf", "id_municipio"])

    return df_ibge


# =========================================================
# ETAPA 2 - VALIDAÇÃO CRUZADA COM O IBGE
# =========================================================

def validar_com_ibge(df, df_ibge, origem=""):
    """
    Valida uf + id_municipio contra a tabela de referência do IBGE.
    Linhas fora da referência vão para quarentena.
    """
    n_antes = len(df)

    chaves_validas = set(zip(df_ibge["uf"], df_ibge["id_municipio"]))
    mask = pd.Series(
        [par in chaves_validas for par in zip(df["uf"], df["id_municipio"])],
        index=df.index,
    )

    salvar_quarentena(df[~mask].copy(), AUDITORIA_VENDAS, f"fora_do_ibge_{origem}.csv")
    df = df[mask].copy()
    log_etapa("Validação IBGE", n_antes, len(df), origem)
    return df


# =========================================================
# ETAPA 3 - PADRONIZAÇÃO DE COLUNAS
# =========================================================

def padronizar_colunas(df):
    """Renomeia as colunas para o schema interno padronizado."""
    return df.rename(columns=ESQUEMA_ORIGINAL_VENDAS)


# =========================================================
# ETAPA 4 - LIMPEZA TEXTUAL
# =========================================================

def limpar_textos(df):
    """Normaliza colunas textuais e converte strings nulas em pd.NA."""
    for coluna in ["uf", "tipo_combustivel", "municipio"]:
        df[coluna] = df[coluna].apply(
            lambda x: normalizar_texto(
                x,
                remover_acentos=False,
                remover_pontuacao=False,
                strings_nulas=STRINGS_NULAS,
            )
        )
    return df


# =========================================================
# ETAPA 5 - CONVERSÃO DE TIPOS
# =========================================================

def converter_tipos(df):
    """
    Converte os campos para seus tipos adequados.
    Valores inválidos viram pd.NA (via errors='coerce').
    """
    df = colunas_para_inteiro(df, ["ano"])

    df["uf"] = df["uf"].map(MAPA_UF_SIGLA)

    df = colunas_para_string(df, ["id_municipio"])
    df["id_municipio"] = df["id_municipio"].apply(
        lambda x: x.zfill(7) if pd.notna(x) and x != "" else pd.NA
    )

    # converter_decimal_br: novo em transformadores/tipos.py
    # Substitui a manipulação manual de str + colunas_para_numero
    df = converter_decimal_br(df, ["volume_vendas_m3"])

    return df


# =========================================================
# ETAPA 6 - REGRAS DE DOMÍNIO
# =========================================================

def aplicar_regras_de_dominio(df, origem=""):
    """
    Aplica regras de plausibilidade por coluna.
    Cada regra usa um validador genérico de utils/auditoria.py.
    Linhas reprovadas em cada regra vão para quarentena separada.
    """
    df = validar_intervalo(df, "ano", ANO_INICIO_ESCOPO_PROJETO, ANO_FIM_ESCOPO_PROJETO, AUDITORIA_VENDAS, origem)
    df = validar_dominio(df, "uf", UFS_VALIDAS, AUDITORIA_VENDAS, origem)
    df = validar_dominio(df, "uf", UFS_ESCOPO,  AUDITORIA_VENDAS, f"{origem}_escopo")
    df = validar_dominio(df, "tipo_combustivel", COMBUSTIVEIS_VALIDOS, AUDITORIA_VENDAS, origem)
    df = validar_minimo(df,  "volume_vendas_m3", 0, AUDITORIA_VENDAS, origem)
    
    return df


# =========================================================
# ETAPA 7 - PIPELINE COMPLETO DE UM ARQUIVO
# =========================================================

def processar_arquivo(caminho_arquivo, combustivel_fixo, df_ibge):
    """
    Executa o pipeline completo de limpeza de um arquivo individual.
    Cada etapa loga quantas linhas sobreviveram e salva os descartados em quarentena.
    """
    origem = combustivel_fixo
    print(f"\n{'='*60}")
    print(f"Processando: {caminho_arquivo}  [{origem}]")
    print(f"{'='*60}")

    df = ler_csv(caminho_arquivo, separador=";")
    print(f"  Linhas lidas: {len(df)}")

    # Coluna de rastreamento: identifica a origem nas quarentenas.
    # Removida antes do output final.
    df["_arquivo_origem"] = combustivel_fixo

    validar_esquema(df.drop(columns=["_arquivo_origem"]), ESQUEMA_ORIGINAL_VENDAS, origem)

    df = padronizar_colunas(df)
    df = limpar_textos(df)
    df = converter_tipos(df)

    df = separar_nulos(df, COLUNAS_CRITICAS_VENDAS, AUDITORIA_VENDAS, origem)
    df = validar_regex(df, "id_municipio", r"^\d{7}$", AUDITORIA_VENDAS, origem)

    # Força o combustível fixo após validação de nulos —
    # garante consistência mesmo que o campo venha errado na origem.
    df["tipo_combustivel"] = combustivel_fixo

    df = aplicar_regras_de_dominio(df, origem)
    df = validar_com_ibge(df, df_ibge, origem)
    df = tratar_duplicidades(df, CHAVE_LOGICA, AUDITORIA_VENDAS, origem)

    validar_consistencia_grupo(df, "id_municipio", "uf", AUDITORIA_VENDAS, origem)

    print(f"  ✓ [{origem}] Linhas aprovadas: {len(df)}")
    return df


# =========================================================
# ETAPA 8 - EXECUÇÃO PRINCIPAL
# =========================================================

def main():
    print("Carregando tabela de referência do IBGE...")
    df_ibge = carregar_ibge(ARQUIVO_CODIGOS_IBGE)
    print(f"  IBGE carregado: {len(df_ibge)} municípios de referência\n")

    dfs = [
        processar_arquivo(arquivo, combustivel, df_ibge)
        for combustivel, arquivo in ARQUIVOS.items()
    ]

    # ── Consolidação ──────────────────────────────────────
    print(f"\n{'='*60}")
    print("Consolidando os 3 arquivos...")
    print(f"{'='*60}")

    df_final = concatenar(dfs)
    df_final = df_final.drop(columns=["_arquivo_origem"], errors="ignore")

    df_final = df_final.rename(columns=ESQUEMA_VENDAS_ANP)
    df_final = df_final[list(ESQUEMA_VENDAS_ANP.values())].copy()

    df_final = ordenar_linhas(df_final, ["ano", "uf", "id_municipio", "tipo_combustivel"])

    # Outliers calculados no consolidado para comparar os 3 combustíveis juntos
    identificar_outliers(df_final, "volume_vendas_m3", AUDITORIA_VENDAS, sufixo="_consolidado")

    # Verificação final: nenhuma duplicidade lógica pode sobrar
    n_dupl = df_final.duplicated(subset=CHAVE_LOGICA).sum()
    if n_dupl > 0:
        raise ValueError(
            f"Duplicidade lógica no dataset final: {n_dupl} linhas. "
            f"Verifique os arquivos em {AUDITORIA_VENDAS}."
        )

    # ── Exportação ────────────────────────────────────────
    df_final.to_csv(
        ARQUIVO_CONSOLIDADO_VENDAS_ANP,
        sep=";",
        index=False,
        encoding="utf-8",
    )

    # ── Resumo final ──────────────────────────────────────
    print(f"\n{'='*60}")
    print("PROCESSAMENTO FINALIZADO")
    print(f"{'='*60}")
    print(f"  Total de linhas finais : {len(df_final)}")
    print(f"  Combustíveis presentes : {sorted(df_final['tipo_combustivel'].unique())}")
    print(f"  Anos cobertos          : {int(df_final['ano'].min())} – {int(df_final['ano'].max())}")
    print(f"  Municípios distintos   : {df_final['id_municipio'].nunique()}")
    print(f"  Arquivo salvo em       : {ARQUIVO_CONSOLIDADO_VENDAS_ANP}")
    print(f"  Quarentena/auditoria   : {AUDITORIA_VENDAS}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
