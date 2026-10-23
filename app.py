# -*- coding: utf-8 -*-
"""
Tema visual do FluxoClaro.
Paleta oficial: #001089, #9918ed, #6e1aac | fundos claros: #e8e9f9, #b9c2f9, #dfd3ea, #e9e8ea
Assinatura visual: cantos arredondados com o canto inferior esquerdo "mordido" (pequeno),
sombras tingidas de azul/roxo e uma faixa de cor no topo de cada cartão.
"""

import streamlit as st

COR_MAPA = {
    "Entradas": "#001089",
    "Despesas Essenciais": "#9918ed",
    "Despesas Não Essenciais": "#c9a4f2",
}

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

:root{
  --azul:#001089; --roxo:#9918ed; --roxo-esc:#6e1aac;
  --lav:#e8e9f9; --peri:#b9c2f9; --lilas:#dfd3ea; --cinza:#e9e8ea;
  --raio:22px 22px 22px 6px;
  --sombra:0 10px 30px -12px rgba(0,16,137,.28);
}

html, body, [class*="css"]{ font-family:'Poppins',sans-serif; color:var(--azul); }

.stApp{
  background:
    radial-gradient(900px 420px at 100% -5%, rgba(153,24,237,.14), transparent 60%),
    radial-gradient(700px 500px at -5% 35%, rgba(185,194,249,.55), transparent 60%),
    #F6F7FD;
}

/* ---------- Títulos ---------- */
h1{ font-weight:900 !important; color:var(--azul) !important; letter-spacing:-.02em; }
h2,h3,h4{ font-weight:800 !important; color:var(--azul) !important; letter-spacing:-.01em; }

/* ---------- Hero ---------- */
.fc-hero{
  position:relative; overflow:hidden; color:#fff;
  padding:30px 36px 28px; margin:-.5rem 0 1.6rem;
  border-radius:30px 30px 30px 8px;
  background:linear-gradient(120deg,#001089 0%,#3a1aa8 45%,#9918ed 100%);
  box-shadow:0 22px 40px -18px rgba(0,16,137,.55);
}
.fc-hero::before{
  content:""; position:absolute; right:-70px; top:-90px; width:300px; height:300px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.28),transparent 65%);
}
.fc-hero::after{
  content:""; position:absolute; right:140px; bottom:-120px; width:240px; height:240px; border-radius:50%;
  border:34px solid rgba(255,255,255,.10);
}
.fc-hero h1{ color:#fff !important; margin:0; font-size:2.1rem; line-height:1.15; position:relative; z-index:1; padding:0; }
.fc-hero p{ margin:.35rem 0 0; font-weight:500; opacity:.85; position:relative; z-index:1; }
.fc-chip{
  display:inline-block; margin-top:14px; padding:6px 16px; border-radius:999px; position:relative; z-index:1;
  background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.35);
  font-weight:600; font-size:.85rem; backdrop-filter:blur(6px);
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#FFFFFF 0%,#f4effb 100%) !important;
  border-right:none !important;
  border-radius:0 32px 32px 0;
  box-shadow:10px 0 40px -14px rgba(110,26,172,.25);
}
[data-testid="stSidebar"] > div:first-child{ padding:1rem 1.2rem; }
[data-testid="stSidebar"] h2{ font-size:1.25rem; }

