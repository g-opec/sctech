'''
# 1 — Indexação por posição
import numpy as np
v = np.array([50, 150, 300, 450, 600])
resultado = v[[1, 3]]
print(resultado)
# [150 450]
'''
'''
# 2 — dtype e shape
import numpy as np
a = np.array([89.90, 210.00, 520.75])
print(a.dtype)   # → float64
print(a.shape)   # → (3,)
'''
'''
# 3 - Array 2D e filtragem
import numpy as np

# 4 regiões × 3 canais, valores entre R$50 e R$1000
m = np.random.randint(50, 1000, (4, 3))
'''
#print("Array completo:\n", m)
'''
# Filtrando valores acima de R$500
acima_500 = m[m > 500]
print("Valores acima de R$500:", acima_500)
'''
'''
# 4  - Indexação booleana com média
import numpy as np
#(4, 3) 4 listas de 3 elementos cada, valores entre R$50 e R$1000
m = np.random.randint(50, 1000, (4, 3))

# Canal Online = coluna de índice 1
canal_online = m[:, 1]

# Selecionando apenas os que superam a média geral
media_geral = m.mean()
resultado = canal_online[canal_online > media_geral]

print("Média geral:", media_geral)
print("Vendas Online acima da média:", resultado)
'''
import numpy as np
#1

vendas = np.array([100, 250, 400, 750, 1200])
print(vendas*1.12)

#2

dados = np.array([89.9, 210.0, 520.75, 340.0, 670.3])
media = np.mean(dados)
print("Média dos dados:", media)
desvio_padrao = np.std(dados)
print("Desvio padrão dos dados:", desvio_padrao)

#import pandas as pd

#df = pd.read_excel(r'C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido.xlsx')

#q1
#print(df.dtypes)

#q2
#q2 = df[["Produto", "Valor_Venda"]].reset_index(drop=True)
#q2.to_csv(r"C:\Users\JK\Desktop\py\sctech\produtos_valores.csv", index=False, encoding="utf-8-sig")

#q3
#q3 = pd.read_csv(r"C:\Users\JK\Desktop\py\sctech\produtos_valores.csv", encoding="utf-8-sig",sep=",")
#resultado = q2.equals(q3)
#print("Os DataFrames são idênticos?", "Sim" if resultado else "Não")

#q4
#df.to_json(r"C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido_json.json", orient="records", force_ascii=False, indent=2)
#q4 = pd.read_json(r"C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido_json.json")

#q5

def carrgar_dados(caminho,tipo):
    if tipo == "excel":
        return pd.read_excel(caminho)
    elif tipo == "csv":
        return pd.read_csv(caminho)
    elif tipo == "json":
        return pd.read_json(caminho)
    else:
        raise ValueError("Tipo de arquivo não suportado. Use 'excel', 'csv' ou 'json'.")

#print(carrgar_dados(r"C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido.xlsx", "excel").head())    

'''
vendas = df[df["Canal"] == "E-commerce"]
print(vendas["Valor_Venda"].head())

vendas2 = df.loc[df["Canal"] == "E-commerce", ["Produto", "Valor_Venda"]]
print(vendas2.head(10))

vendas3 = df.query('Canal == "Loja Física" and Região == "Joinville" and 1500 <= Valor_Venda <= 2600')[["Produto", "Valor_Venda"]]
print(vendas3.head(10))
'''
'''
#1
acima_da_media = lambda valor: valor > 284.84
print(acima_da_media(300.00))

#2
vendas = [900, 1200, 2991]
vendas_com_frete = list(map(lambda valor: valor + 100, vendas))
print(vendas_com_frete)

#3
def categorizar_pacoca(Valor_Venda):
    if Valor_Venda >= 50.00:
        return "Cx 100 Paçoca Premium"
    elif Valor_Venda >= 24.99:
        return "Cx 100 Paçoca Free Sugar"
    else:
        return "Cx 100 Paçoca Padrão"

df["categoria"] = df["Valor_Venda"].apply(categorizar_pacoca)
print(df.head())

#4
registros = [
    ("E-Commerce", 2500),
    ("Loja Física", 3000),
    ("E-Commerce", 1500),
    ("E-Commerce", 4200),
]

vendas_filtradas = list(
    filter(lambda x: x[0] == "E-Commerce" and x[1] > 2000, registros)
)

print(vendas_filtradas)

#5
amplitude_vendas = df.groupby("Região")["Valor_Venda"].agg(lambda x: x.max() - x.min())

print(amplitude_vendas)

#6
df_ordenado = df.sort_values(
    by=["Região", "Valor_Venda"],
    ascending=[True, False],
    key=lambda coluna: coluna.str.lower() if coluna.dtype == "object" else coluna
)

print(df_ordenado)
'''
