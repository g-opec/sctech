"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Disciplina: Visualização de Dados e Business Intelligence [T4]
Aluno: Genez José de Mattos Junior

Objetivo:
 Identificar problemas nos dados (valores nulos, tipos incorretos, duplicados), 
 tratar esses problemas com ferramentas como pandas e gerar estatísticas simples e 
 funções de agrupamento, para responder perguntas operacionais 
 (quem compra mais, quais categorias vendem mais, como variam as vendas ao longo do tempo).


Execução:
    python MiniProjeto_GenezMattos_T4.py

Dependência:
    pathlib
    pandas
    numpy
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Funções basicas e genericas para tratamento e análise de dados em qualquer DataFrame----
#
# Função auxiliar para formatar números inteiros com separador de milhar------------------
def fmt_int(valor):
    return f"{int(valor):,}".replace(",", ".")


# Função generica para limpar linhas e colunas vazias e linhas duplicadas do DataFrame----
def limpar_dados(df):
  """Recebe um DataFrame e executa a limpeza estrutural inicial:
  - Remove colunas 100% vazias.
  - Remove linhas 100% vazias.
  - Remove linhas duplicadas.
  Retorna o DataFrame limpo e a quantidade de duplicadas.
  """
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
  return df_clean, linhas_duplicadas


# Função para gerar relatório de valores ausentes-----------------------------------------
def relatorio_valores_ausentes(df):
  """Exibe um relatório detalhado com a quantidade e a porcentagem
  de valores ausentes (NaN) em cada coluna do DataFrame.
  """
  total_linhas = len(df)
  qtd_ausentes = df.isna().sum()
  pct_ausentes = (qtd_ausentes / total_linhas) * 100

  resumo = pd.DataFrame(
      {"Qtd_Ausentes": qtd_ausentes, "%_Ausentes": pct_ausentes}
  )

  resumo_filtrado = resumo[resumo["Qtd_Ausentes"] > 0].sort_values(
      by="%_Ausentes", ascending=False
  )

  print(f"Total de linhas na base: {total_linhas}")
  if not resumo_filtrado.empty:
    print("\nColunas com valores ausentes:")
    print(resumo_filtrado.to_string())
  else:
    print("\nNenhuma coluna possui valores ausentes.")

  return resumo


# Função para padronizar placeholders nulos-----------------------------------------------
def padronizar_placeholders_nulos(df):
  """Converte strings que representam erros/ausência (como '#N/D', 'NULL', 'NA', '')
  em valores NaN reais do Pandas, sem corromper os nulos já existentes.
  """
  df_padrao = df.copy()
  termos_nulos = ["#n/d", "#n/a", "n/d", "n/a", "na", "null", "none", ""]

  for col in df_padrao.columns:
    if df_padrao[col].dtype == "object":
      # Cria uma máscara para encontrar os termos nulos ignorando maiúsculas e espaços
      serie_str = df_padrao[col].astype(str).str.strip().str.lower()
      mask = serie_str.isin(termos_nulos)
      
      # Substitui apenas os encontrados por np.nan real
      df_padrao.loc[mask, col] = np.nan

  return df_padrao

# Função para tratar valores ausentes em uma coluna específica----------------------------
def tratar_ausentes(
    df, coluna, estrategia="constante", valor_constante="desconhecido"
):
  """Trata valores ausentes em uma coluna específica com base na estratégia escolhida."""
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
    df_tratado[coluna] = df_tratado[coluna].ffill().bfill()
    print(f"Coluna '{coluna}': {nulos_antes} nulos tratados via preenchimento temporal.")

  elif estrategia == "constante":
    df_tratado[coluna] = df_tratado[coluna].fillna(valor_constante)
    print(f"Coluna '{coluna}': {nulos_antes} nulos preenchidos com a constante '{valor_constante}'.")

  return df_tratado


