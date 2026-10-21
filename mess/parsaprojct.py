"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Disciplina: Visualização de Dados e Business Intelligence [T3]
Aluno: Charles Ricardo Nascimento D' Lima

Objetivo:
Realizar uma Análise Exploratória de Dados (AED) na base de varejo,
identificando problemas de qualidade, fazendo a limpeza mínima necessária,
gerando estatísticas descritivas e explorando padrões com agrupamentos.

Execução:
    python Miniprojeto_Charles_Ricardo_T3.py

Dependência:
    pandas
"""

from pathlib import Path
import pandas as pd


def fmt_int(valor):
    """Formata inteiros com ponto como separador de milhar."""
    return f"{int(valor):,}".replace(",", ".")


# ---------------------------------------------------------------------
# 1. LOCALIZAÇÃO E LEITURA DO ARQUIVO
# ---------------------------------------------------------------------

PASTA_PROJETO = Path(__file__).resolve().parent

# Aceita os dois nomes mais prováveis para facilitar a execução.
arquivos_candidatos = [
    PASTA_PROJETO / "Base Varejo.csv",
    PASTA_PROJETO / "Varejo.csv",
    PASTA_PROJETO / "BaseVarejo.csv",
]

arquivo_csv = next((p for p in arquivos_candidatos if p.exists()), None)

if arquivo_csv is None:
    raise FileNotFoundError(
        "Arquivo da base não encontrado. Coloque 'Base Varejo.csv' ou "
        "'Varejo.csv' na mesma pasta deste script."
    )

# A base utiliza ponto e vírgula como separador.
df_raw = pd.read_csv(arquivo_csv, sep=";", encoding="utf-8")

print("=" * 72)
print("1. CARREGAMENTO E ESTRUTURA INICIAL")
print("=" * 72)
print(f"Arquivo: {arquivo_csv.name}")
print(f"Número de registros: {fmt_int(len(df_raw))}")
print(f"Número de colunas: {df_raw.shape[1]}")
print("\nColunas:")
for coluna in df_raw.columns:
    print(f" - {coluna}")

print("\nTipos de dados iniciais:")
print(df_raw.dtypes)


# ---------------------------------------------------------------------
# 2. DIAGNÓSTICO DE QUALIDADE
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("2. DIAGNÓSTICO DE QUALIDADE")
print("=" * 72)

print("\nValores nulos por coluna:")
print(df_raw.isna().sum())

# O CSV fornecido possui colunas extras vazias geradas pelos delimitadores
# finais. Elas não pertencem ao dicionário de dados e são 100% nulas.
colunas_totalmente_vazias = [
    coluna for coluna in df_raw.columns
    if df_raw[coluna].isna().all()
]

print("\nColunas 100% vazias:")
if colunas_totalmente_vazias:
    for coluna in colunas_totalmente_vazias:
        print(f" - {coluna}")
else:
    print("Nenhuma.")

# Remove somente as colunas comprovadamente vazias.
df = df_raw.drop(columns=colunas_totalmente_vazias).copy()

# Padronização mínima das colunas de texto.
colunas_texto = df.select_dtypes(include="object").columns
for coluna in colunas_texto:
    df[coluna] = df[coluna].astype("string").str.strip()

# Valores como #N/D não são nulos do pandas, mas representam informação
# ausente e precisam ser tratados como problema de qualidade.
marcadores_ausentes = ["#N/D", "#N/A", "N/D", "N/A", "NA", "NULL", "NONE", ""]

categorias_invalidas = df["PR_CAT"].isin(marcadores_ausentes).sum()
produtos_invalidos = df["PR_NOME"].isin(marcadores_ausentes).sum()

print(f"\nCategorias vazias/indefinidas: {categorias_invalidas:,}".replace(",", "."))
print(f"Nomes de produto vazios/indefinidos: {fmt_int(produtos_invalidos)}")

duplicatas = df.duplicated().sum()
print(f"Linhas exatamente duplicadas: {fmt_int(duplicatas)}")


# ---------------------------------------------------------------------
# 3. LIMPEZA E CONVERSÃO DE TIPOS
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("3. LIMPEZA E CONVERSÃO DE TIPOS")
print("=" * 72)

# Converte os campos numéricos. O parâmetro errors='coerce' transforma
# valores incompatíveis em NaN, permitindo que o problema seja detectado.
colunas_numericas = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# Conversão de data. A base está no padrão dia/mês/ano.
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")

datas_invalidas = df["DATA"].isna().sum()
print(f"Datas inválidas após conversão: {fmt_int(datas_invalidas)}")

# A regra do enunciado pede que categoria vazia seja preenchida
# com "Sem Categoria".
df["PR_CAT"] = (
    df["PR_CAT"]
    .replace(marcadores_ausentes, pd.NA)
    .fillna("Sem Categoria")
)

# O nome do produto também possui o mesmo marcador #N/D.
df["PR_NOME"] = (
    df["PR_NOME"]
    .replace(marcadores_ausentes, pd.NA)
    .fillna("Produto não informado")
)

# A rubrica menciona "dimensões físicas". Entretanto, a base fornecida não
# possui campos como altura, largura, comprimento ou peso. O bloco abaixo
# deixa a regra preparada caso uma versão futura da base contenha esses campos.
possiveis_dimensoes = [
    "ALTURA", "LARGURA", "COMPRIMENTO", "PROFUNDIDADE", "PESO"
]

dimensoes_existentes = [
    coluna for coluna in possiveis_dimensoes
    if coluna in df.columns
]

if dimensoes_existentes:
    print("\nTratamento das dimensões físicas:")
    for coluna in dimensoes_existentes:
        # Para uma medida numérica, a mediana é menos sensível a valores
        # extremos do que a média.
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        mediana = df[coluna].median()
        df[coluna] = df[coluna].fillna(mediana)
        print(f" - {coluna}: nulos preenchidos pela mediana ({mediana}).")
else:
    print(
        "\nA base fornecida não possui colunas de dimensões físicas "
        "(altura, largura, comprimento, profundidade ou peso)."
    )

# Verifica se restaram nulos nas 10 colunas efetivas da base.
print("\nNulos após os tratamentos:")
print(df.isna().sum())

# Remoção de duplicatas exatas.
#
# Justificativa:
# Como não existe coluna de quantidade, linhas completamente idênticas não
# podem ser diferenciadas entre duplicação de registro e compra de mais de uma
# unidade. Para cumprir a limpeza mínima, elas são removidas. Esta limitação
# fica registrada no README e deve ser validada com a fonte dos dados em um
# cenário real.
antes = len(df)
df = df.drop_duplicates().copy()
removidas = antes - len(df)

print(f"\nDuplicatas exatas removidas: {fmt_int(removidas)}")

# Converte para inteiro quando a coluna não possui nulos.
for coluna in colunas_numericas:
    if df[coluna].isna().sum() == 0:
        df[coluna] = df[coluna].astype("int64")


# ---------------------------------------------------------------------
# 4. VALIDAÇÃO DA REGRA DO IDENTIFICADOR DE COMPRA (CO_ID)
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("4. VALIDAÇÃO DO IDENTIFICADOR DE COMPRA (CO_ID)")
print("=" * 72)

# CO_ID identifica a compra/nota fiscal. Ele aparece em várias linhas porque
# uma mesma compra pode conter diversos produtos. A validação abaixo verifica
# se cada CO_ID está associado a apenas uma data e a apenas um cliente.
validacao_compra = (
    df.groupby("CO_ID")
      .agg(
          qtd_datas=("DATA", "nunique"),
          qtd_clientes=("CL_ID", "nunique"),
          qtd_generos=("CL_GENERO", "nunique"),
          qtd_estados_civis=("CL_EC", "nunique"),
          qtd_segmentos=("CL_SEG", "nunique"),
      )
)

compras_inconsistentes = (
    (validacao_compra > 1)
    .any(axis=1)
    .sum()
)

print(f"Compras únicas (CO_ID): {fmt_int(df['CO_ID'].nunique())}")
print(f"Clientes únicos (CL_ID): {fmt_int(df['CL_ID'].nunique())}")
print(f"Produtos/SKUs únicos (PR_ID): {fmt_int(df['PR_ID'].nunique())}")
print(
    "CO_ID com conflito de data/cliente/perfil: "
    f"{fmt_int(compras_inconsistentes)}"
)

if compras_inconsistentes == 0:
    print("Resultado: regra de consistência do CO_ID validada.")
else:
    print("Resultado: existem CO_ID que precisam de investigação.")


# ---------------------------------------------------------------------
# 5. ESTATÍSTICAS DESCRITIVAS - NÚMERO DE FILHOS
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("5. ESTATÍSTICAS - NÚMERO DE FILHOS DOS CLIENTES")
print("=" * 72)

# Como um cliente aparece em muitas compras e produtos, calculamos a
# estatística sobre clientes únicos para não dar peso maior aos clientes
# que compraram mais vezes.
df_clientes = (
    df[["CL_ID", "CL_FHL", "CL_GENERO", "CL_EC", "CL_SEG"]]
    .drop_duplicates(subset=["CL_ID"])
)

filhos = df_clientes["CL_FHL"]

print(f"Contagem:       {fmt_int(filhos.count())}")
print(f"Média:          {filhos.mean():.3f}")
print(f"Mediana:        {filhos.median():.3f}")
print(f"Desvio padrão:  {filhos.std():.3f}")
print(f"Moda:           {', '.join(map(str, filhos.mode().tolist()))}")
print(f"Máximo:         {filhos.max()}")
print(f"Mínimo:         {filhos.min()}")


# ---------------------------------------------------------------------
# 6. AGRUPAMENTOS
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("6. PADRÕES DE AGRUPAMENTO")
print("=" * 72)

# Cria uma visão de compra: uma linha por CO_ID.
df_compras = (
    df[["CO_ID", "CL_ID", "CL_GENERO", "CL_SEG", "DATA"]]
    .drop_duplicates(subset=["CO_ID"])
)

# Agrupamento 1: quantidade de compras por gênero.
compras_genero = (
    df_compras.groupby("CL_GENERO")["CO_ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n6.1 Quantidade de compras por gênero:")
print(compras_genero)

# Agrupamento 2: quantidade de registros/itens por categoria.
itens_categoria = (
    df.groupby("PR_CAT")
    .size()
    .sort_values(ascending=False)
)

print("\n6.2 Quantidade de itens/registros por categoria:")
print(itens_categoria)

# Agrupamento extra: número de compras em que cada categoria apareceu.
compras_categoria = (
    df.groupby("PR_CAT")["CO_ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n6.3 Quantidade de compras contendo cada categoria:")
print(compras_categoria)

# Agrupamento extra: compras por segmento econômico.
compras_segmento = (
    df_compras.groupby("CL_SEG")["CO_ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n6.4 Quantidade de compras por segmento econômico:")
print(compras_segmento)

# Agrupamento temporal.
compras_ano = (
    df_compras.assign(ANO=df_compras["DATA"].dt.year)
    .groupby("ANO")["CO_ID"]
    .nunique()
)

print("\n6.5 Quantidade de compras por ano:")
print(compras_ano)


# ---------------------------------------------------------------------
# 7. EXPORTAÇÃO DA BASE LIMPA
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("7. EXPORTAÇÃO")
print("=" * 72)

arquivo_saida = PASTA_PROJETO / "df_limpo.csv"

# Datas em ISO (AAAA-MM-DD) facilitam interoperabilidade em BI.
df_saida = df.copy()
df_saida["DATA"] = df_saida["DATA"].dt.strftime("%Y-%m-%d")
df_saida.to_csv(
    arquivo_saida,
    sep=";",
    index=False,
    encoding="utf-8-sig",
)

print(f"Arquivo gerado: {arquivo_saida.name}")
print(f"Registros finais: {fmt_int(len(df))}")
print(f"Colunas finais: {df.shape[1]}")


# ---------------------------------------------------------------------
# 8. CONCLUSÕES
# ---------------------------------------------------------------------

print("\n" + "=" * 72)
print("8. CONCLUSÕES")
print("=" * 72)

genero_lider = compras_genero.index[0]
qtd_genero_lider = int(compras_genero.iloc[0])

categoria_lider = itens_categoria.index[0]
qtd_categoria_lider = int(itens_categoria.iloc[0])

segmento_lider = compras_segmento.index[0]
qtd_segmento_lider = int(compras_segmento.iloc[0])

print(
    f"1. Foram identificadas {fmt_int(removidas)} linhas exatamente duplicadas, "
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
    f"4. O segmento econômico com mais compras foi '{segmento_lider}', "
    f"com {fmt_int(qtd_segmento_lider)} compras."
)
print(
    f"5. A base possui {fmt_int(len(df_clientes))} clientes únicos; a média de "
    f"filhos por cliente é {filhos.mean():.3f} e a moda é "
    f"{', '.join(map(str, filhos.mode().tolist()))}."
)
print(
    "6. Permanece uma limitação: como a base não possui coluna de quantidade, "
    "linhas idênticas podem representar duplicação técnica ou mais de uma "
    "unidade do mesmo produto. Em um ambiente real, essa regra deve ser "
    "confirmada com a origem dos dados."
)