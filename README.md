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
  - Preços de combustíveis por município e estado

- **IBGE**
  - PIB dos municípios (total, per capita e composição setorial)
  - Mapas de regiões
  - Códigos dos municípios e regiões

- **SENATRAN**
  - Frota de veículos por tipo e município (dados de dezembro de cada ano como proxy anual)


## Estrutura do Projeto

- `/dados/1-brutos` → dados obtidos nas fontes
- `/dados/2-modificados` → dados tratados
- `/dados/3-modelados` → dados finais para análise
- `/notebooks` → análises exploratórias (Python)
- `/sql` → consultas e modelagem
- `/src` → scripts de tratamento de dados
- `/dashboard` → arquivos do Power BI


## Pipeline de Dados

1. Coleta de dados
   - Frota (SENATRAN)
   - PIB municipal (IBGE)
   - Vendas e preços (ANP)

2. Tratamento (Python)
   - Limpeza e padronização
   - Consolidação de séries históricas

3. Modelagem (SQL)
   - Filtros por região e período
   - Agregações
   - Construção de tabelas analíticas

4. Análise (Python)
   - Exploração de padrões
   - Criação de métricas

5. Visualização (Power BI)
   - Mapas geográficos
   - Indicadores de demanda
   - Análise logística


## Ferramentas Utilizadas

- SQL
- Python (Pandas)
- Power BI

---

## Observações

- Dados de PIB disponíveis até 2023 (anos posteriores tratados como ausência ou proxy)
- PIB a preços correntes (não ajustado pela inflação)