import pandas as pd 
df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')

def filtrar_por_regiao(dataframe, regiao):
    return dataframe[dataframe["Região"]==regiao]

def total_por_canal(dataframe,canal):
    filtrado = dataframe[dataframe["Canal"] == canal]
    return filtrado["Valor_Venda"].sum()

norte = filtrar_por_regiao(df,"Norte")
print(norte.head())

sul = filtrar_por_regiao(df,"Sul")
print(sul.head())

total_online = total_por_canal(df,"E-commerce")
print(f"Vendas Online totalizam em R${total_online:,.2f}")