/* ---------- Métricas ---------- */
div[data-testid="stMetric"]{
  position:relative; overflow:hidden;
  background:#fff; border:1px solid var(--lav);
  border-radius:var(--raio); padding:20px 18px 16px;
  box-shadow:var(--sombra);
  transition:transform .18s ease, box-shadow .18s ease;
}
div[data-testid="stMetric"]:hover{ transform:translateY(-3px); box-shadow:0 16px 34px -12px rgba(153,24,237,.38); }
div[data-testid="stMetric"]::before{
  content:""; position:absolute; left:0; right:0; top:0; height:6px;
  background:var(--faixa,linear-gradient(90deg,#001089,#9918ed));
}
div[data-testid="stMetricLabel"] p{ font-weight:600; font-size:.8rem; color:var(--roxo-esc) !important; }
div[data-testid="stMetricValue"]{ color:var(--azul) !important; font-weight:800 !important; font-size:1.45rem !important; }

/* uma faixa de cor diferente por métrica */
[data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#001089,#4a5ee0); }
[data-testid="stHorizontalBlock"] > div:nth-child(2) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#6e1aac,#9918ed); }
[data-testid="stHorizontalBlock"] > div:nth-child(3) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#9918ed,#d9a3ff); }
[data-testid="stHorizontalBlock"] > div:nth-child(4) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#4a5ee0,#b9c2f9); }
[data-testid="stHorizontalBlock"] > div:nth-child(5) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#001089,#9918ed); }
[data-testid="stHorizontalBlock"] > div:nth-child(6) [data-testid="stMetric"]{ --faixa:linear-gradient(90deg,#9918ed,#001089); }

/* ---------- Abas em pílula ---------- */
[data-baseweb="tab-list"]{
  gap:8px; background:#fff; padding:6px; border-radius:999px;
  border:1px solid var(--lav); box-shadow:var(--sombra); width:fit-content; max-width:100%;
}
[data-baseweb="tab"]{ border-radius:999px !important; padding:8px 20px !important; font-weight:600; color:var(--azul); height:auto; }
[data-baseweb="tab"][aria-selected="true"]{
  background:linear-gradient(120deg,#001089,#9918ed) !important; color:#fff !important;
  box-shadow:0 8px 18px -8px rgba(153,24,237,.7);
}
[data-baseweb="tab"][aria-selected="true"] p{ color:#fff !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"]{ display:none !important; }

/* ---------- Campos ---------- */
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"]{
  border-radius:14px !important; border-color:var(--peri) !important; background:#fff !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within{
  border-color:var(--roxo) !important; box-shadow:0 0 0 4px rgba(153,24,237,.15) !important;
}
label p{ font-weight:600 !important; color:var(--azul) !important; }

/* ---------- Botões ---------- */
.stButton > button{
  border-radius:999px; font-weight:700; padding:.55rem 1.2rem;
  border:2px solid var(--peri); background:#fff; color:var(--azul);
  transition:all .18s ease;
}
.stButton > button:hover{ border-color:var(--roxo); color:var(--roxo); transform:translateY(-1px); }
.stButton > button[kind="primary"]{
  border:none; color:#fff; background:linear-gradient(120deg,#001089,#9918ed);
  box-shadow:0 12px 22px -10px rgba(153,24,237,.75);
}
.stButton > button[kind="primary"]:hover{ color:#fff; filter:brightness(1.08); }

/* ---------- Avisos (totais) ---------- */
div[data-testid="stAlert"]{
  background:linear-gradient(100deg,var(--lav),#f3eefb) !important;
  color:var(--azul) !important; border:none !important;
  border-left:6px solid var(--roxo) !important;
  border-radius:16px 16px 16px 4px !important;
}
div[data-testid="stAlert"] *{ color:var(--azul) !important; }

/* ---------- Expander, gráficos, progresso, divisor ---------- */
details{ background:#fff; border:1px solid var(--peri) !important; border-radius:18px !important; box-shadow:var(--sombra); }
div[data-testid="stPlotlyChart"]{
  background:#fff; border:1px solid var(--lav); border-radius:var(--raio);
  padding:14px; box-shadow:var(--sombra);
}
div[data-testid="stProgress"] > div > div{ background:var(--lav) !important; border-radius:999px; height:12px; }
div[data-testid="stProgress"] > div > div > div{ background:linear-gradient(90deg,#001089,#9918ed) !important; border-radius:999px; }
hr{ border:none !important; height:3px !important; border-radius:3px; background:linear-gradient(90deg,#9918ed,#b9c2f9 55%,transparent) !important; opacity:.55; }
</style>
"""


def aplicar_tema():
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(titulo: str, subtitulo: str = "", chip: str = ""):
    chip_html = f'<span class="fc-chip">{chip}</span>' if chip else ""
    sub_html = f"<p>{subtitulo}</p>" if subtitulo else ""
    st.markdown(
        f'<div class="fc-hero"><h1>{titulo}</h1>{sub_html}{chip_html}</div>',
        unsafe_allow_html=True,
    )


def estilizar_figura(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color="#001089"),
        title=dict(font=dict(size=17, family="Poppins, sans-serif"), x=0.01),
        legend=dict(orientation="h", y=1.14, x=0, title_text=""),
        margin=dict(t=90, l=10, r=10, b=10),
        hoverlabel=dict(bgcolor="#001089", font_color="#fff", font_family="Poppins"),
        bargap=0.28,
    )
    fig.update_xaxes(showgrid=False, linecolor="#b9c2f9", title_text="")
    fig.update_yaxes(gridcolor="#e8e9f9", zeroline=False, title_text="")
    fig.update_traces(marker_line_width=0, textfont_size=11)
    try:
        fig.update_layout(barcornerradius=10)  # Plotly 6+
    except Exception:
        pass
    return fig
