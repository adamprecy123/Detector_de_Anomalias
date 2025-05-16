import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

# Etapa 1: Leitura dos dados
dados = pd.read_csv('dados.csv')



                     


# Etapa 2: Visualização inicial
print("Visualização inicial dos dados:")
print(dados.head())

# Etapa 3: Padronização (Z-score) - apenas das colunas numéricas
colunas_numericas = dados.select_dtypes(include=['float64', 'int']).columns
scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(dados[colunas_numericas])

# Etapa 4: Conversão para DataFrame novamente
dados_zscore = pd.DataFrame(dados_padronizados, columns=colunas_numericas)

# Etapa 5: Detecção de outliers (Z-score > 3 ou < -3)
outliers = (dados_zscore > 3) | (dados_zscore < -3)

# Etapa 6: Exibir onde existem outliers
print("\nMatriz de outliers (True indica outlier):")
print(outliers)

# Etapa 7: Listar os dados originais com pelo menos um outlier
linhas_com_outliers = outliers.any(axis=1)
print("\nLinhas com outliers detectados:")
print(dados[linhas_com_outliers])

# Etapa 8: Visualização gráfica com boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=dados[colunas_numericas], orient="h")
plt.title("Boxplot das variáveis numéricas")
plt.tight_layout()
plt.show()
