"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Disciplina: Visualização de Dados e Business Intelligence [T4]
Aluno: Genez Jose de Mattos

Objetivo:
 Identificar problemas nos dados (valores nulos, tipos incorretos, duplicados), 
 tratar esses problemas com ferramentas como pandas e gerar estatísticas simples e 
 funções de agrupamento, para responder perguntas operacionais 
 (quem compra mais, quais categorias vendem mais, como variam as vendas ao longo do tempo).


Execução:
    python MiniProjeto_GenezMattos_T4.py

Dependência:
    pandas
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Função auxiliar para formatar números inteiros com separador de milhar-------------------------
def fmt_int(valor):
    return f"{int(valor):,}".replace(",", ".")


# Função generica para limpar linhas e colunas vazias do DataFrame-------------------------------
def limpar_dados(df):
  """Recebe um DataFrame e executa a limpeza estrutural inicial:
  - Remove colunas 100% vazias.
  - Remove linhas 100% vazias.
  Retorna o DataFrame limpo.
  """
  # Cria uma cópia para evitar modificar o DataFrame original diretamente
  df_clean = df.copy()

  print(
      f"Dimensões antes da limpeza: {df_clean.shape[0]} linhas,"
      f" {df_clean.shape[1]} colunas."
  )

  # 1. Identifica e remove colunas totalmente vazias
  colunas_vazias = [
      col for col in df_clean.columns if df_clean[col].isna().all()
  ]

  if colunas_vazias:
    print(f"Removendo {len(colunas_vazias)} coluna(s) totalmente vazia(s):")
    for coluna in colunas_vazias:
      print(f" - {coluna}")
    df_clean = df_clean.drop(columns=colunas_vazias)
  else:
    print("Nenhuma coluna 100% vazia encontrada.")

  # 2. Remove linhas totalmente vazias
  linhas_antes = len(df_clean)
  df_clean = df_clean.dropna(how="all")
  linhas_removidas = linhas_antes - len(df_clean)

  if linhas_removidas > 0:
    print(f"Removidas {linhas_removidas} linha(s) totalmente vazia(s).")
  else:
    print("Nenhuma linha 100% vazia encontrada.")

   # 3. Remove linhas duplicadas
  linhas_duplicadas = df_clean.duplicated().sum()
  print(f"Quantidade de linhas duplicadas: {linhas_duplicadas}")
  if linhas_duplicadas > 0:
      print(f"Removendo {linhas_duplicadas} linha(s) duplicada(s).") 
      df_clean = df_clean.drop_duplicates()

  print(
      f"Dimensões após a limpeza: {df_clean.shape[0]} linhas,"
      f" {df_clean.shape[1]} colunas.\n"
  )
  return df_clean


# Função para gerar relatório de valores ausentes------------------------------------------------
def relatorio_valores_ausentes(df):
  """Exibe um relatório detalhado com a quantidade e a porcentagem

  de valores ausentes (NaN) em cada coluna do DataFrame.
  """
  total_linhas = len(df)
  qtd_ausentes = df.isna().sum()
  pct_ausentes = (qtd_ausentes / total_linhas) * 100

  # Cria um DataFrame de resumo
  resumo = pd.DataFrame(
      {"Qtd_Ausentes": qtd_ausentes, "%_Ausentes": pct_ausentes}
  )

  # Filtra apenas colunas que possuem pelo menos 1 ausente e ordena da maior para menor %
  resumo_filtrado = resumo[resumo["Qtd_Ausentes"] > 0].sort_values(
      by="%_Ausentes", ascending=False
  )

  print(f"Total de linhas na base: {total_linhas}")
  if not resumo_filtrado.empty:
    print("\nColunas com valores ausentes:")
    print(resumo_filtrado.to_string())
  else:
    print("\nParabéns! Nenhuma coluna possui valores ausentes.")

  return resumo


