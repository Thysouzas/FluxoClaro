# -*- coding: utf-8 -*-
"""
Painel Gerencial de Controle Financeiro Pessoal — FluxoClaro
Identidade Visual Premium:
- Cores Principais: #001089, #6e1aac, #9918ed
- Paleta Suave: #e8e9f9, #b9c2f9, #dfd3ea, #F6F7FD
- Assinatura Visual: Cartões com canto inferior esquerdo "mordido"
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


# --- ESTILIZAÇÃO AVANÇADA (CSS SURPRESA) ---
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #F4F5FC;
        color: #001089;
    }

    .stApp {
        background: radial-gradient(circle at 95% 5%, #eceeff 0%, #F4F5FC 55%);
        color: #001089;
    }

    /* BANNER DE TOPO COM GRADIENTE E CÍRCULOS */
    .hero-banner {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #001089 0%, #6e1aac 52%, #9918ed 100%);
        border-radius: 26px 26px 26px 6px;
        padding: 32px 38px;
        margin-bottom: 28px;
        box-shadow: 0 16px 36px rgba(110, 26, 172, 0.22);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    }

    .hero-banner::before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        background: radial-gradient(circle, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        top: -90px;
        right: -50px;
        pointer-events: none;
    }

    .hero-banner::after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        background: rgba(185, 194, 249, 0.14);
        border: 2px solid rgba(255, 255, 255, 0.15);
        border-radius: 50%;
        bottom: -70px;
        right: 160px;
        pointer-events: none;
    }

    .hero-title {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 900 !important;
        font-size: 2.1rem !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #e8e9f9;
        margin-top: 6px;
        font-weight: 500;
        opacity: 0.92;
    }

    .hero-badge {
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 10px 22px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 0.95rem;
        color: #FFFFFF;
        box-shadow: 0 8px 20px rgba(0, 16, 137, 0.25);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        z-index: 2;
    }

    /* BARRA LATERAL COM DEGRADÊ LILÁS E BORDAS DIREITAS ARREDONDADAS */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e8e9f9 0%, #dfd3ea 55%, #f3eef8 100%) !important;
        border-right: 2px solid #b9c2f9 !important;
        border-radius: 0 30px 30px 0 !important;
        box-shadow: 10px 0 35px rgba(0, 16, 137, 0.10) !important;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.2rem 1.3rem !important;
    }

    /* TÍTULOS */
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

    /* CARTÕES DE MÉTRICAS COM CANTO MORDIDO E HOVER */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #d4dafc;
        border-radius: 22px 22px 22px 4px !important;
        padding: 18px 20px !important;
        box-shadow: 0 10px
