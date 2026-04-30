# Estratégia de Expansão no Mercado de Combustíveis (Sudeste)

## Cenário

Este projeto simula o contexto de uma distribuidora de combustíveis (fictícia), responsável por adquirir combustíveis de refinarias e revendê-los a postos que atendem o consumidor final.

Nesse cenário, a empresa possui sede em Belo Horizonte (MG), com base operacional na região metropolitana, próxima à REGAP (Refinaria Gabriel Passos), e atuação consolidada em Minas Gerais.

Atualmente, a empresa atende municípios estratégicos de MG:
- Belo Horizonte  
- Contagem  
- Betim  
- Uberlândia  
- Uberaba  
- Juiz de Fora  
- Montes Claros  

Com o crescimento da operação, a empresa busca expandir sua atuação no Sudeste, avaliando o potencial mercado em novos municípios no estado de São Paulo, além de oportunidades ainda não exploradas em Minas Gerais.

---

## Problema de Negócio

Diante da expansão da distribuidora para o Sudeste (MG e SP), quais municípios devem ser priorizados para entrada, considerando potencial de demanda, crescimento de mercado e viabilidade econômica?

---

## Objetivo

Desenvolver uma análise integrada que permita ranquear municípios com maior atratividade para expansão, a partir da combinação de indicadores de consumo de combustíveis, crescimento histórico, perfil da frota e contexto econômico, apoiando a tomada de decisão estratégica.

---

## Fontes de Dados

Os dados foram obtidos a partir de fontes públicas oficiais:

Bases utilizadas:

- **ANP (Agência Nacional do Petróleo)**
  - Vendas de combustíveis por município (gasolina, diesel, etanol)
  - Preços de combustíveis por município e estado

- **IBGE**
  - PIB dos municípios (total, per capita e composição setorial)

- **SENATRAN**
  - Frota de veículos por tipo e município (dados de dezembro de cada ano como proxy anual)

---

## Escopo do Projeto

- Período analisado: **2015 a 2025**
- Região de foco:
  - Minas Gerais (MG)
  - São Paulo (SP)

Observações:
- Dados de PIB disponíveis até 2023 (anos posteriores tratados como ausência ou proxy)
- PIB a preços correntes (não ajustado pela inflação)

---

## Etapas do Projeto

### 1. Coleta de dados em múltiplas fontes  

### 2. Preparação dos dados (Pandas)
  - Leitura de arquivos (CSV/XLS)
  - Limpeza e padronização de colunas (nomes, tipos, unidades)
  - Filtro por período (2015–2025) e região (MG e SP)
  - Exportação dos dados tratados

### 3. Integração e modelagem dos dados (SQL)
  - Criação de tabelas estruturadas
  - Junção das bases (vendas, preços, PIB, frota)
  - Construção da base consolidada por município e ano
  - Criação de métricas derivadas (ex: consumo total, crescimento)

### 4. Análise exploratória (Pandas)
  - Exploração dos dados consolidados
  - Observação de padrões e tendências
  - Identificação de oportunidades e anomalias

### 5. Visualização e comunicação dos resultados
  - Construção de dashboard no Power BI
  - Apresentação de insights e recomendações estratégicas

---

## Modelagem dos Dados

O projeto utiliza uma estrutura integrada por município e ano, combinando:

- Consumo de combustíveis  
- Preços médios (agregados)  
- Indicadores econômicos (PIB)  
- Frota de veículos (total, leves, pesados)  

Essa abordagem permite análises comparativas e construção de indicadores mais robustos de potencial de mercado.

---

## Principais Análises

- Ranking de municípios por volume de consumo  
- Evolução temporal do consumo de combustíveis  
- Identificação de municípios com maior crescimento  
- Comparação entre tipos de combustível (gasolina, etanol, diesel)  
- Análise de consumo ajustado:
  - por habitante  
  - por veículo  
- Relação entre:
  - frota e consumo  
  - PIB e consumo
- Identificação de padrões regionais (MG vs SP)  

---

## Resultados Esperados

- Identificação de municípios com maior potencial de expansão  
- Detecção de mercados emergentes vs saturados  
- Compreensão do perfil de consumo por região  
- Definição de estratégias por tipo de combustível  
- Apoio à tomada de decisão estratégica  

---

## Estrutura do Projeto

- `/dados/brutos`
- `/dados/modificados` → dados tratados e consolidados  
- `/notebooks` → análises exploratórias (Python)  
- `/sql` → consultas e modelagem  
- `/dashboard` → arquivos do Power BI  

---

## Ferramentas Utilizadas

- SQL  
- Python (Pandas)  
- Power BI  

---

## Observações

Este projeto faz parte de um portfólio voltado à análise de dados aplicada a cenários reais de decisão.
