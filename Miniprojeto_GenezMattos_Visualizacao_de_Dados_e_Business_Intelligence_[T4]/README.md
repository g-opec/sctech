# Mini-Projeto Avaliativo - Módulo 1 - Semana 07
## Visualização de Dados e Business Intelligence [T4]

---

## 📋 1. Contextualização
Este projeto consiste no desenvolvimento de uma **Análise Exploratória de Dados (AED)** aplicada ao setor varejista, utilizando uma base de dados real de compras (`BaseVarejo.csv`). O objetivo é aprender e demonstrar na prática como transformar dados brutos em informações acionáveis, verificando a qualidade dos dados, realizando etapas de limpeza, extração de estatísticas descritivas e agrupamentos estratégicos para responder a perguntas operacionais e de negócio.

---

## 🎯 2. O Desafio
Desenvolver um script em Python estruturado e reproduzível que execute as seguintes etapas obrigatórias:
1. **Carregamento e Inspeção:** Importar a base de dados utilizando a biblioteca `pandas`, exibindo o número de registros, colunas e tipos de dados.
2. **Diagnóstico de Problemas:** Identificar e reportar valores nulos por coluna, registros duplicados e inconsistências estruturais.
3. **Limpeza de Dados (ETL Mínimo):** 
   - Tratar valores nulos (explicando as escolhas de imputação ou remoção).
   - Eliminar duplicatas relevantes e colunas totalmente vazias.
   - Ajustar tipos de dados (ex.: conversão de colunas de data para `datetime`).
4. **Estatísticas Descritivas:** Calcular parâmetros estatísticos fundamentais (média, mediana, desvio padrão, moda, máximo, mínimo e contagem) para a coluna de **número de filhos do cliente**.
5. **Padrões de Agrupamento:** Explorar agrupamentos utilizando `groupby()` e `pivot_table()` para analisar vendas por gênero e categorias de produtos.
6. **Conclusões e Insights:** Apresentar os principais insights obtidos com base nos resultados numéricos consolidados.

---

## 💻 3. Requisitos Técnicos
- **Linguagem:** Python 3.x
- **Bibliotecas Principais:** `pandas`, `numpy`, `pathlib`
- **Ambiente de Execução:** VS Code ou Google Colab (`.py`)

---

## 🚀 4. Como Executar o Projeto

### Opção 1: Via VS Code (Local)
1. Clone o repositório ou certifique-se de estar na branch principal.
2. Instale as dependências necessárias executando no terminal:
   `pip install pandas numpy`
3. Posicione o arquivo `BaseVarejo.csv` na mesma pasta do script ou ajuste os caminhos.
4. Execute o script Python:
   `python MiniProjeto_GenezMattos_T4.py`

### Opção 2: Via Google Colab
1. Faça o upload do script e da base de dados (`BaseVarejo.csv`).
2. Execute todas as células em sequência para reproduzir as análises e gerar os relatórios no console.

---

## 💡 5. Insights e Conclusões da Análise
Com base na execução do script sobre a base de dados (que continha inicialmente 830.000 registros e 14 colunas), destacam-se os seguintes resultados:

1. **Limpeza Estrutural e Duplicatas:** Foram identificadas e removidas **4 colunas totalmente vazias** (`Unnamed: 10` a `13`) e **96.553 linhas exatamente duplicadas**, otimizando a base para 733.447 registros consistentes.
2. **Volume de Itens por Categoria:** A categoria de produtos com maior quantidade de itens/registros na base foi **'ALIMENTOS'**, somando **384.197 ocorrências**, seguida por **'HIGIENE'** (137.702) e **'LIMPEZA'** (128.632).
3. **Comportamento de Compra por Gênero:** O gênero **'F' (Feminino)** lidera o volume de compras com **9.615 transações**, enquanto o gênero **'M' (Masculino)** registrou **8.856 transações**.
4. **Relevância de Categorias em Compras Distintas:** A categoria **'ALIMENTOS'** também lidera o ranking de compras distintas que contêm itens da categoria, totalizando **18.267 compras**, seguida por **'HIGIENE'** (17.610) e **'LIMPEZA'** (17.475).
5. **Perfil Demográfico (Filhos):** A base possui **1.000 clientes únicos**. A média de filhos por cliente é de **1,136** (com desvio padrão de 1,413), mediana igual a **0** e **moda igual a 0** (com valor máximo de 4 filhos por cliente).
6. **Tratamento de Nulos:** As colunas `PR_CAT` e `PR_NOME` apresentavam 3.228 valores ausentes (cerca de 0,44% da base limpa), tratados com sucesso através da aplicação de constante descritiva (`'Sem Categoria'` e `'Produto não informado'`), preservando a integridade do conjunto de dados.

---

## 📚 6. Reflexão Teórica: ETL e Qualidade de Dados

O desenvolvimento deste mini-projeto evidencia que a etapa de **ETL (Extract, Transform, Load)** e a garantia da **Qualidade de Dados** representam a base fundamental para qualquer iniciativa confiável de Business Intelligence (BI) e análise estatística. 

### Pilares Aplicados no Projeto:
* **Extração e Inspeção (Extract):** A importação inicial revelou anomalias estruturais críticas, como colunas de ruído estrutural (`Unnamed`) totalmente vazias e um volume expressivo de registros duplicados (mais de 96 mil linhas). Sem uma inspeção rigorosa prévia, métricas de volume e contagem estariam gravemente distorcidas.
* **Transformação e Limpeza (Transform):** A etapa de tratamento exigiu decisões fundamentadas nas regras de negócio e estatísticas descritivas:
  * *Duplicatas:* A remoção de linhas duplicadas assegurou que as contagens de transações (`co_id`) e clientes (`cl_id`) refletissem a realidade operacional sem inflar o faturamento ou a frequência de compra.
  * *Valores Ausentes (Missing Values):* O tratamento de colunas categóricas nulas (`PR_CAT` e `PR_NOME`) por meio de constantes controladas (`'Sem Categoria'`) evitou a perda arbitrária de milhares de linhas válidas, mantendo a integridade estrutural do DataFrame.
  * *Padronização de Tipos:* A conversão correta da coluna de data para o formato `datetime` permitiu futuras análises temporais consistentes.
* **Confiabilidade para Tomada de Decisão (Load / Analytics):** Com os dados limpos, normalizados e validados através de análises de cardinalidade e dependência funcional (identificação de entidades "pai" como `cl_id`), as agregações via `groupby` e tabelas dinâmicas (`pivot_table`) produziram insights precisos sobre o comportamento de consumo por gênero e categorias de produtos. 

Em suma, o projeto reforça que ferramentas de visualização e algoritmos avançados de BI perdem a validade se alimentados por dados brutos e inconsistentes. O rigor no processo de engenharia e limpeza de dados é o que garante o valor estratégico das conclusões geradas.

---
*Autor: Genez José de Mattos Jr. | Turma 4 - SENAI Lab 365*