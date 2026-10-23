# -*- coding: utf-8 -*-
import base64
import json
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="FluxoClaro — Painel Gerencial Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REPO_NAME = st.secrets.get("REPO_NAME", "Thysouzas/FluxoClaro")
ARQUIVO_DADOS = "dados_fluxo.json"


def obter_token():
    try:
        return st.secrets["GITHUB_TOKEN"]
    except Exception:
        return None


def carregar_da_nuvem():
    token = obter_token()
    if not token:
        return None

    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{ARQUIVO_DADOS}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            content_encoded = r.json().get("content")
            decoded = base64.b64decode(content_encoded).decode("utf-8")
            return json.loads(decoded)
    except Exception:
        pass
    return None


def salvar_na_nuvem(dados_dict):
    token = obter_token()
    if not token:
        st.error("Token do GitHub não configurado nos Secrets do Streamlit!")
        return False

    url = f"https://api.github.com/repos/{REPO_NAME}/contents/{ARQUIVO_DADOS}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    r = requests.get(url, headers=headers)
    sha = r.json().get("sha") if r.status_code == 200 else None

    conteudo_str = json.dumps(dados_dict, ensure_ascii=False, indent=4)
    b64_bytes = base64.b64encode(conteudo_str.encode("utf-8"))
    conteudo_base64 = b64_bytes.decode("utf-8")

    payload = {
        "message": "Atualização de dados financeiros via FluxoClaro",
        "content": conteudo_base64,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=headers, json=payload)
    return resp.status_code in [200, 201]


