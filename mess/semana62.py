
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
df = pd.read_excel(r"C:/Users/JK/Desktop/py/sctech/tabela_vendas_ZePequeno_corrigido.xlsx")

# Inicializando o scaler
scaler = MinMaxScaler()

# Aplicando a transformação (fit calcula min/max, transform aplica a fórmula)
df["Valor_Venda_MinMax"] = scaler.fit_transform(df[["Valor_Venda"]])

# Verificação de integridade
v_min = df["Valor_Venda_MinMax"].min()
v_max = df["Valor_Venda_MinMax"].max()

print(f"Mínimo: {v_min} | Máximo: {v_max}")
# Resultado esperado: Mínimo: 0.0 | Máximo: 1.0


from sklearn.preprocessing import RobustScaler

# Aplicação de ambos para comparação
df["MinMax"] = MinMaxScaler().fit_transform(df[["Valor_Venda"]])
df["Robust"] = RobustScaler().fit_transform(df[["Valor_Venda"]])

# Filtrando os 10 maiores para observação
outliers_comp = df.nlargest(10, "Valor_Venda")[["MinMax", "Robust"]]
print(outliers_comp)


from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer

# 1. Função para remover outliers via IQR
def remove_outliers_iqr(X):
    X = pd.DataFrame(X)
    Q1 = X.quantile(0.25)
    Q3 = X.quantile(0.75)
    IQR = Q3 - Q1
    # Filtra os dados dentro do limite (opcional: em pipelines, 
    # as vezes apenas clipamos os valores para não quebrar o shape)
    return X.clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR, axis=1)

# 2. Construção do Pipeline
pipeline_processamento = Pipeline([
    # Etapa 1: Imputação pela mediana
    ("imputer", SimpleImputer(strategy="median")),
    
    # Etapa 2: Tratamento de outliers (usando FunctionTransformer)
    ("outlier_remover", FunctionTransformer(remove_outliers_iqr)),
    
    # Etapa 3: Padronização (Z-score)
    ("scaler", StandardScaler())
])

# Execução
dados_processados = pipeline_processamento.fit_transform(df[["Valor_Venda"]])

