import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Detector de Anomalias", layout="wide")

# Título principal
st.title("🕵️‍♂️ Detector de Anomalias em Transações Financeiras")
st.markdown("Este dashboard analisa transações e identifica possíveis anomalias com valores acima de R$20.000.")

# Leitura dos dados
try:
    dados = pd.read_csv("dados.csv", parse_dates=["data"])
except Exception as e:
    st.error(f"Erro ao carregar o arquivo CSV: {e}")
    st.stop()

# Filtro de anomalias
limite_anomalia = 20000
dados["anomalia"] = dados["valor"] > limite_anomalia

# Exibição de métricas rápidas
total_transacoes = len(dados)
total_anomalias = dados["anomalia"].sum()
valor_total = dados["valor"].sum()
valor_anomalias = dados.loc[dados["anomalia"], "valor"].sum()

st.markdown("### 📊 Resumo das Transações")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Transações", f"{total_transacoes}")
col2.metric("Transações Anômalas", f"{total_anomalias}")
col3.metric("Valor Total", f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col4.metric("Valor das Anomalias", f"R$ {valor_anomalias:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Gráfico de evolução dos valores ao longo do tempo
st.markdown("### 📈 Visualização das Anomalias")

# Criando nova coluna para rótulo mais claro no gráfico
dados["status"] = dados["anomalia"].map({True: "Anomalia", False: "Normal"})

fig = px.scatter(
    dados,
    x="data",
    y="valor",
    color="status",
    title="Valores de Transações ao Longo do Tempo",
    labels={"data": "Data", "valor": "Valor (R$)"},
    hover_data={"valor": ":.2f", "data": True, "status": True},
)

fig.update_traces(marker=dict(size=10, line=dict(width=1, color="DarkSlateGrey")))
fig.update_layout(
    template="plotly_white",
    yaxis_tickformat=".2f",
    legend_title="Tipo de Transação",
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
)

st.plotly_chart(fig, use_container_width=True)

# Tabela com destaque para anomalias
st.markdown("### 📋 Tabela de Transações")
def highlight_anomaly(row):
    return ['background-color: #ffcccc' if row["anomalia"] else '' for _ in row]

st.dataframe(
    dados.style.apply(highlight_anomaly, axis=1).format({
        "valor": lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),

        "data": lambda d: d.strftime("%d/%m/%Y %H:%M")
    }),
    use_container_width=True
)