# CSS construído em lista segura (impede erros de aspas triplas cortadas)
 Regras_CSS = [
    "<style>",
    "@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');",
    "html, body, [class*='css'] { font-family: 'Poppins', sans-serif; background-color: #F4F5FC; color: #001089; }",
    ".stApp { background: radial-gradient(circle at 95% 5%, #eceeff 0%, #F4F5FC 55%); color: #001089; }",
    ".hero-banner { position: relative; overflow: hidden; background: linear-gradient(135deg, #001089 0%, #6e1aac 52%, #9918ed 100%); border-radius: 26px 26px 26px 6px; padding: 32px 38px; margin-bottom: 28px; box-shadow: 0 16px 36px rgba(110, 26, 172, 0.22); color: #FFFFFF; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; }",
    ".hero-banner::before { content: ''; position: absolute; width: 260px; height: 260px; background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; top: -90px; right: -50px; pointer-events: none; }",
    ".hero-banner::after { content: ''; position: absolute; width: 180px; height: 180px; background: rgba(185, 194, 249, 0.14); border: 2px solid rgba(255, 255, 255, 0.15); border-radius: 50%; bottom: -70px; right: 160px; pointer-events: none; }",
    ".hero-title { font-family: 'Poppins', sans-serif !important; font-weight: 900 !important; font-size: 2.1rem !important; color: #FFFFFF !important; margin: 0 !important; letter-spacing: -0.5px; line-height: 1.15; }",
    ".hero-subtitle { font-size: 0.95rem; color: #e8e9f9; margin-top: 6px; font-weight: 500; opacity: 0.92; }",
    ".hero-badge { background: rgba(255, 255, 255, 0.16); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.35); padding: 10px 22px; border-radius: 999px; font-weight: 800; font-size: 0.95rem; color: #FFFFFF; box-shadow: 0 8px 20px rgba(0, 16, 137, 0.25); display: inline-flex; align-items: center; gap: 8px; z-index: 2; }",
    "[data-testid='stSidebar'] { background: linear-gradient(180deg, #e8e9f9 0%, #dfd3ea 55%, #f3eef8 100%) !important; border-right: 2px solid #b9c2f9 !important; border-radius: 0 30px 30px 0 !important; box-shadow: 10px 0 35px rgba(0, 16, 137, 0.12) !important; }",
    "[data-testid='stSidebar'] > div:first-child { padding: 1.2rem 1.3rem !important; }",
    "h1 { font-family: 'Poppins', sans-serif !important; font-weight: 900 !important; color: #001089 !important; }",
    "h2, h3, h4 { font-family: 'Poppins', sans-serif !important; font-weight: 800 !important; color: #001089 !important; }",
    "div[data-testid='stMetric'] { background-color: #FFFFFF; border: 1px solid #d4dafc; border-radius: 22px 22px 22px 4px !important; padding: 18px 20px !important; box-shadow: 0 10px 26px rgba(0, 16, 137, 0.07), 0 3px 10px rgba(153, 24, 237, 0.05); transition: all 0.28s ease; position: relative; overflow: hidden; }",
    "div[data-testid='stMetric']:hover { transform: translateY(-6px); box-shadow: 0 18px 34px rgba(0, 16, 137, 0.13), 0 6px 16px rgba(153, 24, 237, 0.12); border-color: #9918ed; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(1) div[data-testid='stMetric'] { border-top: 6px solid #001089 !important; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(2) div[data-testid='stMetric'] { border-top: 6px solid #6e1aac !important; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(3) div[data-testid='stMetric'] { border-top: 6px solid #9918ed !important; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(4) div[data-testid='stMetric'] { border-top: 6px solid #2b59ff !important; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(5) div[data-testid='stMetric'] { border-top: 6px solid #b833ff !important; }",
    "div[data-testid='stHorizontalBlock'] > div:nth-child(6) div[data-testid='stMetric'] { border-top: 6px solid #43125f !important; }",
    "div[data-testid='stMetricValue'] { color: #001089 !important; font-weight: 900 !important; font-size: 1.5rem !important; }",
    "div[data-testid='stMetricLabel'] { font-weight: 700 !important; color: #4a4e8a !important; }",
    "div[data-testid='stTabs'] [data-baseweb='tab-list'] { gap: 12px; background-color: #e8e9f9; padding: 8px 10px; border-radius: 999px; border: 1px solid #b9c2f9; margin-bottom: 18px; }",
    "div[data-testid='stTabs'] [data-baseweb='tab'] { border-radius: 999px !important; padding: 10px 24px !important; font-weight: 700 !important; color: #001089 !important; border: none !important; background-color: transparent !important; transition: all 0.25s ease; }",
    "div[data-testid='stTabs'] [data-baseweb='tab']:hover { background-color: rgba(185, 194, 249, 0.45) !important; }",
    "div[data-testid='stTabs'] [aria-selected='true'] { background: linear-gradient(135deg, #001089 0%, #6e1aac 50%, #9918ed 100%) !important; color: #FFFFFF !important; box-shadow: 0 6px 18px rgba(153, 24, 237, 0.35) !important; }",
    "div[data-testid='stTabs'] [aria-selected='true'] p { color: #FFFFFF !important; font-weight: 800 !important; }",
    "div[data-testid='stTabs'] [data-baseweb='tab-highlight'] { display: none !important; }",
    ".stButton > button { border-radius: 999px !important; font-weight: 700 !important; padding: 0.55rem 1.3rem !important; border: 1.5px solid #b9c2f9 !important; background-color: #FFFFFF !important; color: #001089 !important; transition: all 0.25s ease !important; box-shadow: 0 4px 12px rgba(0, 16, 137, 0.05) !important; }",
    ".stButton > button:hover { border-color: #9918ed !important; color: #6e1aac !important; transform: translateY(-2px); box-shadow: 0 6px 16px rgba(153, 24, 237, 0.18) !important; }",
    ".stButton > button[kind='primary'] { background: linear-gradient(135deg, #001089 0%, #6e1aac 50%, #9918ed 100%) !important; color: #FFFFFF !important; border: none !important; box-shadow: 0 6px 20px rgba(153, 24, 237, 0.45), 0 0 14px rgba(153, 24, 237, 0.28) !important; }",
    ".stButton > button[kind='primary']:hover { box-shadow: 0 10px 26px rgba(153, 24, 237, 0.65), 0 0 20px rgba(153, 24, 237, 0.4) !important; transform: translateY(-2px) scale(1.01); color: #FFFFFF !important; }",
    "div[data-baseweb='input'] > div, div[data-baseweb='select'] > div { background-color: #FFFFFF !important; border: 1.5px solid #b9c2f9 !important; border-radius: 14px 14px 14px 4px !important; transition: all 0.2s ease !important; }",
    "div[data-baseweb='input']:focus-within > div, div[data-baseweb='select']:focus-within > div { border-color: #9918ed !important; box-shadow: 0 0 0 3.5px rgba(153, 24, 237, 0.22) !important; }",
    "div[data-testid='stAlert'] { background: linear-gradient(90deg, #eceeff 0%, #FFFFFF 100%) !important; border: 1px solid #b9c2f9 !important; border-left: 7px solid #9918ed !important; border-radius: 18px 18px 18px 4px !important; color: #001089 !important; box-shadow: 0 6px 18px rgba(0, 16, 137, 0.06) !important; padding: 14px 18px !important; }",
    "div[data-testid='stProgress'] > div > div > div > div { background: linear-gradient(90deg, #001089 0%, #6e1aac 50%, #9918ed 100%) !important; border-radius: 999px !important; }",
    "div[data-testid='stProgress'] > div > div { background-color: #e8e9f9 !important; border-radius: 999px !important; height: 12px !important; }",
    "div[data-testid='stPlotlyChart'] { background-color: #FFFFFF; border: 1px solid #d4dafc; border-radius: 22px 22px 22px 4px; padding: 18px; box-shadow: 0 10px 26px rgba(0, 16, 137, 0.06); margin-bottom: 16px; }",
    "div[data-testid='stExpander'] { background-color: #FFFFFF; border: 1.5px solid #b9c2f9 !important; border-radius: 20px 20px 20px 4px !important; box-shadow: 0 6px 18px rgba(0, 16, 137, 0.05); overflow: hidden; }",
    "</style>",
]
st.markdown("\n".join(Regras_CSS), unsafe_allow_html=True)


