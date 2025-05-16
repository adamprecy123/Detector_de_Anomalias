import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

# Configuração da página
st.set_page_config(page_title="Detector de Anomalias", layout="wide")

# Injeção do CSS no Streamlit
st.markdown(
    """
    <style>
    h1 {
      font-size: 2.5rem;
      margin-bottom: 0.3em;
      color: #222;
    }
    .subtitulo {
      font-style: italic;
      color: #555;
      margin-bottom: 1.2em;
    }
    .upload-area {
      border: 2px dashed #aaa;
      padding: 1em;
      border-radius: 8px;
      margin-bottom: 2em;
      background-color: #f9f9f9;
    }
    .resumo-container {
      display: flex;
      justify-content: space-around;
      margin-bottom: 2em;
    }
    .resumo-item {
      background-color: #f0f4f8;
      padding: 1em 2em;
      border-radius: 10px;
      box-shadow: 1px 1px 5px #ddd;
      text-align: center;
      font-weight: 600;
    }
    .anomalias {
      color: #d9534f;
      font-weight: bold;
    }
    .botao-download {
      background-color: #007bff;
      color: white;
      padding: 10px 25px;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 10px;
      display: inline-block;
      font-weight: 600;
      text-align: center;
      text-decoration: none;
      border: none;
    }
    .table-container {
      max-height: 300px;
      overflow-y: auto;
      border: 1px solid #ddd;
      border-radius: 6px;
      margin-bottom: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título e explicação com classes CSS
st.markdown('<h1>🕵️‍♂️ Detector de Anomalias em Transações Financeiras</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Este dashboard analisa automaticamente seu extrato bancário e detecta transações fora do padrão.<br>'
    'Você pode usar o exemplo abaixo ou carregar seu próprio arquivo para análise.<br><br>'
    'Transações suspeitas são detectadas com base no <b>comportamento geral de valores</b>, sem limite fixo (como R$20.000).</p>',
    unsafe_allow_html=True
)

# Dados de exemplo carregados automaticamente
@st.cache_data
def carregar_dados_exemplo():
    return pd.DataFrame({
        "data": pd.date_range("2025-01-01", periods=100, freq="D"),
        "valor": [300 + i * 5 for i in range(100)]
    }).sample(frac=1).reset_index(drop=True)

dados = carregar_dados_exemplo()

# Área para upload com borda e fundo destacado
st.markdown('<div class="upload-area"><h4>Ou carregue seu extrato bancário para análise:</h4></div>', unsafe_allow_html=True)
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

# Resumo com container e estilos CSS
st.markdown('<h3>📊 Resumo das Transações</h3>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="resumo-container">
      <div class="resumo-item">Total de Transações<br><span>{total_transacoes}</span></div>
      <div class="resumo-item anomalias">Anomalias Detectadas<br><span>{total_anomalias}</span></div>
      <div class="resumo-item">Valor Total<br><span>R$ {valor_total:,.2f}</span></div>
      <div class="resumo-item anomalias">Valor das Anomalias<br><span>R$ {valor_anomalias:,.2f}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Gráfico
st.markdown('<h3>📈 Transações ao Longo do Tempo</h3>', unsafe_allow_html=True)
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

# Tabela com contêiner para scroll e estilização
st.markdown('<h3>📋 Tabela de Transações</h3>', unsafe_allow_html=True)

def highlight_anomaly(row):
    return ['background-color: #ffcccc' if row["anomalia"] else '' for _ in row]

st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.dataframe(
    dados.style.apply(highlight_anomaly, axis=1).format({
        "valor": lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "data": lambda d: d.strftime("%d/%m/%Y")
    }),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Download estilizado
st.markdown('<h3>💾 Baixe os dados analisados</h3>', unsafe_allow_html=True)
st.download_button("📥 Baixar CSV com anomalias", data=dados.to_csv(index=False).encode("utf-8"), file_name="resultado.csv", mime="text/csv")

