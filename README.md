# Estratégia de Expansão no Mercado de Combustíveis (Sudeste)

## Visão Geral

Este projeto simula um cenário real de negócio no qual uma distribuidora de combustíveis, com origem em Belo Horizonte (MG) e atuação consolidada em Minas Gerais, busca expandir suas operações no estado de São Paulo.

A análise utiliza dados públicos para entender o comportamento do mercado de combustíveis em nível municipal, com o objetivo de identificar regiões com maior potencial de crescimento e retorno.

O foco do projeto é transformar dados em insights estratégicos, considerando fatores como demanda, crescimento, perfil econômico e características da frota de veículos.

---

## Problema de Negócio

Quais municípios apresentam maior potencial para expansão, considerando:

- volume de consumo de combustíveis  
- crescimento ao longo do tempo  
- perfil de consumo por tipo de combustível  
- características da frota de veículos  
- contexto econômico local  

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
  - Frota de veículos por município (dados de dezembro de cada ano como proxy anual)

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

- Coleta de dados em múltiplas fontes  
- Padronização e limpeza das bases  
- Integração dos dados por município e ano  
- Criação de métricas derivadas:
  - consumo total  
  - crescimento  
  - consumo per capita  
  - consumo por veículo  
- Análise exploratória dos dados  
- Geração de insights estratégicos  
- Construção de dashboard (Power BI)  

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
