# main.py — DropIntel: Dashboard Principal
# Execute com: streamlit run main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from config import (
    APP_NAME, CUSTOS_FIXOS, TOTAL_CUSTOS_FIXOS,
    MARKETPLACES, MARKETPLACE_CORES
)

# ─── Configuração da Página ───────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} · Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  /* Fundo escuro premium */
  .stApp {
    background: #0A0A0F;
    color: #E8E8F0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #0F0F1A !important;
    border-right: 1px solid #1E1E2E;
  }

  /* Cards de métrica */
  .metric-card {
    background: linear-gradient(135deg, #13131F 0%, #1A1A2E 100%);
    border: 1px solid #2A2A3E;
    border-radius: 16px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
  }
  .metric-card:hover { border-color: #4A4AFF; }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4A4AFF, #FF4AF8);
  }
  .metric-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: #6B6B8A;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 8px;
  }
  .metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #F0F0FF;
    line-height: 1.1;
  }
  .metric-delta {
    font-size: 13px;
    font-weight: 500;
    margin-top: 8px;
  }
  .delta-up   { color: #00E87A; }
  .delta-down { color: #FF4A6E; }

  /* Títulos de seção */
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #C0C0E0;
    letter-spacing: 0.5px;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* Header */
  .app-header {
    background: linear-gradient(135deg, #13131F 0%, #1A1A2E 100%);
    border: 1px solid #2A2A3E;
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .app-logo {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(90deg, #4A4AFF, #FF4AF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .app-subtitle {
    font-size: 14px;
    color: #6B6B8A;
    margin-top: 4px;
  }
  .status-badge {
    background: rgba(0, 232, 122, 0.1);
    border: 1px solid rgba(0, 232, 122, 0.3);
    color: #00E87A;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
  }

  /* Custo card */
  .custo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #1E1E2E;
    font-size: 14px;
  }
  .custo-nome { color: #9090B0; }
  .custo-valor { color: #F0F0FF; font-weight: 600; font-family: 'Syne', sans-serif; }

  /* Alerta de insight */
  .insight-card {
    background: linear-gradient(135deg, #1A1020 0%, #20102A 100%);
    border: 1px solid #4A2A6E;
    border-left: 4px solid #A855F7;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
  }
  .insight-title { color: #C084FC; font-weight: 600; font-size: 14px; margin-bottom: 4px; }
  .insight-text  { color: #9090B0; font-size: 13px; line-height: 1.5; }

  /* Oculta itens padrão do Streamlit */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; }
  [data-testid="stMetric"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── Geração de Dados Simulados ───────────────────────────────────────────────
@st.cache_data(ttl=300)
def gerar_dados_simulados():
    random.seed(42)

    # Vendas dos últimos 30 dias por marketplace
    hoje = datetime.now()
    datas = [hoje - timedelta(days=i) for i in range(29, -1, -1)]

    registros = []
    for data in datas:
        for mp in MARKETPLACES:
            base = {"Kwai Shop": 280, "TikTok Shop": 420, "Amazon": 650, "Shopee": 380}[mp]
            variacao = random.uniform(0.7, 1.4)
            num_pedidos = max(1, int(random.gauss(8, 3)))
            ticket = base * variacao
            gmv = ticket * num_pedidos
            taxa_mp = gmv * random.uniform(0.10, 0.18)
            custo_produto = gmv * random.uniform(0.40, 0.50)
            registros.append({
                "data": data.strftime("%Y-%m-%d"),
                "marketplace": mp,
                "pedidos": num_pedidos,
                "ticket_medio": round(ticket, 2),
                "gmv": round(gmv, 2),
                "taxa_marketplace": round(taxa_mp, 2),
                "custo_produto": round(custo_produto, 2),
                "receita_liquida": round(gmv - taxa_mp - custo_produto, 2),
            })

    df = pd.DataFrame(registros)
    df["data"] = pd.to_datetime(df["data"])
    return df

def calcular_metricas(df: pd.DataFrame):
    # Mês atual (30 dias)
    gmv_total        = df["gmv"].sum()
    receita_liquida  = df["receita_liquida"].sum()
    taxas_total      = df["taxa_marketplace"].sum()
    pedidos_total    = df["pedidos"].sum()
    lucro_liquido    = receita_liquida - TOTAL_CUSTOS_FIXOS
    ticket_medio     = df["ticket_medio"].mean()
    margem           = (lucro_liquido / gmv_total * 100) if gmv_total > 0 else 0

    return {
        "gmv_total":       gmv_total,
        "receita_liquida": receita_liquida,
        "lucro_liquido":   lucro_liquido,
        "taxas_total":     taxas_total,
        "pedidos_total":   int(pedidos_total),
        "ticket_medio":    ticket_medio,
        "margem":          margem,
    }

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 30px;'>
      <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:800;
                  background:linear-gradient(90deg,#4A4AFF,#FF4AF8);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
        ⚡ DropIntel
      </div>
      <div style='font-size:11px; color:#4A4A6A; margin-top:4px;'>v1.0 · MODO SIMULAÇÃO</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Navegação")
    pagina = st.radio("", [
        "📊 Dashboard Financeiro",
        "🤖 Gerador de Anúncios IA",
        "🔍 Auditoria da Loja",
        "💎 Mineração de Produtos",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 📅 Período")
    periodo = st.selectbox("", ["Últimos 30 dias", "Últimos 7 dias", "Este mês"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🏪 Marketplaces")
    mps_ativos = []
    for mp in MARKETPLACES:
        cor = MARKETPLACE_CORES[mp]
        checked = st.checkbox(mp, value=True, key=f"mp_{mp}")
        if checked:
            mps_ativos.append(mp)

    st.markdown("---")
    st.markdown("""
    <div style='background:#13131F; border:1px solid #2A2A3E; border-radius:12px; padding:16px; margin-top:8px;'>
      <div style='font-size:11px; color:#4A4A6A; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>
        💸 Custos Fixos
      </div>
    """, unsafe_allow_html=True)

    for nome, valor in CUSTOS_FIXOS.items():
        st.markdown(f"""
        <div class='custo-item'>
          <span class='custo-nome'>{nome}</span>
          <span class='custo-valor'>R$ {valor:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
      <div style='display:flex; justify-content:space-between; padding-top:12px; margin-top:4px;'>
        <span style='color:#E0E0FF; font-weight:700; font-size:14px;'>TOTAL</span>
        <span style='color:#FF4A6E; font-weight:800; font-size:16px; font-family:Syne,sans-serif;'>
          R$ {TOTAL_CUSTOS_FIXOS:.2f}
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Conteúdo Principal ───────────────────────────────────────────────────────
df = gerar_dados_simulados()

# Filtro de período
if periodo == "Últimos 7 dias":
    df = df[df["data"] >= datetime.now() - timedelta(days=7)]
elif periodo == "Este mês":
    df = df[df["data"].dt.month == datetime.now().month]

# Filtro de marketplaces
if mps_ativos:
    df = df[df["marketplace"].isin(mps_ativos)]

metricas = calcular_metricas(df)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='app-header'>
  <div>
    <div class='app-logo'>⚡ DropIntel</div>
    <div class='app-subtitle'>Central de Inteligência para Dropshipping · {periodo}</div>
  </div>
  <div>
    <span class='status-badge'>● DADOS SIMULADOS</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Seção: Página Ativa ───────────────────────────────────────────────────────
if "Dashboard" in pagina:

    # KPIs Principais
    st.markdown("<div class='section-title'>📈 Visão Geral do Período</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    kpis = [
        (col1, "💰 GMV Total",       f"R$ {metricas['gmv_total']:,.2f}",      "▲ +12.4%", True),
        (col2, "📦 Pedidos",          f"{metricas['pedidos_total']:,}",         "▲ +8.1%",  True),
        (col3, "🎯 Ticket Médio",     f"R$ {metricas['ticket_medio']:.2f}",    "▲ +3.7%",  True),
        (col4, "📊 Taxas MP",         f"R$ {metricas['taxas_total']:,.2f}",    "▼ -1.2%",  False),
    ]

    for col, label, valor, delta, positivo in kpis:
        with col:
            cor_delta = "delta-up" if positivo else "delta-down"
            st.markdown(f"""
            <div class='metric-card'>
              <div class='metric-label'>{label}</div>
              <div class='metric-value'>{valor}</div>
              <div class='metric-delta {cor_delta}'>{delta} vs. período anterior</div>
            </div>
            """, unsafe_allow_html=True)

    # KPIs Financeiros
    st.markdown("<div class='section-title'>💵 Resultado Financeiro</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    fin_kpis = [
        (col1, "📥 Receita Líquida",  f"R$ {metricas['receita_liquida']:,.2f}", "▲ +9.8%",  True),
        (col2, "🏦 Custos Fixos",     f"R$ {TOTAL_CUSTOS_FIXOS:.2f}",           "= Fixo",   None),
        (col3, "✅ Lucro Líquido",    f"R$ {metricas['lucro_liquido']:,.2f}",   f"Margem {metricas['margem']:.1f}%", metricas['lucro_liquido'] > 0),
    ]

    for col, label, valor, delta, positivo in fin_kpis:
        with col:
            if positivo is None:
                cor = "delta-down"
            elif positivo:
                cor = "delta-up"
            else:
                cor = "delta-down"
            st.markdown(f"""
            <div class='metric-card'>
              <div class='metric-label'>{label}</div>
              <div class='metric-value'>{valor}</div>
              <div class='metric-delta {cor}'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    # Gráficos
    st.markdown("<div class='section-title'>📉 Evolução do GMV por Marketplace</div>", unsafe_allow_html=True)

    df_daily = df.groupby(["data", "marketplace"])["gmv"].sum().reset_index()

    fig_gmv = px.line(
        df_daily, x="data", y="gmv", color="marketplace",
        color_discrete_map=MARKETPLACE_CORES,
        labels={"data": "", "gmv": "GMV (R$)", "marketplace": ""},
    )
    fig_gmv.update_layout(
        plot_bgcolor="#0D0D1A",
        paper_bgcolor="#0D0D1A",
        font=dict(color="#9090B0", family="DM Sans"),
        legend=dict(orientation="h", y=-0.15, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#1E1E2E", showgrid=True),
        yaxis=dict(gridcolor="#1E1E2E", showgrid=True),
        margin=dict(l=0, r=0, t=20, b=0),
        hovermode="x unified",
    )
    fig_gmv.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig_gmv, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>🥧 GMV por Marketplace</div>", unsafe_allow_html=True)
        df_mp = df.groupby("marketplace")["gmv"].sum().reset_index()
        fig_pie = px.pie(
            df_mp, names="marketplace", values="gmv",
            color="marketplace", color_discrete_map=MARKETPLACE_CORES,
            hole=0.55,
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9090B0", family="DM Sans"),
            legend=dict(orientation="v", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_pie.update_traces(textfont_color="#F0F0FF")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>📊 Receita vs. Custos</div>", unsafe_allow_html=True)
        categorias   = ["GMV Total", "Taxas MP", "Custo Produto", "Custos Fixos", "Lucro Líquido"]
        valores      = [
            metricas["gmv_total"],
            -metricas["taxas_total"],
            -df["custo_produto"].sum(),
            -TOTAL_CUSTOS_FIXOS,
            metricas["lucro_liquido"],
        ]
        cores_bar = ["#4A4AFF", "#FF4A6E", "#FF9944", "#FF4AF8", "#00E87A"]

        fig_bar = go.Figure(go.Bar(
            x=categorias, y=valores,
            marker_color=cores_bar,
            text=[f"R$ {abs(v):,.0f}" for v in valores],
            textposition="outside",
            textfont=dict(color="#C0C0E0", size=11),
        ))
        fig_bar.update_layout(
            plot_bgcolor="#0D0D1A", paper_bgcolor="#0D0D1A",
            font=dict(color="#9090B0", family="DM Sans"),
            showlegend=False,
            xaxis=dict(gridcolor="#1E1E2E"),
            yaxis=dict(gridcolor="#1E1E2E", showgrid=True),
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Insights IA (simulados)
    st.markdown("<div class='section-title'>🤖 Insights Automáticos (prévia)</div>", unsafe_allow_html=True)

    insights = [
        ("⚠️ Queda de Performance", "TikTok Shop registrou queda de 18% no GMV nos últimos 3 dias. Verifique o orçamento de tráfego pago ou atualize a capa do produto mais vendido."),
        ("🚀 Oportunidade Detectada", "Shopee apresenta ticket médio 23% acima da meta esta semana. Considere aumentar o preço em R$ 15–20 sem impacto na conversão."),
        ("📦 Estoque em Risco", "Produto 'Kit Organizador' tem velocidade de venda alta na Amazon. Reforce o pedido ao fornecedor nos próximos 2 dias."),
    ]
    for titulo, texto in insights:
        st.markdown(f"""
        <div class='insight-card'>
          <div class='insight-title'>{titulo}</div>
          <div class='insight-text'>{texto}</div>
        </div>
        """, unsafe_allow_html=True)

    # Tabela de vendas
    st.markdown("<div class='section-title'>📋 Detalhamento por Marketplace</div>", unsafe_allow_html=True)
    df_resumo = df.groupby("marketplace").agg(
        Pedidos=("pedidos", "sum"),
        GMV=("gmv", "sum"),
        Taxas=("taxa_marketplace", "sum"),
        Receita_Liquida=("receita_liquida", "sum"),
    ).reset_index()
    df_resumo["Margem (%)"] = (df_resumo["Receita_Liquida"] / df_resumo["GMV"] * 100).round(1)
    df_resumo = df_resumo.rename(columns={"marketplace": "Marketplace"})
    for col in ["GMV", "Taxas", "Receita_Liquida"]:
        df_resumo[col] = df_resumo[col].map("R$ {:,.2f}".format)

    st.dataframe(
        df_resumo, use_container_width=True, hide_index=True,
        column_config={
            "Margem (%)": st.column_config.ProgressColumn(
                "Margem %", format="%.1f%%", min_value=0, max_value=60
            )
        }
    )

elif "Anúncios" in pagina:
    st.markdown("""
    <div style='text-align:center; padding:80px 0;'>
      <div style='font-size:64px; margin-bottom:16px;'>🤖</div>
      <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:700; color:#C0C0E0;'>
        Gerador de Anúncios IA
      </div>
      <div style='color:#6B6B8A; margin-top:8px; font-size:15px;'>
        Integração com Google Gemini · Em breve no Passo 2
      </div>
    </div>
    """, unsafe_allow_html=True)

elif "Auditoria" in pagina:
    st.markdown("""
    <div style='text-align:center; padding:80px 0;'>
      <div style='font-size:64px; margin-bottom:16px;'>🔍</div>
      <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:700; color:#C0C0E0;'>
        Auditoria da Loja em Tempo Real
      </div>
      <div style='color:#6B6B8A; margin-top:8px; font-size:15px;'>
        Análise automática com IA · Em breve no Passo 3
      </div>
    </div>
    """, unsafe_allow_html=True)

elif "Mineração" in pagina:
    st.markdown("""
    <div style='text-align:center; padding:80px 0;'>
      <div style='font-size:64px; margin-bottom:16px;'>💎</div>
      <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:700; color:#C0C0E0;'>
        Mineração de Produtos Vencedores
      </div>
      <div style='color:#6B6B8A; margin-top:8px; font-size:15px;'>
        Web Scraping com Playwright · Em breve no Passo 4
      </div>
    </div>
    """, unsafe_allow_html=True)
