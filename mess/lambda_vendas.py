import pandas as pd

df = pd.read_excel(r'C:\Users\JK\Desktop\py\sctech\tabela_vendas_ZePequeno_corrigido.xlsx')
'''
valor_vendas = df["Valor_Venda"].apply(lambda v: round(v, 2))
print(valor_vendas.head(10))
'''
ola=lambda x: f"Olá {x}, Bem-vindo(a) ao sistema de vendas da ZePequeno!"
nome = input("Digite seu nome: ")

print(ola(nome))

qtd_vendas = int(input("Quantas vendas fez hoje?: "))
insere_vendas = lambda q: "Puts deu ruim p vc!" if q == 0 else [float(input(f"insira o valor da venda {i}: ")) for i in range(1, q+1)]
soma_listas = lambda lista: sum(lista) if len(lista) > 0 else 0.0
lista_vendas = insere_vendas(qtd_vendas)
print(lista_vendas)
print(f"Total das vendas: R${soma_listas(lista_vendas):.2f}")

