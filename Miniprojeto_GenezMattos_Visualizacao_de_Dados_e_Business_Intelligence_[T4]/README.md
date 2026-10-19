# Mini-Projeto Avaliativo - Módulo 1 - Semana 07
## Visualização de Dados e Business Intelligence [T4]

---

## 📋 1. Contextualização
Este projeto consiste no desenvolvimento de uma **Análise Exploratória de Dados (AED)** aplicada ao setor varejista, utilizando uma base de dados real de compras (`varejo.csv`). O objetivo é aprender e demonstrar na prática como transformar dados brutos em informações acionáveis, verificando a qualidade dos dados, realizando etapas de limpeza, extração de estatísticas descritivas e agrupamentos estratégicos para responder a perguntas operacionais e de negócio.

---

## 🎯 2. O Desafio
Desenvolver um script em Python estruturado e reproduzível que execute as seguintes etapas obrigatórias:
1. **Carregamento e Inspeção:** Importar a base de dados utilizando a biblioteca `pandas`, exibindo o número de registros, colunas e tipos de dados.
2. **Diagnóstico de Problemas:** Identificar e reportar valores nulos por coluna, registros duplicados e inconsistências (ex.: datas inválidas ou categorias vazias).
3. **Limpeza de Dados (ETL Mínimo):** 
   - Tratar valores nulos (explicando as escolhas de imputação ou remoção).
   - Eliminar duplicatas relevantes.
   - Ajustar tipos de dados (ex.: conversão de colunas de data para `datetime`).
4. **Estatísticas Descritivas:** Calcular parâmetros estatísticos fundamentais (média, mediana, desvio padrão, moda, máximo, mínimo e contagem) para a coluna de **número de filhos do cliente**.
5. **Padrões de Agrupamento:** Explorar agrupamentos utilizando `groupby()` ou `pivot_table()` com pelo menos duas combinações relevantes (ex.: vendas por canal, gênero ou região).
6. **Conclusões e Insights:** Apresentar de 3 a 6 tópicos com os principais insights obtidos e eventuais problemas remanescentes na base.

---

## 💻 3. Requisitos Técnicos
- **Linguagem:** Python 3.x
- **Bibliotecas Principais:** `pandas`, `numpy`, `matplotlib` / `seaborn` (opcionais para visualização).
- **Ambiente de Execução:** VS Code ou Google Colab (`.py` ou `.ipynb`).

---

## 🚀 4. Como Executar o Projeto

### Opção 1: Via VS Code (Local)
1. Clone o repositório ou certifique-se de estar na branch `master`.
2. Instale as dependências necessárias executando no terminal:
   `pip install pandas numpy matplotlib seaborn`
3. Execute o script Python correspondente localizado na pasta `script/`:
   `python script/miniprojeto.py`

### Opção 2: Via Google Colab
1. Faça o upload do script ou notebook para o Google Colab.
2. Certifique-se de que o arquivo `varejo.csv` está posicionado na pasta `data/nao_processado/`.
3. Execute todas as células em sequência para reproduzir as análises e gerar os relatórios.

---

## 💡 5. Insights e Conclusões da Análise (3–6 Tópicos)
*(Preencha esta seção após a execução do script com os resultados numéricos obtidos)*

1. **Concentração de Vendas por Canal:** Mapeamento do desempenho relativo entre canais de venda (Loja Física vs. E-commerce) para direcionamento de estratégias comerciais.
2. **Qualidade e Integridade dos Dados:** Identificação de falhas e aplicação de regras de imputação (mediana/moda) para preservar a integridade das análises sem perda excessiva de amostra.
3. **Perfil Demográfico:** Análise da distribuição de filhos dos clientes para apoiar campanhas de segmentação de mercado.
4. **Tendências e Sazonalidade:** Avaliação do comportamento das transações ao longo do tempo após a padronização das datas.
5. **Desafios e Limitações:** Tratamento de inconsistências de formatação e mitigação de vieses durante as etapas de agrupamento.

---

## 📚 6. Reflexão Teórica: ETL e Qualidade de Dados
O processo de Análise Exploratória de Dados reforça a premissa de que grande parte do esforço em projetos de BI e Análise de Dados é dedicada à limpeza e preparação (ETL). Garantir a consistência dos tipos de dados, tratar valores ausentes com critérios fundamentados na regra de negócio (como imputação por grupos) e validar chaves de identificação asseguram que as decisões estratégicas e os dashboards gerados baseiem-se em informações confiáveis.

---
*Autor: Genez José de Mattos Jr. | Turma 4 - SENAI Lab 365*