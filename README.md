# Estratégia de Expansão de uma Distribuidora de Combustíveis

## Contexto

Este projeto simula o cenário de uma distribuidora de combustíveis (fictícia) regional, de médio-grande porte, com atuação consolidada em Minas Gerais.

A empresa opera com duas bases de distribuição:

- Base principal em Betim (MG), abastecida pela Refinaria Gabriel Passos (REGAP)
- Base secundária em Oliveira (MG), com função de suporte logístico e redução do raio de atendimento

A operação é estruturada ao longo de um eixo logístico principal, utilizando as rodovias BR-381 e BR-262 como corredores de distribuição.

O modelo operacional segue o fluxo:
`Refinaria → Base de distribuição → Postos atendidos`


## Área de Atuação Atual

A empresa possui atuação consolidada nas seguintes regiões:

### Região Intermediária de Belo Horizonte
- Região Imediata de Belo Horizonte: [Belo Horizonte, Contagem, Betim, Mateus Leme, Ribeirão das Neves, Juatuba]

### Região Intermediária de Divinópolis

- Região Imediata de Pará de Minas: [Pará de Minas, Igaratinga]
- Região Imediata de Oliveira: [Itaguara, Carmópolis de Minas, Oliveira]
- Região Imediata de Divinópolis: [Itatiaiuçu, Itaúna, Divinópolis, São Gonçalo do Pará, Nova Serrana]

### Região Intermediária de Varginha

- Região Imediata de Lavras: [Lavras, Santo Antônio do Amparo, Perdões]
- Região Imediata de Três Corações: [Três Corações, Carmo da Cachoeira]
- Região Imediata de Varginha: [Varginha]

Além disso, a empresa atende postos localizados ao longo das rodovias BR-381 e BR-262.


## Problema de Negócio

Com a expansão da área de atuação, a empresa enfrenta aumento da distância média de entrega, elevando os custos logísticos.

O problema central é:

**"Como expandir a malha de distribuição maximizando a cobertura de demanda e minimizando os custos logísticos?"**


## Estrutura do Problema

A decisão de expansão envolve três dimensões:

- Seleção de novos mercados (municípios/regiões)
- Viabilidade logística a partir das bases existentes
- Avaliação da necessidade de criação de uma nova base ou polo logístico

---

## Hipóteses de Expansão

O projeto considera três caminhos estratégicos:

### Hipótese 1 — Expansão contínua no eixo atual (REGAP)

- Manutenção do modelo atual (Betim + Oliveira)
- Expansão ao longo da BR-381 (sentido sul de Minas)
- Avanço para municípios no entorno
- Criação de uma nova base no sul de Minas, atendido via base de Oliveira

### Hipótese 2 — Criação de novo polo logístico (REPLAN)

- Implantação de uma nova base conectada à Refinaria de Paulínia (REPLAN) em SP
- Formação de um segundo eixo logístico independente
- Possibilidade de atendimento eficiente ao Sul de MG e interior de SP (região de Campinas)

### Hipótese 3 — Expansão alternativa dentro de Minas Gerais

- Avaliação de expansão para outras regiões do estado (Ex: oeste ou norte de Minas)
- Comparação de atratividade vs custo logístico

---

## Abordagem Analítica

A análise será estruturada em três etapas, considerando dados no período de 2015 a 2025:

### 1. Potencial de Demanda

Identificação de mercados prioritários com base em:

- Frota de veículos (SENATRAN)
- PIB municipal (IBGE)
- Vendas de combustíveis (ANP)

### 2. Viabilidade Logística

Avaliação da capacidade de atendimento considerando:

- Distância entre bases e municípios
- Eixos rodoviários (BR-381, BR-262)
- Tempo estimado de deslocamento

### 3. Trade-off Custo vs Cobertura

Análise do equilíbrio entre:

- Expansão da área atendida
- Aumento do custo logístico

Objetivos:

- Identificar o limite eficiente de expansão com a estrutura atual
- Avaliar o ponto em que uma nova base se torna viável

---

## Fontes de Dados

Os dados foram obtidos a partir de fontes públicas oficiais:

Bases utilizadas:

- **ANP (Agência Nacional do Petróleo)**
  - Vendas de combustíveis por município (gasolina, diesel, etanol)

- **IBGE (Instituo Brasileiro de Geografia e Estatística)** 
  - PIB dos municípios (total, per capita e composição setorial)
  - Mapas de regiões
  - Códigos dos municípios e regiões

- **SENATRAN (Secretaria Nacional de Trânsito)** 
  - Frota de veículos por tipo e município (dados de dezembro de cada ano como proxy anual)

- **GitHub: kelvins/municípios-brasileiros**
  - Coordenadas geográficas dos municípios brasileiros

## Métricas e Scores Analíticos

O projeto utiliza métricas derivadas para representar demanda, perfil econômico e viabilidade logística dos municípios analisados.

As métricas incluem:

- Volume total de combustíveis vendidos
- Intensidade de consumo por veículo
- Crescimento histórico de vendas e frota
- Participação setorial do VAB municipal
- PIB per capita relativo ao estado
- Distância logística até as bases operacionais

A partir das métricas, são calculados três scores dimensionais:

- `Score de Demanda`: Mede o potencial de consumo e intensidade de mercado.
- `Score Econômico`: Avalia a qualificação econômica dos municípios com base em renda e perfil produtivo.
- `Score Logístico`: Representa a eficiência operacional considerando a distância até a base de atendimento.

Os scores são posteriormente consolidados em um `Score Final` de atratividade do município, para apoiar a decisão de expansão.

---

## Estrutura do Projeto

```text
analise-expansao-combustiveis/
├── dados/
│   ├── 1-brutos/             # Dados originais das fontes
│   ├── 2-intermediarios/     # Dados limpos e padronizados
│   └── banco_dados.duckdb    # Banco de dados local
│
├── sql/
│   ├── 1-metricas/           # Cálculo de métricas
│   ├── 2-pontuacoes/         # Cálculo dos scores
│   └── 3-tabelas-analiticas/ # Consolidação das tabelas finais para análise e BI
│
└── src/
    ├── arquivos/             # Leitura e escrita de arquivos
    ├── bd/                   # Realiza operações ligadas ao BD
    ├── configs/              # Configurações estáticas e mapeamentos
    ├── dominios/             # Regras específicas de cada domínio
    ├── pipelines/            # Fluxos de processamento por fonte de dados
    ├── transformadores/      # Funções reutilizáveis de transformação
    └── main.py               # Ponto de entrada da aplicação
```

## Pipeline de Dados

1. Coleta de dados:
   - Frota (SENATRAN)
   - PIB municipal (IBGE)
   - Vendas e preços (ANP)
   - Coordenadas dos municípios (Rep. Github)

2. Tratamento (Python):
   - Limpeza e padronização
   - Consolidação de séries históricas

3. Modelagem Analítica (SQL | DuckDB):
   - Criação de métricas derivadas
   - Construção de scores dimensionais
   - Consolidação das tabelas analíticas

4. Análise e Visualização:
   - Exploração dos resultados
   - Mapas e indicadores no Power BI
   - Avaliação de cenários de expansão


## Ferramentas Utilizadas

- SQL
- Duck DB
- Python (Pandas)
- Power BI

---

## Como executar

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>

# Criar virtual environment (venv)
python3 -m venv .venv

# Ativar a virtual environment:

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Observações

- Dados de PIB disponíveis até 2023 (anos posteriores tratados como ausência ou proxy)
- PIB a preços correntes (não ajustado pela inflação)