# Função para padronizar placeholders nulos----------------------------------------------------
def padronizar_placeholders_nulos(df):
  """Converte strings que representam erros/ausência (como '#N/D', 'NULL', 'NA', '')

  em valores NaN reais do Pandas, permitindo que a normalização de tipos funcione.
  """
  df_padrao = df.copy()
  termos_nulos = ["#n/d", "#n/a", "n/d", "n/a", "na", "null", "none", ""]

  for col in df_padrao.columns:
    if df_padrao[col].dtype == "object":
      # Converte para string, remove espaços extras e joga para minúsculo para comparar
      serie_str = df_padrao[col].astype(str).str.strip().str.lower()
      # Substitui os termos da lista por np.nan
      df_padrao[col] = serie_str.replace(termos_nulos, np.nan)

  return df_padrao

# Função para tratar valores ausentes em uma coluna específica--------------------------------
def tratar_ausentes(
    df, coluna, estrategia="constante", valor_constante="desconhecido"
):
  """Trata valores ausentes em uma coluna específica com base na estratégia escolhida:

  - 'mediana': preenche com a mediana (para colunas numéricas)
  - 'moda': preenche com o valor mais frequente
  - 'temporal': preenche usando forward fill / backward fill (para datas/séries)
  - 'constante': preenche com um valor fixo (ex: 'desconhecido' ou 0)
  """
  df_tratado = df.copy()

  if coluna not in df_tratado.columns:
    print(f"Aviso: Coluna '{coluna}' não foi encontrada no DataFrame.")
    return df_tratado

  nulos_antes = df_tratado[coluna].isna().sum()
  if nulos_antes == 0:
    print(f"A coluna '{coluna}' não possui valores ausentes para tratar.")
    return df_tratado

  if estrategia == "mediana":
    if pd.api.types.is_numeric_dtype(df_tratado[coluna]):
      val = df_tratado[coluna].median()
      df_tratado[coluna] = df_tratado[coluna].fillna(val)
      print(f"Coluna '{coluna}': {nulos_antes} nulos preenchidos pela mediana ({val}).")
    else:
      print(f"Erro: Coluna '{coluna}' não é numérica para calcular mediana.")

  elif estrategia == "moda":
    val = df_tratado[coluna].mode()[0]
    df_tratado[coluna] = df_tratado[coluna].fillna(val)
    print(f"Coluna '{coluna}': {nulos_antes} nulos preenchidos pela moda ({val}).")

  elif estrategia == "temporal":
    # Propaga o último valor válido para frente e depois para trás
    df_tratado[coluna] = df_tratado[coluna].ffill().bfill()
    print(f"Coluna '{coluna}': {nulos_antes} nulos tratados via preenchimento temporal.")

  elif estrategia == "constante":
    df_tratado[coluna] = df_tratado[coluna].fillna(valor_constante)
    print(f"Coluna '{coluna}': {nulos_antes} nulos preenchidos com a constante '{valor_constante}'.")

  return df_tratado