# Função para normalizar os dados do DataFrame--------------------------------------------
def normalizar_dados(df):
  """Recebe um DataFrame e executa a normalização completa."""
  df_norm = df.copy()

  print("Iniciando a normalização dos dados...")

  df_norm.columns = (
      df_norm.columns.str.strip().str.lower().str.replace(" ", "_")
  )

  colunas_texto = df_norm.select_dtypes(include=["object", "string"]).columns
  for col in colunas_texto:
    df_norm[col] = df_norm[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

  print("Verificando e limpando colunas numéricas...")
  for col in df_norm.columns:
    if df_norm[col].dtype == "object":
      amostra = df_norm[col].dropna()
      amostra_str = amostra[amostra.apply(lambda x: isinstance(x, str))]

      if len(amostra_str) > 0:
        teste_limpeza = (
            amostra_str.str.replace("R$", "", regex=False)
            .str.replace(" ", "")
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        try:
          convertido = pd.to_numeric(teste_limpeza, errors="coerce")
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

  colunas_texto = df_norm.select_dtypes(include=["object", "string"]).columns

  print("Analisando e convertendo colunas de data...")
  for col in colunas_texto:
    amostra = df_norm[col].dropna()
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

    if not convertido_com_sucesso:
      try:
        convertido_geral = pd.to_datetime(amostra_str, format='mixed', errors="coerce")
        if convertido_geral.notna().sum() / len(amostra_str) > 0.8:
          df_norm[col] = pd.to_datetime(df_norm[col], format='mixed', errors="coerce")
          print(
              f" - Coluna '{col}' convertida para datetime usando inferência"
              " padrão."
          )
      except Exception:
        pass

  print("Normalização concluída com sucesso!")
  return df_norm

# Função para identificar dados repetidos que podem ser pais prováveis no DataFrame-------
def relatorio_colunas_pai(df):
  """Analisa um DataFrame para identificar prováveis colunas 'pai'."""
  n_linhas = len(df)
  relatorio = []

  for col in df.columns:
    n_unicos = df[col].nunique()
    taxa_unicidade = (n_unicos / n_linhas) * 100
    media_repeticao = n_linhas / n_unicos if n_unicos > 0 else 0

    atributos_dependentes = 0
    if 1 < n_unicos < n_linhas:
      for outra_col in df.columns:
        if outra_col == col:
          continue
        if df.groupby(col)[outra_col].nunique().max() == 1:
          atributos_dependentes += 1

    relatorio.append({
        "coluna": col,
        "n_unicos": n_unicos,
        "unicidade_pct": round(taxa_unicidade, 2),
        "media_linhas_por_pai": round(media_repeticao, 2),
        "atributos_dependentes": atributos_dependentes,
    })

  df_resultado = pd.DataFrame(relatorio)
  df_resultado = df_resultado.sort_values(
      by=["atributos_dependentes", "unicidade_pct"], ascending=[False, True]
  )

  return df_resultado.reset_index(drop=True)


# Função para analisar estatísticas de métricas agrupadas por entidade pai----------------
def analisar_estatisticas_pai(df, col_pai, col_metrica=None):
  """Isola as entidades pai únicas e gera estatísticas automáticas."""
  df_pai = df.drop_duplicates(subset=[col_pai])

  if col_metrica is not None:
    if col_metrica not in df.columns:
      raise ValueError(f"A coluna '{col_metrica}' não existe no DataFrame.")
    colunas_metricas = [col_metrica]
  else:
    colunas_metricas = df_pai.select_dtypes(
        include=["number", "int64", "float64"]
    ).columns.tolist()
    if col_pai in colunas_metricas:
      colunas_metricas.remove(col_pai)

  resultados = {}

  print(f"=== Relatório Estatístico dos Filhos por Pai: '{col_pai}' ===")
  print(
      f"Total de entidades pai únicas ({col_pai}):"
      f" {fmt_int(len(df_pai))}\n"
  )

  for col in colunas_metricas:
    filhos = df_pai[col]

    moda_vals = filhos.mode()
    total_unicos = filhos.nunique()

    if len(moda_vals) > 10 or (
        total_unicos > 0 and len(moda_vals) > (total_unicos * 0.5)
    ):
      str_moda = "N/A (Alta dispersão / Sem moda clara)"
    else:
      str_moda = ", ".join(map(str, moda_vals.tolist()))

    contagem = filhos.count()
    media = filhos.mean() if contagem > 0 else 0
    mediana = filhos.median() if contagem > 0 else 0
    desvio_padrao = filhos.std() if contagem > 1 else 0
    maximo = filhos.max() if contagem > 0 else 0
    minimo = filhos.min() if contagem > 0 else 0

    print(f"--- Métrica: {col} ---")
    print(f"Contagem:       {fmt_int(contagem)}")
    print(f"Média:          {media:.3f}")
    print(f"Mediana:        {mediana:.3f}")
    print(
        f"Desvio padrão:  {desvio_padrao:.3f}"
        if pd.notna(desvio_padrao)
        else "Desvio padrão:  0.000"
    )
    print(f"Moda:           {str_moda}")
    print(f"Máximo:         {maximo}")
    print(f"Mínimo:         {minimo}\n")

    resultados[col] = {
        "contagem": contagem,
        "media": media,
        "mediana": mediana,
        "std": desvio_padrao,
        "moda": moda_vals.tolist(),
        "max": maximo,
        "min": minimo,
    }

  return resultados

# ---------------------------------------------------------------------
# 1. LOCALIZAÇÃO E LEITURA DO ARQUIVO (ONLINE OU OFFLINE)
# ---------------------------------------------------------------------

folderScript = Path(__file__).resolve().parent

arquivos_candidatos = [
    folderScript / "Base Varejo.csv",
    folderScript / "BaseVarejo.csv",
    folderScript / "Varejo.csv"
]

arquivo_csv_local = next((p for p in arquivos_candidatos if p.exists()), None)
file_url = "https://raw.githubusercontent.com/g-opec/sctech/refs/heads/master/Miniprojeto_GenezMattos_Visualizacao_de_Dados_e_Business_Intelligence_%5BT4%5D/data/nao_processado/BaseVarejo.csv"

print("\n" + "=" * 72)

if arquivo_csv_local is not None:
    print(f"Arquivo local encontrado: {arquivo_csv_local.name}. Carregando...")
    df = pd.read_csv(arquivo_csv_local, sep=";", encoding="utf-8", na_values=["#N/D", "#n/d", "NULL", "NA", ""])
    print("Sucesso! O DataFrame local foi carregado corretamente.")
else:
    print("Arquivo CSV não foi encontrado localmente. Tentando ler diretamente da URL do GitHub...")
    print("=" * 72)
    try:
        df = pd.read_csv(file_url, sep=";", encoding="utf-8", na_values=["#N/D", "#n/d", "NULL", "NA", ""])
        print("Sucesso! O DataFrame foi carregado corretamente da URL do GitHub.")
    except Exception as e:
        print("Falha ao carregar o arquivo.")
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

print("-" * 72)
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
print("\n")

qtd_linhas_totalmente_vazias = df.isna().all(axis=1).sum()

print(f"Quantidade de linhas 100% vazias: {qtd_linhas_totalmente_vazias}")


print("\n" + "=" * 72)
print("3. TRATAMENTO DE DADOS")
print("=" * 72)

# 1. Chamando a limpeza e capturando a quantidade de duplicadas retornada
df_clean, qtd_duplicadas = limpar_dados(df)


# 2. converte textos de erro em NaN reais
df_com_nulos_reais = padronizar_placeholders_nulos(df_clean)

print("-" * 72)
# 3. relatório de ausentes
relatorio_valores_ausentes(df_com_nulos_reais)

print("-" * 72)
# 4. tratamento de colunas específicas
df_com_nulos_reais = tratar_ausentes(df_com_nulos_reais, coluna="PR_CAT", estrategia="constante", valor_constante="Sem Categoria")
df_com_nulos_reais = tratar_ausentes(df_com_nulos_reais, coluna="PR_NOME", estrategia="constante", valor_constante="Produto não informado")

df_tratado = df_com_nulos_reais.copy()

print("-" * 72)
# 5. normalização
df_normalized = normalizar_dados(df_tratado)

print("-" * 72)
# 6. relatório após normalização
print("\n" + "Segunda inspeção de valores ausentes após o tratamento e normalização:")
relatorio_valores_ausentes(df_normalized)

print("-" * 72)
# 7. tipos de dados após normalização
print("\n" + "Tipos de dados após normalização:")
print(df_normalized.dtypes)

print("\n" + "=" * 72)
print("4. ESTATISTICAS DESCRITIVAS")
print("=" * 72)

print("\n" + "analise de colunas prováveis 'pai' com base na cardinalidade, taxa de repetição e dependência funcional:")
df_analise = relatorio_colunas_pai(df_normalized)
print(df_analise)
print("\n")

print("-" * 72)
estatisticas = analisar_estatisticas_pai(df_normalized, col_pai="cl_id", col_metrica="cl_fhl")

print("\n" + "=" * 72)
print("5. PADRÕES DE AGRUPAMENTOS")
print("=" * 72)

compras_genero = (
    df_normalized.groupby("cl_genero")["co_id"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n5.1 Quantidade de compras por gênero:")
print(compras_genero)

itens_categoria = (
    df_normalized.groupby("pr_cat")
    .size()
    .sort_values(ascending=False)
)

print("-" * 72)
print("\n5.2 Quantidade de itens/registros por categoria:")
print(itens_categoria)

compras_categoria = (
    df_normalized.pivot_table(index="pr_cat", values="co_id", aggfunc="nunique")
    .squeeze()
    .sort_values(ascending=False)
)

print("-" * 72)
print("\n5.3 Quantidade de compras contendo cada categoria:")
print(compras_categoria)

print("\n" + "=" * 72)
print("6. CONCLUSOES E INSIGHTS")
print("=" * 72)
print("\n")

genero_lider = compras_genero.index[0]
qtd_genero_lider = int(compras_genero.iloc[0])

categoria_lider = itens_categoria.index[0]
qtd_categoria_lider = int(itens_categoria.iloc[0])

compras_categoria_lider = compras_categoria.index[0]
qtd_compras_categoria_lider = int(compras_categoria.iloc[0])

# Extraindo informações de estatísticas para a conclusão
stat_fhl = estatisticas.get("cl_fhl", {})
n_clientes_unicos = stat_fhl.get("contagem", len(df_normalized.drop_duplicates(subset=["cl_id"])))
media_fhl = stat_fhl.get("media", 0)
moda_fhl_list = stat_fhl.get("moda", [])
str_moda_fhl = ", ".join(map(str, moda_fhl_list)) if moda_fhl_list else "N/A"

print(
    f"1. Foram identificadas {fmt_int(qtd_duplicadas)} linhas exatamente duplicadas, "
    "removidas na etapa de limpeza."
)
print(
    f"2. A categoria com maior quantidade de itens/registros foi "
    f"'{categoria_lider}', com {fmt_int(qtd_categoria_lider)} ocorrências."
)
print(
    f"3. O gênero com maior número de compras foi '{genero_lider}', "
    f"com {fmt_int(qtd_genero_lider)} compras."
)
print(
    f"4. A categoria com mais compras foi '{compras_categoria_lider}', "
    f"com {fmt_int(qtd_compras_categoria_lider)} compras."
)
print(
    f"5. A base possui {fmt_int(n_clientes_unicos)} clientes únicos; a média de "
    f"filhos por cliente é {media_fhl:.3f} e a moda é {str_moda_fhl}."
)