def format_brl(valor: float) -> str:
    txt = f"R$ {valor:,.2f}"
    return txt.replace(",", "X").replace(".", ",").replace("X", ".")


def get_default_mes():
    return {
        "entradas": {
            "Aluguel": 0.0,
            "Salario": 0.0,
            "Outros": 0.0,
        },
        "essenciais": {
            "Faculdade": 0.0,
            "MEI (DAS)": 0.0,
            "Plano Celular (TIM)": 0.0,
            "Internet (Ligga)": 0.0,
            "Energia (Copel)": 0.0,
            "Cond. R. Redzimski": 0.0,
            "Cond. R. Eduarda Sprada": 0.0,
            "IPTU": 0.0,
        },
        "nao_essenciais": {
            "Cartão de Crédito PF": 0.0,
            "Cartão de Crédito PJ": 0.0,
            "Outras Despesas: Presentes e Diversos": 0.0,
            "Imprevistos": 0.0,
        },
    }


meses_nomes = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]
anos_disponiveis = ["2026", "2027"]

ordem_meses = [f"{m} {a}" for a in anos_disponiveis for m in meses_nomes]

if "dados_meses" not in st.session_state:
    nuvem = carregar_da_nuvem()
    if nuvem and isinstance(nuvem, dict):
        st.session_state.dados_meses = nuvem
        if "meta_reserva_alvo" in nuvem:
            st.session_state.meta_reserva_alvo = float(
                nuvem["meta_reserva_alvo"]
            )
        if "saldo_atual_reserva" in nuvem:
            st.session_state.saldo_atual_reserva = float(
                nuvem["saldo_atual_reserva"]
            )
        if "metas_economia" in nuvem:
            st.session_state.metas_economia = nuvem["metas_economia"]
    else:
        st.session_state.dados_meses = {}

if "meta_reserva_alvo" not in st.session_state:
    st.session_state.meta_reserva_alvo = 10000.0

if "saldo_atual_reserva" not in st.session_state:
    st.session_state.saldo_atual_reserva = 0.0

if "metas_economia" not in st.session_state:
    st.session_state.metas_economia = []
    for m_data in st.session_state.dados_meses.values():
        if isinstance(m_data, dict) and "metas_economia" in m_data:
            st.session_state.metas_economia = m_data["metas_economia"]
            break

