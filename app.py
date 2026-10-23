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
  conteudo_base64 = base64.b64encode(conteudo_str.encode("utf-8")).decode(
      "utf-8"
  )

  payload = {
      "message": "Atualização de dados financeiros via FluxoClaro",
      "content": conteudo_base64,
  }
  if sha:
    payload["sha"] = sha

  resp = requests.put(url, headers=headers, json=payload)
  return resp.status_code in [200, 201]


# CSS com Tipografia Poppins Black / ExtraBold e Paleta Sempre Clara
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


ordem_meses = [
    "Janeiro 2026",
    "Fevereiro 2026",
    "Março 2026",
    "Abril 2026",
    "Maio 2026",
    "Junho 2026",
    "Julho 2026",
    "Agosto 2026",
    "Setembro 2026",
    "Outubro 2026",
    "Novembro 2026",
    "Dezembro 2026",
]

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

# Barra Lateral: Configurações & Mês de Referência
with st.sidebar:
  st.header("Configurações & Servidor")
  mes_referencia = st.selectbox(
      "Mês de Referência",
      ordem_meses,
      index=10,
  )

  # Sincroniza o mês selecionado com o session_state
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
  st.subheader("Reserva de Emergência")
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
  st.subheader("Gerenciar Categorias")
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
      cat_antiga = st.selectbox("Selecione a Categoria", list(dict_alvo.keys()))
      cat_nova = st.text_input("Novo Nome", value=cat_antiga)
      if st.button("Salvar Novo Nome", use_container_width=True):
        if cat_nova.strip() and cat_nova.strip() != cat_antiga:
          valor_atual = dict_alvo.pop(cat_antiga)
          dict_alvo[cat_nova.strip()] = valor_atual
          st.rerun()

  elif acao_cat == "Excluir Categoria":
    if dict_alvo:
      cat_excluir = st.selectbox(
          "Categoria para Excluir", list(dict_alvo.keys())
      )
      if st.button(
          "Confirmar Exclusão", type="primary", use_container_width=True
      ):
        dict_alvo.pop(cat_excluir, None)
        st.rerun()

# Atualiza temporariamente o mês ativo no dicionário global para cálculos corretos
st.session_state.dados_meses[mes_referencia] = {
    "entradas": st.session_state.entradas,
    "essenciais": st.session_state.essenciais,
    "nao_essenciais": st.session_state.nao_essenciais,
}

# Cálculos Automáticos Globais do Mês Ativo
total_entradas = sum(st.session_state.entradas.values())
total_essenciais = sum(st.session_state.essenciais.values())
total_nao_essenciais = sum(st.session_state.nao_essenciais.values())
total_despesas = total_essenciais + total_nao_essenciais
sobra_mensal = total_entradas - total_despesas

# Cálculo do Saldo Acumulado (Caixinha) de Janeiro até o Mês Selecionado
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

# Percentuais para as métricas
pct_ess = (
    (total_essenciais / total_entradas * 100) if total_entradas > 0 else 0.0
)
pct_ness = (
    (total_nao_essenciais / total_entradas * 100) if total_entradas > 0 else 0.0
)
pct_sobra = (sobra_mensal / total_entradas * 100) if total_entradas > 0 else 0.0

# Cabeçalho e Indicadores no Topo (6 Colunas)
st.title(f"FluxoClaro — Painel Gerencial ({mes_referencia})")

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("1. Total de Entradas", format_brl(total_entradas))
c2.metric(
    "2. Despesas Essenciais",
    format_brl(total_essenciais),
    f"{pct_ess:.1f}% da renda",
)
c3.metric(
    "3. Despesas Não Essenciais",
    format_brl(total_nao_essenciais),
    f"{pct_ness:.1f}% da renda",
)
c4.metric(
    "4. Sobra Mensal Prevista",
    format_brl(sobra_mensal),
    f"{pct_sobra:+.1f}% margem",
)
c5.metric(
    "5. Saldo Acumulado (Caixinha)",
    format_brl(saldo_acumulado),
    "Acumulado no ano",
)
c6.metric(
    "6. Meta da Reserva",
    format_brl(st.session_state.meta_reserva_alvo),
    f"Faltam {format_brl(max(0.0, st.session_state.meta_reserva_alvo - st.session_state.saldo_atual_reserva))}",
)

st.divider()

aba_planilha, aba_graficos, aba_metas = st.tabs([
    "📋 Planilha de Entradas e Despesas",
    "📊 Evolução & Comparações Mensais",
    "🎯 Metas de Economia",
])

with aba_planilha:
  col_ent, col_ess, col_ness = st.columns(3, gap="medium")
  with col_ent:
    st.subheader("1. Entradas")
    for k, v in list(st.session_state.entradas.items()):
      st.session_state.entradas[k] = st.number_input(
          k, min_value=0.0, value=float(v), step=50.0, key=f"ent_{k}"
      )
    st.info(
        f"**TOTAL DE ENTRADAS:**"
        f" {format_brl(sum(st.session_state.entradas.values()))}"
    )

  with col_ess:
    st.subheader("2. Despesas Essenciais")
    for k, v in list(st.session_state.essenciais.items()):
      st.session_state.essenciais[k] = st.number_input(
          k, min_value=0.0, value=float(v), step=25.0, key=f"ess_{k}"
      )
    st.info(
        f"**TOTAL DESPESAS ESSENCIAIS:**"
        f" {format_brl(sum(st.session_state.essenciais.values()))}"
    )

  with col_ness:
    st.subheader("3. Despesas Não Essenciais")
    for k, v in list(st.session_state.nao_essenciais.items()):
      st.session_state.nao_essenciais[k] = st.number_input(
          k, min_value=0.0, value=float(v), step=20.0, key=f"ness_{k}"
      )
    st.info(
        f"**TOTAL NÃO ESSENCIAIS:**"
        f" {format_brl(sum(st.session_state.nao_essenciais.values()))}"
    )

with aba_graficos:
  st.subheader("1. Evolução em Coluna Mensal (Entradas vs Despesas)")

  historico_data = []
  for m in ordem_meses:
    if m in st.session_state.dados_meses:
      d = st.session_state.dados_meses[m]
      t_ent = sum(d.get("entradas", {}).values())
      t_ess = sum(d.get("essenciais", {}).values())
      t_ness = sum(d.get("nao_essenciais", {}).values())

      historico_data.append(
          {"Mês": m, "Categoria": "Entradas", "Valor": t_ent}
      )
      historico_data.append(
          {"Mês": m, "Categoria": "Despesas Essenciais", "Valor": t_ess}
      )
      historico_data.append(
          {"Mês": m, "Categoria": "Despesas Não Essenciais", "Valor": t_ness}
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
            "Despesas Não Essenciais": "#9918ed",
        },
        title="Comparativo Mens
