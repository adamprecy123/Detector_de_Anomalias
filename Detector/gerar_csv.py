import pandas as pd
import random
from datetime import datetime, timedelta

# Gerar dados fictícios
num_linhas = 100
data_base = datetime(2025, 1, 1, 8, 0)

dados = {
    "data": [],
    "valor": []
}

for i in range(num_linhas):
    data_transacao = data_base + timedelta(hours=random.randint(1, 2000))
    valor_transacao = round(random.uniform(10, 50000), 2)
    dados["data"].append(data_transacao.strftime("%Y-%m-%d %H:%M:%S"))
    dados["valor"].append(valor_transacao)

df = pd.DataFrame(dados)
df.to_csv("dados.csv", index=False, encoding="utf-8")
print("Arquivo 'dados.csv' gerado com sucesso!")