# Barra Lateral Flutuante
with st.sidebar:
    st.header("📅 Data")

    col_a, col_m = st.columns(2)
    with col_a:
        ano_selecionado = st.selectbox("Ano", anos_disponiveis, index=0)
    with col_m:
        mes_selecionado = st.selectbox("Mês", meses_nomes, index=9)

    mes_referencia = f"{mes_selecionado} {ano_selecionado}"

    if (
        "mes_atual_ativo" not in st.session_state
        or st.session_state.mes_atual_ativo != mes_referencia
    ):
        if mes_referencia not in st.session_state.dados_meses:
            st.session_state.dados_meses[mes_referencia] = get_default_mes()

        m_atual = st.session_state.dados_meses[mes_referencia]
        padrao = get_default_mes()
        st.session_state.entradas = m_atual.get(
            "entradas", padrao["entradas"]
        ).copy()
        st.session_state.essenciais = m_atual.get(
            "essenciais", padrao["essenciais"]
        ).copy()
        st.session_state.nao_essenciais = m_atual.get(
            "nao_essenciais", padrao["nao_essenciais"]
        ).copy()

        for k, v in st.session_state.entradas.items():
            st.session_state[f"ent_{k}"] = float(v)
        for k, v in st.session_state.essenciais.items():
            st.session_state[f"ess_{k}"] = float(v)
        for k, v in st.session_state.nao_essenciais.items():
            st.session_state[f"ness_{k}"] = float(v)

        st.session_state.mes_atual_ativo = mes_referencia

    st.divider()
    st.subheader("☁️ Servidor na Nuvem")
    if st.button(
        "💾 Salvar na Nuvem",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.dados_meses[mes_referencia] = {
            "entradas": st.session_state.entradas,
            "essenciais": st.session_state.essenciais,
            "nao_essenciais": st.session_state.nao_essenciais,
        }
        pacote_global = st.session_state.dados_meses.copy()
        pacote_global["meta_reserva_alvo"] = st.session_state.meta_reserva_alvo
        pacote_global["saldo_atual_reserva"] = (
            st.session_state.saldo_atual_reserva
        )
        pacote_global["metas_economia"] = st.session_state.metas_economia

        sucesso = salvar_na_nuvem(pacote_global)
        if sucesso:
            st.success("Dados salvos com sucesso no servidor!")
        else:
            st.error("Erro ao salvar. Verifique os Secrets do Streamlit.")

    st.divider()
    st.subheader("🧹 Limpeza do Mês")
    if st.button("🔄 Zerar Valores Deste Mês", use_container_width=True):
        for k in st.session_state.entradas:
            st.session_state.entradas[k] = 0.0
            st.session_state[f"ent_{k}"] = 0.0
        for k in st.session_state.essenciais:
            st.session_state.essenciais[k] = 0.0
            st.session_state[f"ess_{k}"] = 0.0
        for k in st.session_state.nao_essenciais:
            st.session_state.nao_essenciais[k] = 0.0
            st.session_state[f"ness_{k}"] = 0.0

        st.session_state.dados_meses[mes_referencia] = {
            "entradas": st.session_state.entradas,
            "essenciais": st.session_state.essenciais,
            "nao_essenciais": st.session_state.nao_essenciais,
        }
        st.success(f"Valores de {mes_referencia} zerados!")
        st.rerun()

    st.divider()
    st.subheader("🛡️ Reserva de Emergência")
    st.session_state.meta_reserva_alvo = st.number_input(
        "Valor Almejado da Reserva (R$)",
        min_value=0.0,
        value=float(st.session_state.meta_reserva_alvo),
        step=500.0,
    )
    st.session_state.saldo_atual_reserva = st.number_input(
        "Saldo Atual da Reserva (R$)",
        min_value=0.0,
        value=float(st.session_state.saldo_atual_reserva),
        step=100.0,
    )

    st.divider()
    st.subheader("⚙️ Gerenciar Categorias")
    acao_cat = st.selectbox(
        "Ação",
        ["Criar Nova Categoria", "Renomear Categoria", "Excluir Categoria"],
    )
    grupo_alvo = st.selectbox(
        "Grupo",
        [
            "1. Outras Entradas",
            "2. Despesas Essenciais",
            "3. Outras Despesas (Não Essenciais)",
        ],
    )

    dict_alvo = (
        st.session_state.entradas
        if grupo_alvo.startswith("1")
        else st.session_state.essenciais
        if grupo_alvo.startswith("2")
        else st.session_state.nao_essenciais
    )

    if acao_cat == "Criar Nova Categoria":
        novo_nome = st.text_input("Nome da Nova Categoria")
        novo_valor = st.number_input(
            "Valor Inicial (R$)", min_value=0.0, value=0.0, step=50.0
        )
        if st.button("Adicionar Categoria", use_container_width=True):
            if novo_nome.strip():
                dict_alvo[novo_nome.strip()] = float(novo_valor)
                st.rerun()

    elif acao_cat == "Renomear Categoria":
        if dict_alvo:
            opcoes_cat = list(dict_alvo.keys())
            cat_antiga = st.selectbox("Selecione a Categoria", opcoes_cat)
            cat_nova = st.text_input("Novo Nome", value=cat_antiga)
            if st.button("Salvar Novo Nome", use_container_width=True):
                if cat_nova.strip() and cat_nova.strip() != cat_antiga:
                    valor_atual = dict_alvo.pop(cat_antiga)
                    dict_alvo[cat_nova.strip()] = valor_atual
                    st.rerun()

    elif acao_cat == "Excluir Categoria":
        if dict_alvo:
            opcoes_del = list(dict_alvo.keys())
            cat_excluir = st.selectbox("Categoria para Excluir", opcoes_del)
            if st.button(
                "Confirmar Exclusão", type="primary", use_container_width=True
            ):
                dict_alvo.pop(cat_excluir, None)
                st.rerun()

# Sincroniza estado atual
st.session_state.dados_meses[mes_referencia] = {
    "entradas": st.session_state.entradas,
    "essenciais": st.session_state.essenciais,
    "nao_essenciais": st.session_state.nao_essenciais,
}

total_entradas = sum(st.session_state.entradas.values())
total_essenciais = sum(st.session_state.essenciais.values())
total_nao_essenciais = sum(st.session_state.nao_essenciais.values())
total_despesas = total_essenciais + total_nao_essenciais
sobra_mensal = total_entradas - total_despesas

try:
    idx_atual = ordem_meses.index(mes_referencia)
except ValueError:
    idx_atual = 0

saldo_acumulado = 0.0
for i in range(idx_atual + 1):
    m_nome = ordem_meses[i]
    if m_nome in st.session_state.dados_meses:
        d = st.session_state.dados_meses[m_nome]
        t_ent = sum(d.get("entradas", {}).values())
        t_esp = sum(d.get("essenciais", {}).values()) + sum(
            d.get("nao_essenciais", {}).values()
        )
        saldo_acumulado += t_ent - t_esp

pct_ess = (
    (total_essenciais / total_entradas * 100) if total_entradas > 0 else 0.0
)
pct_ness = (
    (total_nao_essenciais / total_entradas * 100) if total_entradas > 0 else 0.0
)
pct_sobra = (
    (sobra_mensal / total_entradas * 100) if total_entradas > 0 else 0.0
)

# BANNER DE TOPO (Sem usar triple quotes para nunca quebrar)
banner_html = (
    '<div class="hero-banner">'
    '<div>'
    '<h1 class="hero-title">FluxoClaro — Painel Gerencial</h1>'
    '<div class="hero-subtitle">Gestão financeira inteligente, patrimônio e metas na nuvem</div>'
    '</div>'
    f'<div class="hero-badge">🗓️ {mes_referencia}</div>'
    '</div>'
)
st.markdown(banner_html, unsafe_allow_html=True)

# 6 CARTÕES DE MÉTRICAS
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric(
    "1. Total de Entradas",
    format_brl(total_entradas),
    delta="Receita registrada",
    delta_color="off",
)
c2.metric(
    "2. Despesas Essenciais",
    format_brl(total_essenciais),
    f"{pct_ess:.1f}% da renda",
)
c3.metric(
    "3. Não Essenciais",
    format_brl(total_nao_essenciais),
    f"{pct_ness:.1f}% da renda",
)
c4.metric(
    "4. Sobra Mensal Prevista",
    format_brl(sobra_mensal),
    f"{pct_sobra:+.1f}% margem",
)
c5.metric(
    "5. Saldo Acumulado",
    format_brl(saldo_acumulado),
    "Caixinha acumulada",
)
falta_reserva = max(
    0.0,
    st.session_state.meta_reserva_alvo - st.session_state.saldo_atual_reserva,
)
c6.metric(
    "6. Reserva Ideal",
    format_brl(st.session_state.meta_reserva_alvo),
    f"Faltam {format_brl(falta_reserva)}",
)

st.write("")

aba_planilha, aba_graficos, aba_metas = st.tabs([
    "📋 Planilha de Entradas e Despesas",
    "📊 Dashboard",
    "🎯 Metas de Economia",
])

with aba_planilha:
    col_ent, col_ess, col_ness = st.columns(3, gap="large")
    with col_ent:
        st.subheader("1. Entradas")
        for k, v in list(st.session_state.entradas.items()):
            st.session_state.entradas[k] = st.number_input(
                k, min_value=0.0, value=float(v), step=50.0, key=f"ent_{k}"
            )
        soma_ent = format_brl(sum(st.session_state.entradas.values()))
        st.info(f"**TOTAL DE ENTRADAS:** {soma_ent}")

    with col_ess:
        st.subheader("2. Despesas Essenciais")
        for k, v in list(st.session_state.essenciais.items()):
            st.session_state.essenciais[k] = st.number_input(
                k, min_value=0.0, value=float(v), step=25.0, key=f"ess_{k}"
            )
        soma_ess = format_brl(sum(st.session_state.essenciais.values()))
        st.info(f"**TOTAL DESPESAS ESSENCIAIS:** {soma_ess}")

    with col_ness:
        st.subheader("3. Despesas Não Essenciais")
        for k, v in list(st.session_state.nao_essenciais.items()):
            st.session_state.nao_essenciais[k] = st.number_input(
                k, min_value=0.0, value=float(v), step=20.0, key=f"ness_{k}"
            )
        soma_ness = format_brl(sum(st.session_state.nao_essenciais.values()))
        st.info(f"**TOTAL NÃO ESSENCIAIS:** {soma_ness}")

with aba_graficos:
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        filtro_ano_grafico = st.selectbox(
            "📅 Filtrar Ano do Dashboard",
            ["Todos os Anos"] + anos_disponiveis,
        )

    st.subheader("1. Evolução em Coluna Mensal (Entradas vs Despesas)")

    historico_data = []
    for m in ordem_meses:
        ano_do_mes = m.split(" ")[1]
        if (
            filtro_ano_grafico != "Todos os Anos"
            and ano_do_mes != filtro_ano_grafico
        ):
            continue

        if m in st.session_state.dados_meses:
            d = st.session_state.dados_meses[m]
            t_ent = sum(d.get("entradas", {}).values())
            t_ess = sum(d.get("essenciais", {}).values())
            t_ness = sum(d.get("nao_essenciais", {}).values())

            if t_ent > 0 or t_ess > 0 or t_ness > 0:
                historico_data.append(
                    {"Mês": m, "Categoria": "Entradas", "Valor": t_ent}
                )
                historico_data.append(
                    {
                        "Mês": m,
                        "Categoria": "Despesas Essenciais",
                        "Valor": t_ess,
                    }
                )
                historico_data.append(
                    {
                        "Mês": m,
                        "Categoria": "Despesas Não Essenciais",
                        "Valor": t_ness,
                    }
                )

    df_hist = pd.DataFrame(historico_data)

    if not df_hist.empty:
        fig_colunas = px.bar(
            df_hist,
            x="Mês",
            y="Valor",
            color="Categoria",
            barmode="group",
            text_auto=".2f",
            color_discrete_map={
                "Entradas": "#001089",
                "Despesas Essenciais": "#6e1aac",
                "Despesas Não Essenciais": "#c084fc",
            },
            title=f"Comparativo Mensal ({filtro_ano_grafico})",
        )
        fig_colunas.update_traces(marker_line_width=0, opacity=0.95)
        fig_colunas.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Poppins, sans-serif", color="#001089"),
            bargap=0.25,
            bargroupgap=0.12,
            barcornerradius=8,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.04,
                xanchor="center",
                x=0.5,
                title=None,
            ),
            yaxis=dict(showgrid=True, gridcolor="#eceeff", zeroline=False),
            xaxis=dict(showgrid=False),
            margin=dict(t=70, b=40, l=30, r=30),
        )
        st.plotly_chart(fig_colunas, use_container_width=True)
    else:
        st.info("Preencha e salve dados no ano selecionado para ver o gráfico.")

    st.subheader("2. Comparação da Sobra Mensal ao Longo do Tempo")

    sobra_data = []
    for m in ordem_meses:
        ano_do_mes = m.split(" ")[1]
        if (
            filtro_ano_grafico != "Todos os Anos"
            and ano_do_mes != filtro_ano_grafico
        ):
            continue

        if m in st.session_state.dados_meses:
            d = st.session_state.dados_meses[m]
            t_ent = sum(d.get("entradas", {}).values())
            t_esp = sum(d.get("essenciais", {}).values()) + sum(
                d.get("nao_essenciais", {}).values()
            )
            sobra_val = t_ent - t_esp
            if t_ent > 0 or t_esp > 0:
                sobra_data.append({"Mês": m, "Sobra Mensal": sobra_val})

    df_sobra = pd.DataFrame(sobra_data)
    if not df_sobra.empty:
        fig_sobra = px.bar(
            df_sobra,
            x="Mês",
            y="Sobra Mensal",
            text_auto=".2f",
            color="Sobra Mensal",
            color_continuous_scale=["#c084fc", "#6e1aac", "#001089"],
            title=f"Evolução da Sobra Financeira ({filtro_ano_grafico})",
        )
        fig_sobra.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Poppins, sans-serif", color="#001089"),
            barcornerradius=8,
            yaxis=dict(
                showgrid=True,
                gridcolor="#eceeff",
                zeroline=True,
                zerolinecolor="#b9c2f9",
            ),
            xaxis=dict(showgrid=False),
            margin=dict(t=65, b=40, l=30, r=30),
        )
        st.plotly_chart(fig_sobra, use_container_width=True)
    else:
        st.info(
            "Preencha os valores e clique em 'Salvar na Nuvem' "
            "para visualizar o histórico temporal."
        )

