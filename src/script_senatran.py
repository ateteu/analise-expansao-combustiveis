from pathlib import Path
import ibge
import senatran
import utils
import warnings


warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

ENTRADA  = BASE_DIR / "dados/1-brutos/frota-senatran"
SAIDA    = BASE_DIR / "dados/2-intermediarios"
IBGE_XLS = (
    BASE_DIR / 
    "dados/1-brutos/codigos-ibge/RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
)

# ---------------------------------------------------------------------------
# Carrega tabela de referência do IBGE
# ---------------------------------------------------------------------------
df_ibge = ibge.carregar_e_padronizar_codigos(IBGE_XLS)

# ---------------------------------------------------------------------------
# Processa cada arquivo SENATRAN
# ---------------------------------------------------------------------------
arquivos = [
    f for f in ENTRADA.glob("*.xls*")
    if not f.name.startswith(".~lock")
]

dfs = []
for arquivo in arquivos:
    try:
        ano = utils.extrair_ano_do_nome_arquivo(arquivo.name)
        df  = senatran.processar_arquivo(arquivo, ano)
        dfs.append(df)
        print(f"✓ {arquivo.name} ({ano})")
    except Exception as e:
        print(f"✗ {arquivo.name}: {e}")

# ---------------------------------------------------------------------------
# Consolida, enriquece com IBGE e salva
# ---------------------------------------------------------------------------
df_final = utils.concatenar_dfs_e_ordenar(dfs)
df_final = ibge.adicionar_codigo_ibge(df_final, df_ibge)

PRIMEIRAS = [
    "ANO", "UF", 
    "ID_MUNICIPIO", "MUNICIPIO",
    "ID_RG_IMEDIATA", "RG_IMEDIATA",
    "ID_RG_INTERMEDIARIA", "RG_INTERMEDIARIA"
]
df_final = utils.reordenar_colunas(df_final, PRIMEIRAS)

utils.salvar_como_csv(df_final, SAIDA, "frota-senatran.csv")
