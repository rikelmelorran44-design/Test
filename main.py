# main.py — Rikelme Drop · Plataforma Desktop
# Execute: streamlit run main.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from config import CUSTOS_FIXOS, TOTAL_CUSTOS_FIXOS, MARKETPLACES, MARKETPLACE_CORES

st.set_page_config(
    page_title="Rikelme Drop",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #07080F; color: #E0E0F0; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: #0C0D18 !important;
  border-right: 1px solid #1A1A30;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* Remove itens padrão */
#MainMenu, footer, header { visibility: hidden; }
.modebar, .modebar-container { display: none !important; }

/* ── Título da sidebar ── */
.brand {
  font-family: 'Syne', sans-serif;
  font-size: 22px;
  font-weight: 800;
  background: linear-gradient(90deg, #7B7BFF, #FF5AF5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 2px;
}
.brand-sub { font-size: 11px; color: #3A3A60; margin-bottom: 20px; }

/* ── KPI Cards ── */
.kpi {
  background: linear-gradient(135deg, #0E0F1E, #131428);
  border: 1px solid #1E1E38;
  border-radius: 16px;
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
  height: 100%;
}
.kpi::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #7B7BFF, #FF5AF5);
}
.kpi-label {
  font-size: 11px; font-weight: 600; color: #3A3A60;
  text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px;
}
.kpi-value {
  font-family: 'Syne', sans-serif;
  font-size: 26px; font-weight: 800; color: #F0F0FF; line-height: 1.1;
}
.kpi-delta-up   { color: #00D97A; font-size: 12px; font-weight: 600; margin-top: 6px; }
.kpi-delta-down { color: #FF4A6E; font-size: 12px; font-weight: 600; margin-top: 6px; }
.kpi-delta-neu  { color: #5A5A90; font-size: 12px; margin-top: 6px; }

/* ── Seção título ── */
.sec {
  font-family: 'Syne', sans-serif;
  font-size: 13px; font-weight: 700; color: #3A3A60;
  text-transform: uppercase; letter-spacing: 1px;
  margin: 28px 0 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #1A1A30;
}

/* ── Insight card ── */
.ins {
  border-radius: 12px; padding: 14px 18px;
  margin-bottom: 8px; border-left: 3px solid;
}
.ins-w { background: #18120A; border-color: #F59E0B; }
.ins-g { background: #081510; border-color: #10B981; }
.ins-b { background: #0A0A1A; border-color: #7B7BFF; }
.ins-title { font-size: 13px; font-weight: 700; margin-bottom: 4px; }
.ins-text  { font-size: 12px; color: #5A5A90; line-height: 1.6; }
.c-w { color: #F59E0B; } .c-g { color: #10B981; } .c-b { color: #8080FF; }

/* ── Custo row ── */
.cost-row {
  display: flex; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid #131328; font-size: 13px;
}
.c-name { color: #4A4A80; } .c-val { color: #D0D0F0; font-weight: 600; }

/* ── Tabela ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Coming soon ── */
.cs {
  text-align: center; padding: 80px 40px;
  background: #0C0D18; border: 1px solid #1A1A30;
  border-radius: 16px; margin-top: 20px;
}
.cs-icon  { font-size: 56px; margin-bottom: 16px; }
.cs-title { font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:#C0C0E0; margin-bottom:10px; }
.cs-sub   { font-size:14px; color:#3A3A60; line-height:1.7; max-width:500px; margin:0 auto; }

/* Plotly dark */
.js-plotly-plot .plotly { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Dados simulados realistas ─────────────────────────────────────────────────
@st.cache_data(ttl=300)
def dados():
    random.seed(7)
    hoje = datetime.now()
    rows = []
    bases = {"Kwai Shop": 85, "TikTok Shop": 110, "Amazon": 140, "Shopee": 95}
    for i in range(29, -1, -1):
        d = hoje - timedelta(days=i)
        for mp in MARKETPLACES:
            pedidos = max(1, int(random.gauss(5, 2)))
            ticket  = bases[mp] * random.uniform(0.8, 1.3)
            gmv     = ticket * pedidos
            taxa    = gmv * random.uniform(0.12, 0.18)
            custo   = gmv * random.uniform(0.38, 0.48)
            rows.append({
                "data": d, "marketplace": mp,
                "pedidos": pedidos, "ticket": round(ticket, 2),
                "gmv": round(gmv, 2), "taxa": round(taxa, 2),
                "custo_produto": round(custo, 2),
                "receita_liq": round(gmv - taxa - custo, 2),
            })
    return pd.DataFrame(rows)

df_full = dados()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='brand'>🛍️ Rikelme Drop</div>", unsafe_allow_html=True)
    st.markdown("<div class='brand-sub'>Plataforma de Dropshipping · v1.0</div>", unsafe_allow_html=True)

    pagina = st.radio("Navegação", [
        "📊 Dashboard",
        "💰 Financeiro",
        "🤖 Gerador de Anúncios",
        "🔍 Auditoria da Loja",
        "💎 Mineração de Produtos",
    ])

    st.markdown("---")
    st.markdown("**📅 Período**")
    periodo = st.selectbox("", ["Últimos 30 dias", "Últimos 7 dias", "Este mês"],
                           label_visibility="collapsed")

    st.markdown("**🏪 Marketplaces**")
    mps_ativos = []
    for mp in MARKETPLACES:
        if st.checkbox(mp, value=True, key=f"mp_{mp}"):
            mps_ativos.append(mp)

    st.markdown("---")
    st.markdown("**💸 Custos Fixos Mensais**")
    for nome, val in CUSTOS_FIXOS.items():
        st.markdown(f"""
        <div class='cost-row'>
          <span class='c-name'>{nome}</span>
          <span class='c-val'>R$ {val:.2f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex;justify-content:space-between;padding-top:12px;'>
      <span style='color:#D0D0F0;font-weight:700;font-size:13px;'>TOTAL</span>
      <span style='color:#FF4A6E;font-weight:800;font-family:Syne,sans-serif;font-size:16px;'>
        R$ {TOTAL_CUSTOS_FIXOS:.2f}
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='font-size:10px;color:#2A2A50;text-align:center;'>● DADOS SIMULADOS · {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>",
                unsafe_allow_html=True)

# ── Filtros ───────────────────────────────────────────────────────────────────
df = df_full.copy()
if periodo == "Últimos 7 dias":
    df = df[df["data"] >= datetime.now() - timedelta(days=7)]
elif periodo == "Este mês":
    df = df[df["data"].dt.month == datetime.now().month]
if mps_ativos:
    df = df[df["marketplace"].isin(mps_ativos)]

gmv     = df["gmv"].sum()
pedidos = int(df["pedidos"].sum())
ticket  = df["ticket"].mean()
taxas   = df["taxa"].sum()
custo_p = df["custo_produto"].sum()
rec_liq = df["receita_liq"].sum()
lucro   = rec_liq - TOTAL_CUSTOS_FIXOS
margem  = lucro / gmv * 100 if gmv else 0

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📊 Dashboard":

    st.markdown(f"## 📊 Dashboard  <span style='font-size:14px;color:#3A3A60;font-weight:400;'>· {periodo}</span>", unsafe_allow_html=True)

    # KPIs linha 1
    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "💰 GMV Total",    f"R$ {gmv:,.2f}",       "▲ +12.4% vs anterior", True),
        (c2, "📦 Pedidos",       f"{pedidos:,}",          "▲ +8.1% vs anterior",  True),
        (c3, "🎯 Ticket Médio",  f"R$ {ticket:.2f}",     "▲ +3.7% vs anterior",  True),
        (c4, "📊 Taxas MP",      f"R$ {taxas:,.2f}",     "~14% do GMV",           None),
    ]
    for col, label, valor, delta, positivo in kpis:
        with col:
            cor = "kpi-delta-up" if positivo else ("kpi-delta-down" if positivo is False else "kpi-delta-neu")
            st.markdown(f"""
            <div class='kpi'>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value'>{valor}</div>
              <div class='{cor}'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)

    # KPIs linha 2
    c1, c2, c3 = st.columns(3)
    fin = [
        (c1, "📥 Receita Líquida", f"R$ {rec_liq:,.2f}", "▲ +9.8% vs anterior",   True),
        (c2, "🔒 Custos Fixos",    f"R$ {TOTAL_CUSTOS_FIXOS:.2f}", "Valor fixo mensal", None),
        (c3, "✅ Lucro Líquido",   f"R$ {lucro:,.2f}",   f"Margem: {margem:.1f}%", lucro > 0),
    ]
    for col, label, valor, delta, positivo in fin:
        with col:
            cor = "kpi-delta-up" if positivo else ("kpi-delta-down" if positivo is False else "kpi-delta-neu")
            cor_val = "#00D97A" if (positivo is True) else ("#FF4A6E" if positivo is False else "#F0F0FF")
            st.markdown(f"""
            <div class='kpi'>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value' style='color:{cor_val}'>{valor}</div>
              <div class='{cor}'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    # Gráficos linha 1
    st.markdown("<div class='sec'>📈 Evolução do GMV por Marketplace</div>", unsafe_allow_html=True)
    df_daily = df.groupby(["data","marketplace"])["gmv"].sum().reset_index()
    fig_line = px.line(df_daily, x="data", y="gmv", color="marketplace",
                       color_discrete_map=MARKETPLACE_CORES,
                       labels={"data":"","gmv":"GMV (R$)","marketplace":""})
    fig_line.update_layout(
        height=300, plot_bgcolor="#0A0B15", paper_bgcolor="#0A0B15",
        font=dict(color="#5A5A90", family="Inter"),
        legend=dict(orientation="h", y=-0.2, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#131328"), yaxis=dict(gridcolor="#131328"),
        margin=dict(l=0, r=0, t=10, b=0), hovermode="x unified",
    )
    fig_line.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    # Gráficos linha 2
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sec'>🥧 GMV por Marketplace</div>", unsafe_allow_html=True)
        df_mp = df.groupby("marketplace")["gmv"].sum().reset_index()
        fig_pie = px.pie(df_mp, names="marketplace", values="gmv",
                         color="marketplace", color_discrete_map=MARKETPLACE_CORES, hole=0.55)
        fig_pie.update_layout(
            height=280, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#9090B0", family="Inter"),
            legend=dict(orientation="h", bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("<div class='sec'>💹 Receita vs. Custos</div>", unsafe_allow_html=True)
        cats = ["GMV Total","Taxas MP","Custo Produto","Custos Fixos","Lucro Líquido"]
        vals = [gmv, -taxas, -custo_p, -TOTAL_CUSTOS_FIXOS, lucro]
        cores_b = ["#7B7BFF","#FF4A6E","#FF9944","#FF5AF5","#00D97A" if lucro>0 else "#FF4A6E"]
        fig_bar = go.Figure(go.Bar(x=cats, y=vals, marker_color=cores_b,
                                   text=[f"R$ {abs(v):,.0f}" for v in vals],
                                   textposition="outside",
                                   textfont=dict(color="#9090B0", size=11)))
        fig_bar.update_layout(
            height=280, plot_bgcolor="#0A0B15", paper_bgcolor="#0A0B15",
            font=dict(color="#5A5A90", family="Inter"), showlegend=False,
            xaxis=dict(gridcolor="#131328"), yaxis=dict(gridcolor="#131328", showgrid=True),
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # Tabela
    st.markdown("<div class='sec'>📋 Detalhamento por Marketplace</div>", unsafe_allow_html=True)
    df_tab = df.groupby("marketplace").agg(
        Pedidos=("pedidos","sum"), GMV=("gmv","sum"),
        Taxas=("taxa","sum"), Receita_Liq=("receita_liq","sum")
    ).reset_index()
    df_tab["Margem (%)"] = (df_tab["Receita_Liq"] / df_tab["GMV"] * 100).round(1)
    df_tab = df_tab.rename(columns={"marketplace":"Marketplace","Receita_Liq":"Receita Líq."})
    for c in ["GMV","Taxas","Receita Líq."]:
        df_tab[c] = df_tab[c].map("R$ {:,.2f}".format)
    st.dataframe(df_tab, use_container_width=True, hide_index=True,
                 column_config={"Margem (%)": st.column_config.ProgressColumn(
                     "Margem %", format="%.1f%%", min_value=0, max_value=60)})

    # Insights
    st.markdown("<div class='sec'>🤖 Insights Automáticos</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    insights = [
        (col1, "ins-w", "c-w", "⚠️ Queda de Performance",
         "TikTok Shop registrou queda de 18% no GMV nos últimos 3 dias. Atualize a capa do produto mais vendido ou revise o preço."),
        (col2, "ins-g", "c-g", "🚀 Oportunidade Detectada",
         "Shopee apresenta ticket médio 23% acima da meta esta semana. Considere aumentar o preço em R$ 15–20."),
        (col3, "ins-b", "c-b", "📦 Estoque em Risco",
         "Produto 'Kit Organizador' tem alta velocidade de venda na Amazon. Reforce o pedido ao fornecedor."),
    ]
    for col, cls, ccls, titulo, texto in insights:
        with col:
            st.markdown(f"""
            <div class='ins {cls}'>
              <div class='ins-title {ccls}'>{titulo}</div>
              <div class='ins-text'>{texto}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FINANCEIRO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "💰 Financeiro":

    st.markdown("## 💰 Painel Financeiro", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, label, valor, delta, positivo in [
        (c1, "✅ Lucro Líquido",   f"R$ {lucro:,.2f}",   f"Margem {margem:.1f}%",  lucro>0),
        (c2, "📥 Receita Líquida", f"R$ {rec_liq:,.2f}", "▲ +9.8%",                True),
        (c3, "📊 Taxas MP",        f"R$ {taxas:,.2f}",   f"{taxas/gmv*100:.1f}% do GMV", None),
        (c4, "🔒 Custos Fixos",    f"R$ {TOTAL_CUSTOS_FIXOS:.2f}", "Valor fixo mensal", None),
    ]:
        with col:
            cor = "kpi-delta-up" if positivo else ("kpi-delta-down" if positivo is False else "kpi-delta-neu")
            cor_val = "#00D97A" if positivo is True else ("#FF4A6E" if positivo is False else "#F0F0FF")
            st.markdown(f"""
            <div class='kpi'>
              <div class='kpi-label'>{label}</div>
              <div class='kpi-value' style='color:{cor_val}'>{valor}</div>
              <div class='{cor}'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("<div class='sec'>📊 Composição do Resultado</div>", unsafe_allow_html=True)
        cats = ["GMV Total","− Taxas MP","− Custo Produto","− Custos Fixos","= Lucro"]
        vals = [gmv, -taxas, -custo_p, -TOTAL_CUSTOS_FIXOS, lucro]
        cores_b = ["#7B7BFF","#FF4A6E","#FF9944","#FF5AF5","#00D97A" if lucro>0 else "#FF4A6E"]
        fig3 = go.Figure(go.Bar(x=cats, y=vals, marker_color=cores_b,
                                text=[f"R$ {abs(v):,.2f}" for v in vals],
                                textposition="outside",
                                textfont=dict(color="#9090B0", size=11)))
        fig3.update_layout(
            height=320, plot_bgcolor="#0A0B15", paper_bgcolor="#0A0B15",
            font=dict(color="#5A5A90"), showlegend=False,
            xaxis=dict(gridcolor="#131328"), yaxis=dict(gridcolor="#131328"),
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("<div class='sec'>🔒 Custos Fixos Mensais</div>", unsafe_allow_html=True)
        st.markdown("<div class='kpi' style='padding:20px 22px'>", unsafe_allow_html=True)
        for nome, val in CUSTOS_FIXOS.items():
            st.markdown(f"""
            <div class='cost-row'>
              <span class='c-name'>{nome}</span>
              <span class='c-val'>R$ {val:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;padding-top:14px;'>
          <span style='color:#E0E0FF;font-weight:700;'>TOTAL MENSAL</span>
          <span style='color:#FF4A6E;font-weight:800;font-family:Syne,sans-serif;font-size:18px;'>
            R$ {TOTAL_CUSTOS_FIXOS:.2f}
          </span>
        </div></div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sec'>🤖 Alertas</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='ins ins-g'>
          <div class='ins-title c-g'>✅ Operação Lucrativa</div>
          <div class='ins-text'>Margem de {margem:.1f}% cobre todos os custos fixos com folga.</div>
        </div>
        <div class='ins ins-b'>
          <div class='ins-title c-b'>💡 Meta: R$ 2.000 de lucro</div>
          <div class='ins-text'>Você precisa de R$ {(2000+TOTAL_CUSTOS_FIXOS)/0.41:,.0f} de GMV mensal para atingir essa meta.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ANÚNCIOS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🤖 Gerador de Anúncios":
    st.markdown("## 🤖 Gerador de Anúncios com IA")
    st.markdown("""
    <div class='cs'>
      <div class='cs-icon'>🤖</div>
      <div class='cs-title'>Gerador de Anúncios com Google Gemini</div>
      <div class='cs-sub'>
        Cole o link do produto do fornecedor e a IA vai gerar automaticamente:<br>
        ✅ Títulos otimizados para SEO (até 60 caracteres)<br>
        ✅ Descrições persuasivas com gatilhos mentais<br>
        ✅ Versões adaptadas para cada marketplace
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔜 Em construção — Passo 2 do projeto (integração com API do Google Gemini)")

# ══════════════════════════════════════════════════════════════════════════════
# AUDITORIA
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🔍 Auditoria da Loja":
    st.markdown("## 🔍 Auditoria da Loja em Tempo Real")
    st.markdown("""
    <div class='cs'>
      <div class='cs-icon'>🔍</div>
      <div class='cs-title'>Auditoria Inteligente com IA</div>
      <div class='cs-sub'>
        A IA vai analisar seus dados de vendas e tráfego do Bling ERP e gerar insights automáticos:<br>
        ✅ Produtos com queda de performance<br>
        ✅ Sugestões de preço e capa<br>
        ✅ Alertas de oportunidade por marketplace
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔜 Em construção — Passo 3 do projeto (integração com Bling API v3 + Gemini)")

# ══════════════════════════════════════════════════════════════════════════════
# MINERAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "💎 Mineração de Produtos":
    st.markdown("## 💎 Mineração de Produtos Vencedores")
    st.markdown("""
    <div class='cs'>
      <div class='cs-icon'>💎</div>
      <div class='cs-title'>Mineração Automática de Produtos</div>
      <div class='cs-sub'>
        Web scraping automático monitorando os melhores produtos:<br>
        ✅ Mais vendidos da Shopee e Amazon<br>
        ✅ Tendências do TikTok Creative Center<br>
        ✅ Alertas de produtos virais em tempo real
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("🔜 Em construção — Passo 4 do projeto (Playwright + BeautifulSoup)")
