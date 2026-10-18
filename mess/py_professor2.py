import pandas as pd 
import datetime as dt 
df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')
#1
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
print(df.dtypes)

#2
df['Num_mes'] = df['Data'].dt.month
print(df.head())

#3
vendas_mes = df.groupby('Num_mes')['Valor_Venda'].sum().reset_index()
print(vendas_mes)

#4
df_trimestre = df[df['Num_mes'].isin([1, 2, 3])]
df_trimestre.to_excel("venda_primeiro_trimestre.xlsx", index=False)

#5
df["Dia_semana"] = df["Data"].dt.day_name()
ticket_medio_dia = df.groupby("Dia_semana")["Valor_Venda"].mean()
dia_maior_ticket = ticket_medio_dia.idxmax()
print(dia_maior_ticket)

#6
data_hoje = dt.datetime.now()
data_limite = data_hoje - dt.timedelta(days=90)
vendas_recentes = df[df['Data'] >= data_limite]
print(len(vendas_recentes))