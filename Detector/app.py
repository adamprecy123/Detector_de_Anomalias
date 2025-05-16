import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Configuração da página
st.set_page_config(page_title="Detector de Anomalias", layout="wide")

# Título e explicação
st.title("🕵️‍♂️ Detector de Anomalias em Transações Financeiras")
st.markdown("""
Este dashboard analisa automaticamente seu extrato bancário e detecta transações fora do padrão.  
Você pode usar o exemplo abaixo ou carregar seu próprio arquivo para análise.

Transações suspeitas são detectadas com base no **comportamento geral de valores**, sem limite fixo (como R$20.000).
""")

# Dados de exemplo carregados automaticamente
@st.cache_data
def carregar_dados_exemplo():
    return pd.DataFrame({
        "data": pd.date_range("2025-01-01", periods=100, freq="D"),
        "valor": [300 + i * 5 for i in range(100)]
    }).sample(frac=1).reset_index(drop=True)

dados = carregar_dados_exemplo()

# Opção para carregar arquivo
st.markdown("#### Ou carregue seu extrato bancário para análise:")
uploaded_file = st.file_uploader("📁 Envie seu CSV", type=["csv"])

if uploaded_file:
    try:
        dados = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()

# Verificação de colunas
if "valor" not in dados.columns or "data" not in dados.columns:
    st.error("O CSV deve conter as colunas 'data' e 'valor'.")
    st.stop()

# Conversão de data
dados["data"] = pd.to_datetime(dados["data"], errors='coerce')
dados.dropna(subset=["data", "valor"], inplace=True)

# IA para detecção de anomalias
modelo = IsolationForest(contamination=0.05, random_state=42)
dados["anomalia"] = modelo.fit_predict(dados[["valor"]])
dados["anomalia"] = dados["anomalia"] == -1  # True se for anomalia
dados["status"] = dados["anomalia"].map({True: "Anomalia", False: "Normal"})

# Métricas
total_transacoes = len(dados)
total_anomalias = dados["anomalia"].sum()
valor_total = dados["valor"].sum()
valor_anomalias = dados[dados["anomalia"]]["valor"].sum()

# Resumo
st.markdown("### 📊 Resumo das Transações")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Transações", f"{total_transacoes}")
col2.metric("Anomalias Detectadas", f"{total_anomalias}")
col3.metric("Valor Total", f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col4.metric("Valor das Anomalias", f"R$ {valor_anomalias:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Gráfico
st.markdown("### 📈 Transações ao Longo do Tempo")
fig = px.scatter(
    dados,
    x="data",
    y="valor",
    color="status",
    title="Transações Financeiras",
    labels={"data": "Data", "valor": "Valor (R$)"},
    hover_data=["valor", "status"]
)
st.plotly_chart(fig, use_container_width=True)

# Tabela
st.markdown("### 📋 Tabela de Transações")

def highlight_anomaly(row):
    return ['background-color: #ffcccc' if row["anomalia"] else '' for _ in row]

st.dataframe(
    dados.style.apply(highlight_anomaly, axis=1).format({
        "valor": lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "data": lambda d: d.strftime("%d/%m/%Y")
    }),
    use_container_width=True
)

# Download
st.markdown("### 💾 Baixe os dados analisados")
csv = dados.to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar CSV com anomalias", data=csv, file_name="resultado.csv", mime="text/csv")
