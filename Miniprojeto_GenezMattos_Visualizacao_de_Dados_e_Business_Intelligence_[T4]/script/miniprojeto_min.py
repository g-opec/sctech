"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07 (Versão Minimalista Sem Funções)
Disciplina: Visualização de Dados e Business Intelligence [T4]
Aluno: Genez José de Mattos Junior
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------
# 1. LOCALIZAÇÃO E LEITURA DO ARQUIVO
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
    print("Arquivo CSV não encontrado localmente. Tentando ler diretamente da URL do GitHub...")
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
print(f"Número de registros: {int(len(df)):,}".replace(",", "."))
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

# ---------------------------------------------------------------------
# 3. TRATAMENTO DE DADOS
# ---------------------------------------------------------------------
print("\n" + "=" * 72)
print("3. TRATAMENTO DE DADOS")
print("=" * 72)

# Limpeza estrutural
df_clean = df.copy()
print(f"Dimensões antes da limpeza: {df_clean.shape[0]} linhas, {df_clean.shape[1]} colunas.")

colunas_vazias = [col for col in df_clean.columns if df_clean[col].isna().all()]
if colunas_vazias:
    print(f"Removendo {len(colunas_vazias)} coluna(s) totalmente vazia(s):")
    for coluna in colunas_vazias:
        print(f" - {coluna}")
    df_clean = df_clean.drop(columns=colunas_vazias)
else:
    print("Nenhuma coluna 100% vazia encontrada.")

linhas_antes = len(df_clean)
df_clean = df_clean.dropna(how="all")
linhas_removidas = linhas_antes - len(df_clean)

if linhas_removidas > 0:
    print(f"Removidas {linhas_removidas} linha(s) totalmente vazia(s).")
else:
    print("Nenhuma linha 100% vazia encontrada.")

qtd_duplicadas = df_clean.duplicated().sum()
print(f"Quantidade de linhas duplicadas: {qtd_duplicadas}")
if qtd_duplicadas > 0:
    print(f"Removendo {qtd_duplicadas} linha(s) duplicada(s).") 
    df_clean = df_clean.drop_duplicates()

print(f"Dimensões após a limpeza: {df_clean.shape[0]} linhas, {df_clean.shape[1]} colunas.\n")

# Padronização de placeholders nulos
df_com_nulos_reais = df_clean.copy()
termos_nulos = ["#n/d", "#n/a", "n/d", "n/a", "na", "null", "none", ""]

for col in df_com_nulos_reais.columns:
    if df_com_nulos_reais[col].dtype == "object":
        serie_str = df_com_nulos_reais[col].astype(str).str.strip().str.lower()
        mask = serie_str.isin(termos_nulos)
        df_com_nulos_reais.loc[mask, col] = np.nan

print("-" * 72)

# Relatório de valores ausentes
total_linhas = len(df_com_nulos_reais)
qtd_ausentes = df_com_nulos_reais.isna().sum()
pct_ausentes = (qtd_ausentes / total_linhas) * 100
resumo = pd.DataFrame({"Qtd_Ausentes": qtd_ausentes, "%_Ausentes": pct_ausentes})
resumo_filtrado = resumo[resumo["Qtd_Ausentes"] > 0].sort_values(by="%_Ausentes", ascending=False)

print(f"Total de linhas na base: {total_linhas}")
if not resumo_filtrado.empty:
    print("\nColunas com valores ausentes:")
    print(resumo_filtrado.to_string())
else:
    print("\nNenhuma coluna possui valores ausentes.")

print("-" * 72)

# Tratamento de colunas específicas (constantes)
for coluna, valor_constante in [("PR_CAT", "Sem Categoria"), ("PR_NOME", "Produto não informado")]:
    if coluna in df_com_nulos_reais.columns:
        nulos_antes = df_com_nulos_reais[coluna].isna().sum()
        if nulos_antes > 0:
            df_com_nulos_reais[coluna] = df_com_nulos_reais[coluna].fillna(valor_constante)
            print(f"Coluna '{coluna}': {nulos_antes} nulos preenchidos com a constante '{valor_constante}'.")

df_tratado = df_com_nulos_reais.copy()

print("-" * 72)

# Normalização
print("Iniciando a normalização dos dados...")
df_normalized = df_tratado.copy()
df_normalized.columns = df_normalized.columns.str.strip().str.lower().str.replace(" ", "_")