# Função para normalizar os dados do DataFrame-----------------------------------------------------
def normalizar_dados(df):
  """Recebe um DataFrame e executa a normalização completa:

  - Padroniza os nomes das colunas (minúsculas, sem espaços, underscores).
  - Remove espaços em branco de strings.
  - Identifica e converte colunas numéricas (trata R$, pontos de milhar e vírgulas decimais).
  - Identifica e converte colunas de data usando um dicionário de formatos conhecidos.
  Retorna o DataFrame normalizado.
  """
  df_norm = df.copy()

  print("Iniciando a normalização dos dados...")

  # 1. Normalizar nomes das colunas
  df_norm.columns = (
      df_norm.columns.str.strip().str.lower().str.replace(" ", "_")
  )

  # 2. Normalizar colunas de texto (string) básicas
  colunas_texto = df_norm.select_dtypes(include=["object", "string"]).columns
  for col in colunas_texto:
    df_norm[col] = df_norm[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

  # 3. Tratamento de colunas numéricas mascaradas como texto (ex: valores monetários)
  print("Verificando e limpando colunas numéricas...")
  for col in df_norm.columns:
    if df_norm[col].dtype == "object":
      amostra = df_norm[col].dropna()
      amostra_str = amostra[amostra.apply(lambda x: isinstance(x, str))]

      if len(amostra_str) > 0:
        # Simula a limpeza do padrão monetário/numérico brasileiro (R$, pontos e vírgulas)
        teste_limpeza = (
            amostra_str.str.replace("R$", "", regex=False)
            .str.replace(" ", "")
            .str.replace(".", "", regex=False)  # Remove ponto de milhar
            .str.replace(
                ",", ".", regex=False
            )  # Troca vírgula decimal por ponto
        )

        try:
          convertido = pd.to_numeric(teste_limpeza, errors="coerce")
          # Se mais de 80% da amostra se converteu com sucesso em número
          if convertido.notna().sum() / len(amostra_str) > 0.8:
            df_norm[col] = (
                df_norm[col]
                .astype(str)
                .str.replace("R$", "", regex=False)
                .str.replace(" ", "")
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df_norm[col] = pd.to_numeric(df_norm[col], errors="coerce")
            print(f" - Coluna '{col}' convertida para numérica com sucesso.")
        except Exception:
          pass

  # 4. Dicionário de formatos de data conhecidos
  formatos_data = {
      "dd/mm/aaaa": "%d/%m/%Y",
      "dd/mm/aa": "%d/%m/%y",
      "aaaa-mm-dd": "%Y-%m-%d",
      "aa-mm-dd": "%y-%m-%d",
      "dd-mm-aaaa": "%d-%m-%Y",
      "dd-mm-aa": "%d-%m-%y",
      "mm/dd/aaaa": "%m/%d/%Y",
      "mm/dd/aa": "%m/%d/%y",
      "dd.mm.aaaa": "%d.%m.%Y",
  }

  # Atualiza a lista de colunas de texto após conversões numéricas eventuais
  colunas_texto = df_norm.select_dtypes(include=["object", "string"]).columns

  print("Analisando e convertendo colunas de data...")
  for col in colunas_texto:
    amostra = df_norm[col].dropna()
    # Filtra APENAS valores que são strings para evitar erros de tipo no formato
    amostra_str = amostra[amostra.apply(lambda x: isinstance(x, str))]

    if len(amostra_str) == 0:
      continue

    convertido_com_sucesso = False
    for desc_formato, formato_str in formatos_data.items():
      try:
        convertido = pd.to_datetime(
            amostra_str, format=formato_str, errors="coerce"
        )
        taxa_sucesso = convertido.notna().sum() / len(amostra_str)

        if taxa_sucesso > 0.8:
          df_norm[col] = pd.to_datetime(
              df_norm[col], format=formato_str, errors="coerce"
          )
          print(
              f" - Coluna '{col}' convertida para datetime usando o formato"
              f" '{desc_formato}'."
          )
          convertido_com_sucesso = True
          break
      except Exception:
        continue

    # Fallback genérico caso nenhum formato rígido bata
    if not convertido_com_sucesso:
      try:
        convertido_geral = pd.to_datetime(amostra_str, errors="coerce")
        if convertido_geral.notna().sum() / len(amostra_str) > 0.8:
          df_norm[col] = pd.to_datetime(df_norm[col], errors="coerce")
          print(
              f" - Coluna '{col}' convertida para datetime usando inferência"
              " padrão."
          )
      except Exception:
        pass

  print("Normalização concluída com sucesso!")
  return df_norm

# ---------------------------------------------------------------------
# 1. LOCALIZAÇÃO E LEITURA DO ARQUIVO (ONLINE OU OFFLINE)
# ---------------------------------------------------------------------

folderScript = Path(__file__).resolve().parent

# Aceita os dois nomes mais prováveis para facilitar a execução.
arquivos_candidatos = [
    folderScript / "Base Varejo.csv",
    folderScript / "BaseVarejo.csv",
    folderScript / "Varejo.csv"
]

# Tenta localizar o arquivo CSV localmente
arquivo_csv_local = next((p for p in arquivos_candidatos if p.exists()), None)

# URL do arquivo CSV hospedado no GitHub  
file_url = "https://raw.githubusercontent.com/g-opec/sctech/refs/heads/master/Miniprojeto_GenezMattos_Visualizacao_de_Dados_e_Business_Intelligence_%5BT4%5D/data/nao_processado/BaseVarejo.csv"

print("\n" + "=" * 72)

# Se o arquivo foi encontrado localmente, lê do disco
if arquivo_csv_local is not None:
    print(f"Arquivo local encontrado: {arquivo_csv_local.name}. Carregando...")
    df = pd.read_csv(arquivo_csv_local, sep=";", encoding="utf-8")
    print("Sucesso! O DataFrame local foi carregado corretamente.")

# Se não foi encontrado localmente, tenta ler diretamente da URL do GitHub
else:
    print("Arquivo CSV não foi encontrado localmente. Tentando ler diretamente da URL do GitHub...")
    print("=" * 72)
    try:
        df = pd.read_csv(file_url, sep=";", encoding="utf-8")
        print("Sucesso! O DataFrame foi carregado corretamente da URL do GitHub.")
    except Exception as e:
        print("Falha ao carregar o arquivo.")
        print("Verifique se a URL está correta, se o repositório é público ou se o arquivo existe.")
        print(f"Detalhes técnicos do erro: {e}")

csv_name = arquivo_csv_local.name if arquivo_csv_local else "erro"  

print("=" * 72)
print("1. ESTRUTURA INICIAL DO DATAFRAME")
print("=" * 72)
print(f"Arquivo: {csv_name}")
print(f"Número de registros: {fmt_int(len(df))}")
print(f"Número de colunas: {df.shape[1]}")
print("\nColunas:")
for coluna in df.columns:
    print(f" - {coluna}")

print("\nTipos de dados iniciais:")
print(df.dtypes)

# ---------------------------------------------------------------------
# 2. DIAGNÓSTICO DE QUALIDADE
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("2. DIAGNÓSTICO DE QUALIDADE")
print("=" * 72)

print("\nValores nulos por coluna:")
print(df.isna().sum())
print("\n" + "=" * 72)

# Conta quantas linhas têm 100% dos valores nulos
qtd_linhas_totalmente_vazias = df.isna().all(axis=1).sum()

print(f"Quantidade de linhas 100% vazias: {qtd_linhas_totalmente_vazias}")
print("=" * 72)

# 1. Chamando a função de limpeza strutural inicial (remove colunas e linhas totalmente vazias)
df_clean = limpar_dados(df)

# 2. converte textos de erro ("#N/D", "NULL") em NaN reais
df_com_nulos_reais = padronizar_placeholders_nulos(df_clean)

# 3. chamando a função do relatório para inspecionar os ausentes antes de tratar
relatorio_valores_ausentes(df_com_nulos_reais)

# 4. função para tratar colunas específicas conforme análise do relatório
df_com_nulos_reais = tratar_ausentes(df_com_nulos_reais, coluna="PR_CAT", estrategia="constante", valor_constante="Sem Categoria")
df_com_nulos_reais = tratar_ausentes(df_com_nulos_reais, coluna="PR_NOME", estrategia="constante", valor_constante="Produto não informado")

# caso fosse necessário tratar a coluna de valores monetários, poderia ser feito assim:
#df_tratado = tratar_ausentes(df_com_nulos_reais, coluna="valor_venda", estrategia="mediana")

# caso fosse necessario tratar a coluna de datas, poderia ser feito assim:
#df_tratado = tratar_ausentes(df_com_nulos_reais, coluna="DATA", estrategia="temporal")

### só substituindo o df_com_nulos_reais pelo df_tratado se houver necessidade de tratar mais colunas
df_tratado = df_com_nulos_reais.copy()

# 5. chamando a função de normalização de dataframe
df_normalized = normalizar_dados(df_tratado)

# 6. chamando a função do relatório para confirmar que não há mais ausentes após o tratamento e normalização
relatorio_valores_ausentes(df_normalized)

print("\n")

# Exibe as primeiras linhas para validação
#print(df.head())
#print(df_clean.head())
print(df_normalized.head())

