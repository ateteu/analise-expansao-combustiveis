import pandas as pd
from arquivos.ler_arquivo    import ler_csv
from arquivos.salvar_arquivo import salvar_quarentena
from configs.caminhos        import (
    ARQUIVO_CONSOLIDADO_VENDAS_ANP,
    ARQUIVO_CODIGOS_IBGE,
    AUDITORIA_VENDAS,
    ARQUIVO_VENDAS_ETANOL,
    ARQUIVO_VENDAS_DIESEL,
    ARQUIVO_VENDAS_GASOLINA
)
from configs.esquemas        import (
    ESQUEMA_VENDAS_ANP,
    ESQUEMA_ORIGINAL_VENDAS
)
from configs.constantes      import (
    ANO_INICIO_ESCOPO_PROJETO,
    ANO_FIM_ESCOPO_PROJETO,
    UFS_ESCOPO,
    STRINGS_NULAS
)
from configs.mapeamentos     import (
    MAPA_UF_SIGLA
)
from transformadores.texto   import normalizar_texto
from utils.log               import log_etapa
from configs.colunas         import (
    COLUNAS_CRITICAS_VENDAS
)
from utils.validacoes        import validar_esquema


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ARQUIVOS = {
    "ETANOL": ARQUIVO_VENDAS_ETANOL,
    "DIESEL": ARQUIVO_VENDAS_DIESEL,
    "GASOLINA": ARQUIVO_VENDAS_GASOLINA,
}

# Valores válidos para controle de domínio
UFS_VALIDAS = set(MAPA_UF_SIGLA.values())

COMBUSTIVEIS_VALIDOS = {"ETANOL", "DIESEL", "GASOLINA"}

# =========================================================
# ETAPA 3 - RENOMEAÇÃO DAS COLUNAS
# =========================================================

def padronizar_colunas(df):
    """
    Renomeia as colunas para o schema interno padronizado.
    """
    return df.rename(columns=ESQUEMA_ORIGINAL_VENDAS)


# =========================================================
# ETAPA 4 - LIMPEZA TEXTUAL
# =========================================================

