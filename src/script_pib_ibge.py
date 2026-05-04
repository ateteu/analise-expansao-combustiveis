from pathlib import Path
import warnings

import pandas as pd

import utils

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

ENTRADA = BASE_DIR / "dados/1-brutos/pib-ibge/PIB dos Municipios - base de dados 2010-2023.xlsx"
SAIDA   = BASE_DIR / "dados/2-intermediarios"

# ---------------------------------------------------------------------------
# Colunas a manter e seus nomes padronizados
# ---------------------------------------------------------------------------
COLUNAS_UTEIS = {
    "Ano"                                                  : "ANO",
    "Sigla da Unidade da Federação"                        : "UF",
    "Código do Município"                                  : "ID_MUNICIPIO",
    "Nome do Município"                                    : "MUNICIPIO",
    "Código da Região Geográfica Imediata"                 : "ID_RG_IMEDIATA",
    "Nome da Região Geográfica Imediata"                   : "RG_IMEDIATA",
    "Código da Região Geográfica Intermediária"            : "ID_RG_INTERMEDIARIA",
    "Nome da Região Geográfica Intermediária"              : "RG_INTERMEDIARIA",

    "Valor adicionado bruto da Agropecuária, " \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_AGROPECUARIA",

    "Valor adicionado bruto da Indústria,"     \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_INDUSTRIA",

    "Valor adicionado bruto dos Serviços,"              \
    "\na preços correntes \n"                           \
    "- exceto Administração, defesa, educação e saúde " \
    "públicas e seguridade social\n(R$ 1.000)"             : "VAB_SERVICOS",
    
    "Valor adicionado bruto da Administração, " \
    "defesa, educação e saúde públicas e "      \
    "seguridade social, \na preços correntes\n(R$ 1.000)"  : "VAB_ADMINISTRACAO_PUBLICA",

    "Valor adicionado bruto total, "     \
    "\na preços correntes\n(R$ 1.000)"                     : "VAB_TOTAL",

    "Produto Interno Bruto, "            \
    "\na preços correntes\n(R$ 1.000)"                     : "PIB",

    "Produto Interno Bruto per capita, " \
    "\na preços correntes\n(R$ 1,00)"                      : "PIB_PER_CAPITA",

    "Atividade com maior valor adicionado bruto"           : "ATIVIDADE_1",
    "Atividade com segundo maior valor adicionado bruto"   : "ATIVIDADE_2",
    "Atividade com terceiro maior valor adicionado bruto"  : "ATIVIDADE_3",
}


# ---------------------------------------------------------------------------
# Funções
# ---------------------------------------------------------------------------
def ler_e_selecionar(caminho: Path) -> pd.DataFrame:
    df = pd.read_excel(caminho, engine="openpyxl")

    colunas_presentes = [c for c in COLUNAS_UTEIS if c in df.columns]
    colunas_ausentes  = [c for c in COLUNAS_UTEIS if c not in df.columns]

    if colunas_ausentes:
        print(f"⚠️  {len(colunas_ausentes)} coluna(s) não encontrada(s) no arquivo:")
        for c in colunas_ausentes:
            print(f"   - {c}")

    return df[colunas_presentes].rename(columns=COLUNAS_UTEIS)


def padronizar(df: pd.DataFrame) -> pd.DataFrame:
    # Textos
    df["MUNICIPIO"]       = df["MUNICIPIO"].apply(utils.normalizar_texto)
    df["UF"]              = df["UF"].str.strip().str.upper()
    df["RG_IMEDIATA"]     = df["RG_IMEDIATA"].apply(utils.normalizar_texto)
    df["RG_INTERMEDIARIA"]= df["RG_INTERMEDIARIA"].apply(utils.normalizar_texto)

    colunas_atividade = ["ATIVIDADE_1", "ATIVIDADE_2", "ATIVIDADE_3"]
    for col in colunas_atividade:
        if col in df.columns:
            df[col] = df[col].apply(utils.normalizar_texto)

    # IDs como string
    for col in ["ID_MUNICIPIO", "ID_RG_IMEDIATA", "ID_RG_INTERMEDIARIA"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Numéricos
    df["ANO"] = pd.to_numeric(df["ANO"], errors="coerce").astype("Int64")

    for col in [
            "VAB_AGROPECUARIA", "VAB_INDUSTRIA", "VAB_SERVICOS",
            "VAB_ADMINISTRACAO_PUBLICA", "VAB_TOTAL", 
            "PIB", "PIB_PER_CAPITA"
        ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
try:
    print("\nLendo arquivo...\n")
    df = ler_e_selecionar(ENTRADA)

    print("\nPadronizando...\n")
    df = padronizar(df)

    df = df.sort_values(["ANO", "UF", "MUNICIPIO"])
    utils.salvar_como_csv(df, SAIDA, "pib-ibge.csv")

except Exception as e:
    print(f"Erro ao processar arquivo: {e}")
