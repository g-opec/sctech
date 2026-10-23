import io
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://pt.wikipedia.org/wiki/Popula%C3%A7%C3%A3o_mundial'
headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# find_all para pegar todas as tabelas da página
tables_html = soup.find_all('table')
print(f"Total de tags <table> encontradas: {len(tables_html)}")

# Converter cada tabela HTML em um DataFrame do Pandas
dfs = []
for t in tables_html:
    try:
        # Lê a tabela individualmente usando StringIO
        df_list = pd.read_html(io.StringIO(str(t)))
        dfs.extend(df_list)
    except ValueError:
        # Ignora caso alguma tabela interna não consiga virar DataFrame
        pass

print(f"Total de DataFrames gerados: {len(dfs)}")

# Exemplo: visualizando a primeira e a segunda tabela
if len(dfs) > 0:
    print("\n--- Tabela 0 ---")
    print(dfs[0].head())

if len(dfs) > 1:
    print("\n--- Tabela 1 ---")
    print(dfs[1].head())