for col in df_normalized.select_dtypes(include=["object", "string"]).columns:
    df_normalized[col] = df_normalized[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

print("Verificando e limpando colunas numéricas...")
for col in df_normalized.columns:
    if df_normalized[col].dtype == "object":
        amostra = df_normalized[col].dropna()
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
                    df_normalized[col] = (
                        df_normalized[col].astype(str)
                        .str.replace("R$", "", regex=False)
                        .str.replace(" ", "")
                        .str.replace(".", "", regex=False)
                        .str.replace(",", ".", regex=False)
                    )
                    df_normalized[col] = pd.to_numeric(df_normalized[col], errors="coerce")
                    print(f" - Coluna '{col}' convertida para numérica com sucesso.")
            except Exception:
                pass

formatos_data = {
    "dd/mm/aaaa": "%d/%m/%Y", "dd/mm/aa": "%d/%m/%y", "aaaa-mm-dd": "%Y-%m-%d",
    "aa-mm-dd": "%y-%m-%d", "dd-mm-aaaa": "%d-%m-%Y", "dd-mm-aa": "%d-%m-%y",
    "mm/dd/aaaa": "%m/%d/%Y", "mm/dd/aa": "%m/%d/%y", "dd.mm.aaaa": "%d.%m.%Y",
}

print("Analisando e convertendo colunas de data...")
for col in df_normalized.select_dtypes(include=["object", "string"]).columns:
    amostra = df_normalized[col].dropna()
    amostra_str = amostra[amostra.apply(lambda x: isinstance(x, str))]

    if len(amostra_str) == 0:
        continue

    convertido_com_sucesso = False
    for desc_formato, formato_str in formatos_data.items():
        try:
            convertido = pd.to_datetime(amostra_str, format=formato_str, errors="coerce")
            if convertido.notna().sum() / len(amostra_str) > 0.8:
                df_normalized[col] = pd.to_datetime(df_normalized[col], format=formato_str, errors="coerce")
                print(f" - Coluna '{col}' convertida para datetime usando o formato '{desc_formato}'.")
                convertido_com_sucesso = True
                break
        except Exception:
            continue

    if not convertido_com_sucesso:
        try:
            convertido_geral = pd.to_datetime(amostra_str, format='mixed', errors="coerce")
            if convertido_geral.notna().sum() / len(amostra_str) > 0.8:
                df_normalized[col] = pd.to_datetime(df_normalized[col], format='mixed', errors="coerce")
                print(f" - Coluna '{col}' convertida para datetime usando inferência padrão.")
        except Exception:
            pass

print("Normalização concluída com sucesso!")

print("-" * 72)
print("\nSegunda inspeção de valores ausentes após o tratamento e normalização:")
total_linhas_norm = len(df_normalized)
qtd_ausentes_norm = df_normalized.isna().sum()
pct_ausentes_norm = (qtd_ausentes_norm / total_linhas_norm) * 100
resumo_norm = pd.DataFrame({"Qtd_Ausentes": qtd_ausentes_norm, "%_Ausentes": pct_ausentes_norm})
resumo_filtrado_norm = resumo_norm[resumo_norm["Qtd_Ausentes"] > 0].sort_values(by="%_Ausentes", ascending=False)

print(f"Total de linhas na base: {total_linhas_norm}")
if not resumo_filtrado_norm.empty:
    print("\nColunas com valores ausentes:")
    print(resumo_filtrado_norm.to_string())
else:
    print("\nNenhuma coluna possui valores ausentes.")

print("-" * 72)
print("\nTipos de dados após normalização:")
print(df_normalized.dtypes)

# ---------------------------------------------------------------------
# 4. ESTATISTICAS DESCRITIVAS
# ---------------------------------------------------------------------
print("\n" + "=" * 72)
print("4. ESTATISTICAS DESCRITIVAS")
print("=" * 72)

print("\nAnálise de colunas prováveis 'pai' com base na cardinalidade, taxa de repetição e dependência funcional:")
n_linhas_df = len(df_normalized)
relatorio_pai = []

for col in df_normalized.columns:
    n_unicos = df_normalized[col].nunique()
    taxa_unicidade = (n_unicos / n_linhas_df) * 100
    media_repeticao = n_linhas_df / n_unicos if n_unicos > 0 else 0

    atributos_dependentes = 0
    if 1 < n_unicos < n_linhas_df:
        for outra_col in df_normalized.columns:
            if outra_col == col:
                continue
            if df_normalized.groupby(col)[outra_col].nunique().max() == 1:
                atributos_dependentes += 1

    relatorio_pai.append({
        "coluna": col,
        "n_unicos": n_unicos,
        "unicidade_pct": round(taxa_unicidade, 2),
        "media_linhas_por_pai": round(media_repeticao, 2),
        "atributos_dependentes": atributos_dependentes,
    })

df_analise = pd.DataFrame(relatorio_pai)
df_analise = df_analise.sort_values(by=["atributos_dependentes", "unicidade_pct"], ascending=[False, True]).reset_index(drop=True)
print(df_analise)
print("\n")

print("-" * 72)
# Estatísticas da entidade pai 'cl_id' para a métrica 'cl_fhl'
col_pai = "cl_id"
col_metrica = "cl_fhl"
df_pai = df_normalized.drop_duplicates(subset=[col_pai])
filhos = df_pai[col_metrica]

moda_vals = filhos.mode()
total_unicos = filhos.nunique()

if len(moda_vals) > 10 or (total_unicos > 0 and len(moda_vals) > (total_unicos * 0.5)):
    str_moda = "N/A (Alta dispersão / Sem moda clara)"
    moda_lista = []
else:
    str_moda = ", ".join(map(str, moda_vals.tolist()))
    moda_lista = moda_vals.tolist()

contagem = filhos.count()
media = filhos.mean() if contagem > 0 else 0
mediana = filhos.median() if contagem > 0 else 0
desvio_padrao = filhos.std() if contagem > 1 else 0
maximo = filhos.max() if contagem > 0 else 0
minimo = filhos.min() if contagem > 0 else 0

print(f"=== Relatório Estatístico dos Filhos por Pai: '{col_pai}' ===")
print(f"Total de entidades pai únicas ({col_pai}): {int(len(df_pai)):,}".replace(",", ".") + "\n")
print(f"--- Métrica: {col_metrica} ---")
print(f"Contagem:       {int(contagem):,}".replace(",", "."))
print(f"Média:          {media:.3f}")
print(f"Mediana:        {mediana:.3f}")
print(f"Desvio padrão:  {desvio_padrao:.3f}" if pd.notna(desvio_padrao) else "Desvio padrão:  0.000")
print(f"Moda:           {str_moda}")
print(f"Máximo:         {maximo}")
print(f"Mínimo:         {minimo}\n")

# ---------------------------------------------------------------------
# 5. PADRÕES DE AGRUPAMENTOS
# ---------------------------------------------------------------------
print("\n" + "=" * 72)
print("5. PADRÕES DE AGRUPAMENTOS")
print("=" * 72)

compras_genero = df_normalized.groupby("cl_genero")["co_id"].nunique().sort_values(ascending=False)
print("\n5.1 Quantidade de compras por gênero:")
print(compras_genero)

itens_categoria = df_normalized.groupby("pr_cat").size().sort_values(ascending=False)
print("-" * 72)
print("\n5.2 Quantidade de itens/registros por categoria:")
print(itens_categoria)

compras_categoria = df_normalized.pivot_table(index="pr_cat", values="co_id", aggfunc="nunique").squeeze().sort_values(ascending=False)
print("-" * 72)
print("\n5.3 Quantidade de compras contendo cada categoria:")
print(compras_categoria)

# ---------------------------------------------------------------------
# 6. CONCLUSÕES E INSIGHTS
# ---------------------------------------------------------------------
print("\n" + "=" * 72)
print("6. CONCLUSÕES E INSIGHTS")
print("=" * 72)
print("\n")

genero_lider = compras_genero.index[0]
qtd_genero_lider = int(compras_genero.iloc[0])

categoria_lider = itens_categoria.index[0]
qtd_categoria_lider = int(itens_categoria.iloc[0])

compras_categoria_lider = compras_categoria.index[0]
qtd_compras_categoria_lider = int(compras_categoria.iloc[0])

n_clientes_unicos = contagem
media_fhl = media
str_moda_fhl = str_moda if not moda_lista else (str(moda_lista[0]) if len(moda_lista) == 1 else str_moda)

print(f"1. Foram identificadas {int(qtd_duplicadas):,}".replace(",", ".") + " linhas exatamente duplicadas, removidas na etapa de limpeza.")
print(f"2. A categoria com maior quantidade de itens/registros foi '{categoria_lider}', com {int(qtd_categoria_lider):,}".replace(",", ".") + " ocorrências.")
print(f"3. O gênero com maior número de compras foi '{genero_lider}', com {int(qtd_genero_lider):,}".replace(",", ".") + " compras.")
print(f"4. A categoria com mais compras foi '{compras_categoria_lider}', com {int(qtd_compras_categoria_lider):,}".replace(",", ".") + " compras.")
print(f"5. A base possui {int(n_clientes_unicos):,}".replace(",", ".") + f" clientes únicos; a média de filhos por cliente é {media_fhl:.3f} e a moda é {str_moda_fhl}.")