def limpar_textos(df):
    """
    Normaliza colunas textuais e converte strings que representam
    ausência de valor em pd.NA.

    Mudança em relação à versão anterior:
    - normalizar_texto() agora retorna pd.NA para strings da lista STRINGS_NULAS
      (ex: "", "NA", "-"). Com keep_default_na=False na leitura, essas strings
      entram como texto e precisam ser convertidas explicitamente aqui.
    """
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
    Converte os campos para tipos adequados.
    Valores inválidos viram pd.NA (via errors="coerce").

    Mudança em relação à versão anterior:
    - id_municipio mantido como string com zero-fill de 7 dígitos,
      não convertido para Int64. Isso evita perda de representação
      e problemas de join futuro no SQL (código IBGE é identificador,
      não um número sobre o qual se faz aritmética).
    """
    # Ano
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")

    # uf -> código IBGE
    df["uf"] = df["uf"].map(MAPA_UF_SIGLA)

    # Código IBGE do município: mantido como string, 7 dígitos, zero à esquerda
    df["id_municipio"] = (
        df["id_municipio"]
        .str.strip()
        .apply(lambda x: x.zfill(7) if pd.notna(x) and x.strip() != "" else pd.NA)
    )

    # Volume de vendas, tratando separadores no padrão brasileiro
    df["volume_vendas_m3"] = (
        df["volume_vendas_m3"]
        .str.strip()
        .str.replace(".", "", regex=False)   # separador de milhar
        .str.replace(",", ".", regex=False)  # decimal brasileiro → ponto
    )
    df["volume_vendas_m3"] = pd.to_numeric(df["volume_vendas_m3"], errors="coerce")

    return df


# =========================================================
# ETAPA 6 - MARCAÇÃO E REMOÇÃO DE LINHAS INVÁLIDAS
# =========================================================

def separar_linhas_invalidas(df, origem=""):
    """
    Separa linhas com ausências nas colunas críticas.
    Elas vão para quarentena antes de serem removidas do fluxo principal.
    """
    n_antes = len(df)
    mask_nulos = df[COLUNAS_CRITICAS_VENDAS].isnull().any(axis=1)
    invalidas = df[mask_nulos].copy()
    salvar_quarentena(invalidas, AUDITORIA_VENDAS, f"linhas_com_nulos_{origem}.csv")
    df = df[~mask_nulos].copy()
    log_etapa(
        "Remoção de nulos críticos", 
        len(df.iloc[:0].pipe(lambda _: pd.concat([invalidas, df]))), 
        len(df), 
        origem
    )
    
    return df


# =========================================================
# ETAPA 7 - VALIDAÇÃO DO id_municipio
# =========================================================

def validar_formato_id_municipio(df, origem=""):
    """
    Verifica se id_municipio tem exatamente 7 dígitos numéricos.
    Linhas fora do formato vão para quarentena.
    """
    n_antes = len(df)
    mask_valido = df["id_municipio"].str.match(r"^\d{7}$", na=False)
    invalidos = df[~mask_valido].copy()
    salvar_quarentena(invalidos, AUDITORIA_VENDAS, f"id_municipio_formato_invalido_{origem}.csv")
    df = df[mask_valido].copy()
    log_etapa(
        "Validação formato id_municipio", 
        len(pd.concat([invalidos, df])), 
        len(df), 
        origem
    )
    return df


# =========================================================
# ETAPA 8 - REGRAS DE DOMÍNIO
# =========================================================

def aplicar_regras_de_dominio(df, origem=""):
    """
    Aplica regras de plausibilidade por coluna.

    Mudança em relação à versão anterior:
    - Faixa de anos restrita a ANO_MIN-ANO_MAX, para capturar erros de digitação
    - Linhas descartadas em cada regra são salvas em quarentena separada
    """
    n_antes = len(df)

    # Ano plausível
    mask_ano = df["ano"].between(ANO_INICIO_ESCOPO_PROJETO, ANO_FIM_ESCOPO_PROJETO)
    salvar_quarentena(df[~mask_ano].copy(), AUDITORIA_VENDAS, f"dominio_ano_invalido_{origem}.csv")
    df = df[mask_ano].copy()

    # uf válida
    mask_uf = df["uf"].isin(UFS_VALIDAS)
    salvar_quarentena(df[~mask_uf].copy(), AUDITORIA_VENDAS, f"dominio_uf_invalida_{origem}.csv")
    df = df[mask_uf].copy()

    # uf dentro do escopo
    mask_escopo = df["uf"].isin(UFS_ESCOPO)
    salvar_quarentena(df[~mask_escopo].copy(), AUDITORIA_VENDAS, f"dominio_uf_fora_escopo_{origem}.csv")
    df = df[mask_escopo].copy()

    # Combustível válido
    mask_comb = df["tipo_combustivel"].isin(COMBUSTIVEIS_VALIDOS)
    salvar_quarentena(df[~mask_comb].copy(), AUDITORIA_VENDAS, f"dominio_combustivel_invalido_{origem}.csv")
    df = df[mask_comb].copy()

    # Volume não pode ser negativo
    mask_vol = df["volume_vendas_m3"] >= 0
    salvar_quarentena(df[~mask_vol].copy(), AUDITORIA_VENDAS, f"dominio_volume_negativo_{origem}.csv")
    df = df[mask_vol].copy()

    log_etapa(
        "Regras de domínio", 
        len(pd.DataFrame(index=range(n_antes))), 
        len(df), 
        origem
    )
    return df


# =========================================================
# ETAPA 9 - DEDUPLICAÇÃO CONSERVADORA
# =========================================================

def tratar_duplicidades(df, origem=""):
    """
    Trata duplicidades de forma conservadora.

    Regra adotada:
    - Duplicata exata (linha inteira repetida): mantém uma ocorrência.
    - Duplicata lógica (mesma chave, valor divergente): vai para quarentena
      e é removida do fluxo principal. Não é somado automaticamente porque
      pode mascarar erro de origem.

    Mudança em relação à versão anterior:
    - Substituído o filtro via MultiIndex (frágil) por duplicated(keep=False),
      que é mais legível e confiável entre versões do pandas.
    """
    chave_logica = ["ano", "uf", "id_municipio", "tipo_combustivel"]
    n_antes = len(df)

    # Duplicatas exatas: salva para auditoria, mantém apenas uma ocorrência
    mask_exatas = df.duplicated(keep=False)
    salvar_quarentena(df[mask_exatas].copy(), AUDITORIA_VENDAS, f"duplicatas_exatas_{origem}.csv")
    df = df.drop_duplicates(keep="first").copy()

    # Duplicatas lógicas: mesma chave de negócio, mas linhas distintas
    # (valores de volume_vendas_m3 diferentes, por exemplo)
    mask_logicas = df.duplicated(subset=chave_logica, keep=False)
    duplicatas_logicas = df[mask_logicas].copy()
    salvar_quarentena(duplicatas_logicas, AUDITORIA_VENDAS, f"duplicatas_logicas_{origem}.csv")
    df = df[~mask_logicas].copy()

    log_etapa(
        "Deduplicação", 
        len(pd.DataFrame(index=range(n_antes))), 
        len(df), 
        origem
    )
    return df


# =========================================================
# ETAPA 10 - VALIDAÇÃO COM A TABELA DO IBGE
# =========================================================

def carregar_ibge(caminho_ibge):
    """
    Carrega a tabela de referência do IBGE.
    Usada para validar se o código do município existe e se a uf bate.

    Mudança em relação à versão anterior:
    - Adicionada validação de schema da planilha do IBGE, similar à feita
      para os arquivos da ANP. Se a planilha mudar de versão, falha cedo.
    """
    df_ibge = pd.read_excel(caminho_ibge, dtype=str, skiprows=6)

    # Validação de schema do arquivo do IBGE
    colunas_esperadas_ibge = {
        "UF",
        "Código Município Completo",
        "Nome_Município",
    }
    colunas_recebidas_ibge = set(df_ibge.columns)
    faltando_ibge = colunas_esperadas_ibge - colunas_recebidas_ibge
    if faltando_ibge:
        raise ValueError(
            f"Schema do arquivo IBGE inválido. Colunas faltando: {sorted(faltando_ibge)}\n"
            f"Colunas recebidas: {sorted(colunas_recebidas_ibge)}"
        )

    df_ibge = df_ibge.rename(columns={
        "UF": "uf",
        "Código Município Completo": "id_municipio",
        "Nome_Município": "nome_municipio_ibge",
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


def validar_com_ibge(df, df_ibge, origem=""):
    """
    Valida uf + ID do município contra a tabela de referência do IBGE.
    Linhas fora da referência vão para quarentena.
    """
    n_antes = len(df)

    chaves_validas = set(zip(df_ibge["uf"], df_ibge["id_municipio"]))
    chaves_df = list(zip(df["uf"], df["id_municipio"]))

    mask_valida = pd.Series([c in chaves_validas for c in chaves_df], index=df.index)

    invalidas = df[~mask_valida].copy()
    salvar_quarentena(invalidas, AUDITORIA_VENDAS, f"linhas_fora_do_ibge_{origem}.csv")
    df = df[mask_valida].copy()

    log_etapa(
        "Validação IBGE", 
        len(pd.DataFrame(index=range(n_antes))), 
        len(df), 
        origem
    )
    return df


# =========================================================
# ETAPA 11 - CONSISTÊNCIA INTERNA
# =========================================================

def validar_consistencia_interna(df, origem=""):
    """
    Valida se um mesmo ID de município aparece associado a múltiplas UFs.
    Isso não deveria acontecer: cada código IBGE pertence a uma única uf.

    Mudança em relação à versão anterior:
    - Salva os casos inconsistentes em quarentena em vez de só printar.
    """
    ufs_por_municipio = df.groupby("id_municipio")["uf"].nunique()
    ids_inconsistentes = ufs_por_municipio[ufs_por_municipio > 1].index

    if not ids_inconsistentes.empty:
        inconsistencias = df[df["id_municipio"].isin(ids_inconsistentes)].copy()
        print(f"  ⚠ [{origem}] {len(ids_inconsistentes)} IDs de município com uf inconsistente.")
        salvar_quarentena(inconsistencias, AUDITORIA_VENDAS, f"inconsistencia_municipio_uf_{origem}.csv")
    else:
        print(f"  ✓ [{origem}] Consistência uf x id_municipio: OK")


# =========================================================
# ETAPA 12 - OUTLIERS (SOMENTE AUDITORIA)
# =========================================================

def identificar_outliers(df, sufixo=""):
    """
    Identifica volumes muito altos para revisão manual.
    Não remove automaticamente — apenas salva em quarentena para análise.

    Mudança em relação à versão anterior:
    - Movido para ser chamado no dataset consolidado (não por arquivo),
      permitindo comparação entre os três combustíveis de forma consistente.
    """
    if df.empty:
        return

    q99 = df["volume_vendas_m3"].quantile(0.99)
    suspeitos = df[df["volume_vendas_m3"] > q99].copy()
    salvar_quarentena(suspeitos, AUDITORIA_VENDAS, f"outliers_acima_p99{sufixo}.csv")
    print(f"  P99 volume_vendas_m3: {q99:,.2f} — {len(suspeitos)} linhas acima desse limiar")


# =========================================================
# ETAPA 13 - PIPELINE COMPLETO DE UM ARQUIVO
# =========================================================

def processar_arquivo(caminho_arquivo, combustivel_fixo, df_ibge):
    """
    Executa o pipeline completo de limpeza de um arquivo individual.
    Cada etapa loga quantas linhas sobreviveram e salva as descartadas em quarentena.
    """
    origem = combustivel_fixo
    print(f"\n{'='*60}")
    print(f"Processando: {caminho_arquivo}  [{origem}]")
    print(f"{'='*60}")

    # Leitura segura com detecção automática de encoding
    df = ler_csv(caminho_arquivo, separador=";")
    print(f"  Linhas lidas: {len(df)}")

    # Adiciona coluna de rastreamento de origem para facilitar auditoria
    # nos arquivos de quarentena. Será removida antes do output final.
    df["_ARQUIVO_ORIGEM"] = combustivel_fixo

    # Validação estrutural do arquivo bruto
    # (após remover BOM dos nomes na leitura)
    validar_esquema(
        df.drop(columns=["_ARQUIVO_ORIGEM"]), 
        ESQUEMA_ORIGINAL_VENDAS,
        origem
    )

    # Padronização de nomes de colunas
    df = padronizar_colunas(df)

    # Limpeza textual (também converte strings nulas em pd.NA)
    df = limpar_textos(df)

    # Conversão de tipos
    df = converter_tipos(df)

    # Remove linhas sem campos essenciais
    df = separar_linhas_invalidas(df, origem)

    # Valida formato do id_municipio (7 dígitos numéricos)
    df = validar_formato_id_municipio(df, origem)

    # Força o combustível fixo do arquivo — evita inconsistência na origem
    df["tipo_combustivel"] = combustivel_fixo

    # Regras de domínio
    df = aplicar_regras_de_dominio(df, origem)

    # Validação com a tabela de referência do IBGE
    df = validar_com_ibge(df, df_ibge, origem)

    # Deduplicação conservadora
    df = tratar_duplicidades(df, origem)

    # Validação interna de consistência uf × id_municipio
    validar_consistencia_interna(df, origem)

    print(f"  ✓ [{origem}] Linhas aprovadas: {len(df)}")
    return df


# =========================================================
# ETAPA 14 - EXECUÇÃO PRINCIPAL
# =========================================================

def main():
    print("Carregando tabela de referência do IBGE...")
    df_ibge = carregar_ibge(ARQUIVO_CODIGOS_IBGE)
    print(f"  IBGE carregado: {len(df_ibge)} municípios de referência\n")

    dfs = []

    for combustivel, arquivo in ARQUIVOS.items():
        df_limpo = processar_arquivo(arquivo, combustivel, df_ibge)
        dfs.append(df_limpo)

    # ── Consolidação ──────────────────────────────────────
    print(f"\n{'='*60}")
    print("Consolidando os 3 arquivos...")
    print(f"{'='*60}")

    df_final = pd.concat(dfs, ignore_index=True)

    # Remove coluna de rastreamento de origem antes do output
    df_final = df_final.drop(columns=["_ARQUIVO_ORIGEM"], errors="ignore")

    # Mantém apenas as colunas finais desejadas
    df_final = df_final.rename(columns=ESQUEMA_VENDAS_ANP)
    df_final = df_final[list(ESQUEMA_VENDAS_ANP.values())].copy()

    # Ordenação determinística
    df_final = df_final.sort_values(
        by=["ano", "uf", "id_municipio", "tipo_combustivel"],
        ignore_index=True,
    )

    # Identificação de outliers no dataset consolidado
    # (feito aqui e não por arquivo para comparar os 3 combustíveis juntos)
    identificar_outliers(df_final, sufixo="_consolidado")

    # Verificação final: não pode sobrar duplicidade lógica no resultado
    chave_final = ["ano", "uf", "id_municipio", "tipo_combustivel"]
    n_dupl_final = df_final.duplicated(subset=chave_final).sum()
    if n_dupl_final > 0:
        raise ValueError(
            f"Duplicidade lógica detectada no dataset final: {n_dupl_final} linhas. "
            f"Verifique os arquivos de quarentena."
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
    print(f"{'='*60}")


if __name__ == "__main__":
    main()