with aba_metas:
    st.subheader("🎯 Minhas Metas de Economia")
    todas_categorias_despesa = {
        **st.session_state.essenciais,
        **st.session_state.nao_essenciais,
    }

    with st.expander("➕ Adicionar Nova Meta de Economia"):
        m_titulo = st.text_input("Descrição da Meta (ex: Viagem em Família)")
        opcoes_meta = ["SOBRA_MENSAL"] + list(todas_categorias_despesa.keys())
        m_cat = st.selectbox("Categoria Vinculada", opcoes_meta)
        m_valor = st.number_input(
            "Valor da Meta / Teto (R$)",
            min_value=10.0,
            value=500.0,
            step=50.0,
        )
        if st.button("Salvar Meta", type="primary"):
            st.session_state.metas_economia.append({
                "titulo": m_titulo or f"Meta {m_cat}",
                "categoria": m_cat,
                "meta": float(m_valor),
            })
            st.success(
                "Meta adicionada! Clique em 'Salvar na Nuvem' na barra lateral."
            )
            st.rerun()

    if not st.session_state.metas_economia:
        st.info(
            "Ainda não tem nenhuma meta cadastrada. "
            "Use o botão acima para criar a sua primeira meta!"
        )
    else:
        st.write("")
        for idx, meta in enumerate(list(st.session_state.metas_economia)):
            cat = meta["categoria"]
            alvo = meta["meta"]
            real = (
                max(0.0, sobra_mensal)
                if cat == "SOBRA_MENSAL"
                else todas_categorias_despesa.get(cat, 0.0)
            )
            pct = min(1.0, real / alvo) if alvo > 0 else 0.0

            col_m1, col_m2 = st.columns([5, 1])
            with col_m1:
                txt_real = format_brl(real)
                txt_alvo = format_brl(alvo)
                st.markdown(
                    f"**{meta['titulo']}** — Atual: {txt_real} / Meta: {txt_alvo}"
                )
                st.progress(pct)
            with col_m2:
                st.write("")
                if st.button("🗑️ Excluir", key=f"del_meta_{idx}"):
                    st.session_state.metas_economia.pop(idx)
                    st.success("Meta excluída. Salve na nuvem para atualizar.")
                    st.rerun()
