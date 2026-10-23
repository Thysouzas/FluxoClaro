# -*- coding: utf-8 -*-
"""
Painel Gerencial de Controle Financeiro Pessoal — FluxoClaro (Com Servidor GitHub & Saldo Acumulado)
Identidade Visual Oficial:
- Cores Principais: #001089, #9918ed, #6e1aac
- Variação de Cores (Fundo Sempre Claro): #e8e9f9, #b9c2f9, #dfd3ea, #e9e8ea
- Tipografia: Poppins Black (Títulos) e Poppins ExtraBold (Subtítulos)
"""

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
    initial_sidebar_state="expanded",
)

# --- CONFIGURAÇÃO DO SERVIDOR GITHUB (VIA SECRETS) ---
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
    conteudo_base64 = base64.b64encode(conteudo_str.encode("utf-8")).decode("utf-8")

    payload = {
        "message": "Atualização de dados financeiros via FluxoClaro",
        "content": conteudo_base64,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=headers, json=payload)
    return resp.status_code in [200, 201]


# CSS com Sidebar Flutuante, Tipografia Poppins e Paleta Sempre Clara
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #F6F7FD;
        color: #001089;
    }
    
    .stApp {
        background-color: #F6F7FD;
        color: #001089;
    }

    /* ESTILO DA BARRA LATERAL FLUOTANTE E ELEGANTE */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: none !important;
        box-shadow: 6px 0px 30px rgba(0, 16, 137, 0.06);
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-left: 1.2rem;
        padding-right: 1.2rem;
    }

    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 900 !important;
        color: #001089 !important;
    }
    
    h2, h3, h4 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 800 !important;
        color: #001089 !important;
    }
    
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #b9c2f9;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 12px rgba(0, 16, 137, 0.03);
    }
    
    div[data-testid="stMetricValue"] {
        color: #001089 !important;
        font-weight: 800 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def format_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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

# Inicialização dos dados globais da nuvem
if "dados_meses" not in st.session_state:
    nuvem = carregar_da_nuvem()
    if nuvem and isinstance(nuvem, dict):
        st.session_state.dados_meses = nuvem
        if "meta_reserva_alvo" in nuvem:
            st.session_state.meta_reserva_alvo = float(nuvem["meta_reserva_alvo"])
        if "saldo_atual_reserva" in nuvem:
            st.session_state.saldo_atual_reserva = float(nuvem["saldo_atual_reserva"])
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

# Barra Lateral: Configurações & Filtros de Data Separados
with st.sidebar:
    st.header("Configurações & Servidor")
    
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
        st.session_state.entradas = m_atual.get(
            "entradas", get_default_mes()["entradas"]
        ).copy()
        st.session_state.essenciais = m_atual.get(
            "essenciais", get_default_mes()["essenciais"]
        ).copy()
        st.session_state.nao_essenciais = m_atual.get(
            "nao_essenciais", get_default_mes()["nao_essenciais"]
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
        "💾 Salvar / Confirmar na Nuvem",
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
        pacote_global["saldo_atual_reserva"] = st.session_state.saldo_atual_reserva
        pacote_global["metas_economia"] = st.session_state.metas_economia

        sucesso = salvar_na_nuvem(pacote_global)
        if sucesso:
            st.success("Dados salvos com sucesso no servidor!")
        else:
            st.error("Erro ao salvar. Verifique o token nos Secrets do Streamlit.")

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
        st.success(f"Valores de {mes_referencia} zerados com sucesso!")
        st.rerun()

    st.divider()
    st.subheader("Reserva de Emergência")
    st.session_state.meta_reserva_alvo = st.number_input(
        "Valor Almejado da
