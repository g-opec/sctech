'''
#Exercício 1
# Percentual de nulos por coluna
percentual_nulos = df.isnull().mean() * 100

# Ordenando do maior para o menor
percentual_nulos = percentual_nulos.sort_values(ascending=False)
print("Percentual de valores ausentes por coluna:")
print(percentual_nulos.round(1))

# Colunas com mais de 30% de nulos
criticas = percentual_nulos[percentual_nulos > 30]
print("///nColunas com mais de 30% de valores ausentes:")
print(criticas)
Saída esperada:

Percentual de valores ausentes por coluna:
Valor_Venda    50.0
Qtd_Itens      40.0
Data_Pedido    30.0
Região         20.0
Categoria      30.0
Colunas com mais de 30% de valores ausentes:
Valor_Venda    50.0
Qtd_Itens      40.0


#Exercício 2
# Imputação da mediana por grupo de Região

df["Valor_Venda"] = df.groupby("Região")["Valor_Venda"].transform(
    lambda x: x.fillna(x.median())
)

# Confirmação: se houver nulos restantes, o assert lança um erro
assert df["Valor_Venda"].isnull().sum() == 0, "Ainda existem nulos em Valor_Venda!"

print("Imputação concluída com sucesso.")

print(df[["Região", "Valor_Venda"]])

# Por que imputação grupada é melhor que a mediana global? Porque valores de venda tendem a variar por região. Usar a mediana global "contamina" grupos com padrões distintos, introduzindo viés. A imputação grupada preserva a distribuição local de cada segmento.  
# Principais técnicas para lidar com valores ausentes


# Exercício 3
def tratar_nulos(df):
    """
    Aplica estratégias de imputação de acordo com o tipo de cada coluna:
    - Numéricas  → mediana
    - Categóricas (object) → moda
    - Datas (datetime) → forward fill
    Retorna uma cópia do DataFrame sem modificar o original.
    """
    df_limpo = df.copy()

    # Colunas numéricas → mediana
    colunas_numericas = df_limpo.select_dtypes(include=["number"]).columns
    for col in colunas_numericas:
        df_limpo[col] = df_limpo[col].fillna(df_limpo[col].median())

   # Colunas categóricas → moda (valor mais frequente)
    colunas_categoricas = df_limpo.select_dtypes(include=["object"]).columns
    for col in colunas_categoricas:
        moda = df_limpo[col].mode()[0]  # mode() retorna uma Series; pegamos o primeiro
        df_limpo[col] = df_limpo[col].fillna(moda)

    # Colunas de data → forward fill
    colunas_data = df_limpo.select_dtypes(include=["datetime"]).columns
    for col in colunas_data:
        df_limpo[col] = df_limpo[col].ffill()

    # Verificação final
    nulos_restantes = df_limpo.isnull().sum().sum()
    print(f"Tratamento concluído. Nulos restantes: {nulos_restantes}")

    return df_limpo

# Uso
df_limpo = tratar_nulos(df)
print(df_limpo)

# 1. Conte o número total de linhas duplicadas (exatas) no dataset.
   total_duplicadas = df.duplicated().sum()

# 2. Se o número de duplicatas for 0, insira duplicatas manualmente usando as 5 primeiras linhas.
   if df.duplicated().sum() == 0:
       df = pd.concat([df, df.iloc[:5]], ignore_index=True)

# 3. Identifique registros com a mesma combinação de Canal, Produto e Data e descubra qual canal tem mais duplicatas parciais.
   # marca duplicatas parciais
   dup_parciais = df.duplicated(subset=["Canal", "Produto", "Data"], keep=False)
   # filtra apenas linhas que participam de duplicatas parciais
   df_dup = df[dup_parciais]
   # conta duplicatas por canal
   duplicatas_por_canal = df_dup.groupby("Canal").size()
   canal_com_mais_duplicatas = duplicatas_por_canal.idxmax()

   # 4. Função que detecta duplicatas com janela temporal de ±1 dia (mesmo produto e canal em datas consecutivas).
   from datetime import timedelta
   def marca_suspeitas_janela(df):
       df = df.sort_values(["Canal", "Produto", "Data"]).copy()
       # compara com linha anterior
       prev_igual = (
           (df["Canal"] == df["Canal"].shift(1)) &
           (df["Produto"] == df["Produto"].shift(1)) &
           ( (df["Data"] - df["Data"].shift(1)).abs() <= timedelta(days=1) )
       )
       # compara com linha seguinte
       next_igual = (
           (df["Canal"] == df["Canal"].shift(-1)) &
           (df["Produto"] == df["Produto"].shift(-1)) &
           ( (df["Data"].shift(-1) - df["Data"]).abs() <= timedelta(days=1) )
       )
       df["suspeita_janela_1dia"] = prev_igual | next_igual
       return df





import pandas as pd

df = pd.read_excel(r"C:/Users/JK/Desktop/py/sctech/tabela_vendas_ZePequeno_corrigido.xlsx")

# Verificar duplicatas exatas
print("Duplicatas encontradas:", df.duplicated().sum())

# Visualizar registros duplicados
print(df[df.duplicated(keep=False)])

# Remover duplicatas exatas (manter primeira ocorrência)
df_limpo = df.drop_duplicates()

# Duplicata parcial: mesma Região + Produto + Data
df_sem_dup_parcial = df.drop_duplicates(
    subset=["Região", "Produto", "Data"],
    keep="first"
)

print(f"Linhas antes: {len(df)} | Após remoção: {len(df_limpo)}")



import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# 1) Carregar os dados
# Substitua pelo caminho do seu arquivo se necessário.
df = pd.read_excel(r"C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido.xlsx")

# criar coluna de venda total (unidades * valor) para análise de outliers
df["venda_total"] = df["unidades_vendidas_cx"] * df["valor_R$_cx"]

# Coluna que vamos analisar
col = "venda_total"

# Informações iniciais 
print("Dimensão do DataFrame:", df.shape)
print("Colunas:", df.columns.tolist())
print(f"Resumo da coluna '{col}':")
print(df[col].describe())
print("Número de valores nulos nessa coluna:", df[col].isna().sum())
print("\n--- Iniciando identificação de outliers ---\n")

# 2) Método 1 — IQR (Interquartile Range)
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1

limite_inf = Q1 - 1.5 * IQR
limite_sup = Q3 + 1.5 * IQR

# Imprimir
print("IQR method:")
print(f" Q1 (25%): {Q1}")
print(f" Q3 (75%): {Q3}")
print(f" IQR    : {IQR}")
print(f" Limite inferior (Q1 - 1.5*IQR): {limite_inf}")
print(f" Limite superior (Q3 + 1.5*IQR): {limite_sup}")

# Construir máscara booleana: True para outliers, False caso contrário.
# Observação: se houver NaN, a comparação produz NaN - por isso usamos .fillna(False) depois.
mask_iqr = (df[col] < limite_inf) | (df[col] > limite_sup)

# Selecionar os outliers pelo IQR
outliers_iqr = df.loc[mask_iqr.fillna(False)]  # NaNs tratados como False
print(f"\nNúmero de outliers pelo método IQR: {len(outliers_iqr)}")
print("Exemplos (primeiras linhas):")
print(outliers_iqr[[col]].head())


# 3) Método 2 — Z-score
# - Z = (x - média) / desvio_padrão
# - Valores com |Z| > 3 são frequentemente considerados outliers (regra prática)
# - Importante: distribuições muito assimétricas podem tornar o Z-score menos apropriado.

# Calculamos z-score como uma Series alinhada ao índice do DataFrame.
# Assim evitamos problemas quando existir NaN (não dropamos linhas).
val = df[col]
media = val.mean()
desvio = val.std(ddof=0)  # ddof=0 -> desvio populacional; para amostral use ddof=1

print("\nZ-score method:")
print(f" Média: {media}")
print(f" Desvio padrão (ddof=0): {desvio}")

# Z-score em forma de Series (mesmo índice do df)
z_scores = (val - media) / desvio

# Máscara de outliers por Z-score: True se |Z| > 3
mask_z = z_scores.abs() > 3

# Selecionar outliers por Z-score
outliers_z = df.loc[mask_z.fillna(False)]
print(f"\nNúmero de outliers pelo método Z-score (> 3σ): {len(outliers_z)}")
print("Exemplos (primeiras linhas):")
print(outliers_z[[col]].head())


# 4) Salvar resultados para auditoria
#outliers_iqr.to_excel("outliers_iqr_venda.xlsx", index=False)
#outliers_z.to_excel("outliers_zscore_venda.xlsx", index=False)

print("\nArquivos salvos:")
print(" - outliers_iqr_venda.xlsx")
print(" - outliers_zscore_venda.xlsx")

# 5) Visualização 1 — Boxplot global
# Explicação: o boxplot mostra a mediana, quartis, "whiskers" e os fliers (outliers).
# Matplotlib/pandas marcará automaticamente os fliers.

plt.figure(figsize=(8, 6))
plt.boxplot(df[col].dropna(), vert=True, patch_artist=True,
            boxprops=dict(facecolor="#a6cee3", color="#1f78b4"),
            medianprops=dict(color="red"),
            whiskerprops=dict(color="#1f78b4"),
            capprops=dict(color="#1f78b4"),
            flierprops=dict(marker='o', markerfacecolor='none', markeredgecolor="#1f78b4"),
            labels=["Todas as Regiões"])  # um rótulo simples para a caixa
plt.title("Boxplot Global — Venda Total")
plt.ylabel("Venda Total")
plt.suptitle("")  # remove título automático
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


# 6) Visualização 2 — Scatter com destaque dos outliers
# Explicação: plotamos todos os pontos e destacamos aqueles marcados por IQR e Z-score.
# Isso ajuda a ver onde os outliers estão no eixo y e se são os mesmos entre os métodos.

plt.figure(figsize=(12, 6))

# pontos de todos os dados (com jitter no eixo x para visualização)
x_all = np.zeros(len(df)) + 1
y_all = df[col]
plt.scatter(x_all + (np.random.rand(len(df)) - 0.5) * 0.08, y_all, alpha=0.3, s=10, color="#888888", label="Todos (valores)")

# destacar outliers IQR (laranja)
if not outliers_iqr.empty:
    x_iqr = np.ones(len(outliers_iqr)) + 1.0
    plt.scatter(x_iqr + (np.random.rand(len(outliers_iqr)) - 0.5) * 0.08, outliers_iqr[col],
                color="orange", edgecolor="k", s=50, label=f"Outliers IQR ({len(outliers_iqr)})")

# destacar outliers Z (vermelho)
if not outliers_z.empty:
    x_z = np.ones(len(outliers_z)) + 1.6
    plt.scatter(x_z + (np.random.rand(len(outliers_z)) - 0.5) * 0.08, outliers_z[col],
                color="red", edgecolor="k", s=50, label=f"Outliers Z (>3σ) ({len(outliers_z)})")

plt.xlim(0.7, 2.4)
plt.xticks([1, 2], ["Dados", "Outliers destacados"])
plt.ylabel("Venda Total")
plt.title("Distribuição com Outliers Destacados (IQR = laranja; Z = vermelho)")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


# 7) Flagging no DataFrame (útil para consultas e exercícios)
# - outlier_iqr: True se marcado pelo IQR
# - outlier_z  : True se marcado pelo Z-score
# - outlier_any: True se marcado por qualquer um dos dois

df["outlier_iqr"] = mask_iqr.fillna(False)
df["outlier_z"] = mask_z.fillna(False)
df["outlier_any"] = df["outlier_iqr"] | df["outlier_z"]

# Salvar tabela com flags (para exercícios em sala)
#df.to_excel("tabela_com_flags_outliers.xlsx", index=False)
#print("//nArquivo salvo: tabela_com_flags_outliers.xlsx (contém colunas outlier_iqr, outlier_z, outlier_any)")

# 8) Observações finais (para comentar em aula)

print("//nObservações para a aula:")
print("- IQR é baseado em quartis e é robusto a muitos tipos de distribuição.")
print("- Z-score assume simetria (ou que valores extremos raros são pouco prováveis).")
print("- Métodos diferentes podem identificar conjuntos distintos de outliers.")
print("- Decidir o que fazer com outliers depende do contexto: remover, transformar, corrigir (erro de entrada) ou manter.")
print("- Neste script NÃO alteramos os valores originais (apenas marcamos).")
print("//nFim do script didático sobre outliers.")

'''
