import pandas as pd
df = pd.read_excel(r'C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido.xlsx')

print(df.shape)

resumo = df[["Região","Valor_Venda"]]
print("------------------------------------------------")
print("                                             ")
print(resumo.head(10))
resumo.to_csv(r'C:\Users\JK\Desktop\py\sctech\resumo_vendas.csv', index=False)

df_online = df[df["Canal"].astype(str).str.strip().str.lower() == 'e-commerce']
print("------------------------------------------------")
print("                                             ")
print(df_online.head(10))

df_online.to_json(r'C:\Users\JK\Desktop\py\sctech\vendas_online.json', orient='records', force_ascii=False)
print("------------------------------------------------")
print("                                             ")
print("quantidade de registros: ", len(df_online))

print("------------------------------------------------")
print("                                             ")
print(df.head(5))

print("------------------------------------------------")
print("                                             ")
print(df["Valor_Venda"].head(1))

print("------------------------------------------------")
print("                                             ")
print(df.dtypes)

df.to_json(r'C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno.json', orient='records', force_ascii=False, indent=2)

df_csv = pd.read_csv(r'C:\Users\JK\Desktop\py\sctech\resumo_vendas.csv')

print("------------------------------------------------")
print("                                             ")
print(df_csv.head(5))

print("------------------------------------------------")
print("                                             ")
print(resumo.equals(df_csv))