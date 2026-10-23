# -*- coding: utf-8 -*-
"""
Painel Gerencial de Controle Financeiro Pessoal — FluxoClaro
Identidade Visual Oficial:
- Cores Principais: #001089, #9918ed, #6e1aac
- Variação de Cores (Fundo Sempre Claro): #e8e9f9, #b9c2f9, #dfd3ea, #e9e8ea
- Tipografia: Poppins Black (Títulos) e Poppins ExtraBold (Subtítulos)
"""

import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="FluxoClaro — Painel Gerencial Financeiro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

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


# 1. Inicialização do Session State
if "entradas" not in st.session_state:
  st.session_state.entradas = {
      "Salário Líquido (Pessoa 01)": 0.0,
      "Salário Líquido (Pessoa 02)": 0.0,
      "Vale-Alimentação (VA)": 0.0,
      "Vale-Refeição (VR)": 0.0,
      "Outras Entradas: Uber / Apps / Freelance": 0.0,
      "Outras Entradas: Comissões / Bônus": 0.0,
      "Outras Entradas: Aluguel / Dividendos": 0.0,
  }

if "essenciais" not in st.session_state:
  st.session_state.essenciais = {
      "Moradia (Financiamento / Aluguel)": 0.0,
      "Condomínio": 0.0,
      "Supermercado": 0.0,
      "Água e Saneamento": 0.0,
      "Luz (Energia Elétrica)": 0.0,
      "Gás (Encanado / Botijão)": 0.0,
      "IPTU": 0.0,
      "Plano de Saúde": 0.0,
      "MEI (DAS)": 0.0,
      "Investimentos Obrigatórios": 0.0,
      "Faculdade / Educação": 0.0,
  }

if "nao_essenciais" not in st.session_state:
  st.session_state.nao_essenciais = {
      "Cartão de Crédito PF": 0.0,
      "Cartão de Crédito PJ": 0.0,
      "Farmácia": 0.0,
      "Gastos com Animais (Pet)": 0.0,
      "Imprevistos": 0.0,
      "Transporte (Ônibus / Trem / Uber)": 0.0,
      "Veículo (Seguro / IPVA / Manutenção)": 0.0,
      "Combustível": 0.0,
      "Internet Residencial": 0.0,
      "Streaming (Netflix / Amazon / Spotify)": 0.0,
      "Padaria / Feira": 0.0,
      "Lazer / Cinema / Restaurantes": 0.0,
      "Salão / Manicure / Barbearia": 0.0,
      "Tarifas Bancárias": 0.0,
      "Telefonia Móvel": 0.0,
      "Outras Despesas: Presentes e Diversos": 0.0,
  }

if "metas_economia" not in st.session_state:
  st.session_state.metas_economia = [
      {
          "titulo": "Meta de Gasto com Lazer / Cinema",
          "categoria": "Lazer / Cinema / Restaurantes",
          "meta": 500.0,
      },
      {
          "titulo": "Teto do Cartão de Crédito PF",
          "categoria": "Cartão de Crédito PF",
          "meta": 1000.0,
      },
      {
          "titulo": "Orçamento de Supermercado",
          "categoria": "Supermercado",
          "meta": 1500.0,
      },
      {
          "titulo": "Economia Mensal Livre p/ Viagem e Lazer Futuro",
          "categoria": "SOBRA_MENSAL",
          "meta": 500.0,
      },
  ]

# Barra Lateral: Configurações, Reserva e Gestão de Backup
with st.sidebar:
  st.header("Configurações & Backup")
  mes_referencia = st.selectbox(
      "Mês de Referência",
      [
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
      ],
      index=10,
  )

  st.divider()
  st.subheader("💾 Gestão de Dados (Backup)")
  
  dados_app = {
      "entradas": st.session_state.entradas,
      "essenciais": st.session_state.essenciais,
      "nao_essenciais": st.session_state.nao_essenciais,
  }
  json_str = json.dumps(dados_app, ensure_ascii=False, indent=4)
  st.download_button(
      label="📥 Descarregar Backup",
      data=json_str,
      file_name="fluxoclaro_backup.json",
      mime="application/json",
      use_container_width=True,
  )

  arquivo_carregado = st.file_uploader(
      "📂 Restaurar Backup", type=["json"]
  )
  if arquivo_carregado is not None:
    try:
      dados_carregados = json.load(arquivo_carregado)
      st.session_state.entradas = dados_carregados.get(
          "entradas", st.session_state.entradas
      )
      st.session_state.essenciais = dados_carregados.get(
          "essenciais", st.session_state.essenciais
      )
      st.session_state.nao_essenciais = dados_carregados.get(
          "nao_essenciais", st.session_state.nao_essenciais
      )
      st.success("Backup restaurado com sucesso!")
      st.rerun()
    except Exception as e:
      st.error(f"Erro ao ler o ficheiro: {e}")

  st.divider()
  st.subheader("Reserva de Emergência")
  meses_reserva = st.radio(
      "Multiplicador Ideal (sobre gastos essenciais)",
      options=[3, 6, 12],
      index=1,
      format_func=lambda x: f"{x} meses de custo essencial",
  )
  saldo_atual_reserva = st.number_input(
      "Saldo Atual da Reserva (R$)", min_value=0.0, value=0.0, step=100.0
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

# Cálculos Automáticos Globais
total_entradas = sum(st.session_state.entradas.values())
total_essenciais = sum(st.session_state.essenciais.values())
total_nao_essenciais = sum(st.session_state.nao_essenciais.values())
total_despesas = total_essenciais + total_nao_essenciais
sobra_mensal = total_entradas - total_despesas
reserva_ideal = total_essenciais * meses_reserva

# Cabeçalho e Indicadores no Topo
st.title(f"FluxoClaro — Painel Gerencial ({mes_referencia})")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("1. Total de Entradas", format_brl(total_entradas))
c2.metric(
    "2. Despesas Essenciais",
    format_brl(total_essenciais),
    (
        f"{(total_essenciais/total_entradas*100 if total_entradas else 0):.1f}%"
        " da renda"
    ),
)
c3.metric(
    "3. Despesas Não Essenciais",
    format_brl(total_nao_essenciais),
    (
        f"{(total_nao_essenciais/total_entradas*100 if total_entradas else 0):.1f}%"
        " da renda"
    ),
)
c4.metric(
    "4. Sobra Mensal Prevista",
    format_brl(sobra_mensal),
    (
        f"{(sobra_mensal/total_entradas*100 if total_entradas else 0):+.1f}%"
        " margem"
    ),
)
c5.metric(
    f"5. Reserva Ideal ({meses_reserva}m)",
    format_brl(reserva_ideal),
    f"Faltam {format_brl(max(0.0, reserva_ideal - saldo_atual_reserva))}",
)

st.divider()

aba_planilha, aba_graficos, aba_metas = st.tabs([
    "📋 Planilha de Entradas e Despesas",
    "📊 Gráficos Interativos (Barras e Pizza)",
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
  st.subheader(
      "1. Gráfico de Barras Interativo: Categorias de Entradas vs. Despesas"
  )
  dados_barras = (
      [
          {"Categoria": k, "Valor": v, "Tipo": "1. Entradas"}
          for k, v in st.session_state.entradas.items()
          if v > 0
      ]
      + [
          {"Categoria": k, "Valor": v, "Tipo": "2. Despesas Essenciais"}
          for k, v in st.session_state.essenciais.items()
          if v > 0
      ]
      + [
          {"Categoria": k, "Valor": v, "Tipo": "3. Despesas Não Essenciais"}
          for k, v in st.session_state.nao_essenciais.items()
          if v > 0
      ]
  )
  if dados_barras:
    df_barras = pd.DataFrame(dados_barras).sort_values(
        by="Valor", ascending=True
    )
    fig_barras = px.bar(
        df_barras,
        x="Valor",
        y="Categoria",
        color="Tipo",
        orientation="h",
        text_auto=".2f",
        color_discrete_map={
            "1. Entradas": "#001089",
            "2. Despesas Essenciais": "#6e1aac",
            "3. Despesas Não Essenciais": "#9918ed",
        },
    )
    fig_barras.update_layout(
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font_color="#001089"
    )
    st.plotly_chart(fig_barras, use_container_width=True)

  st.divider()
  st.subheader(
      "2. Gráficos de Pizza: Distribuição das Despesas Essenciais e Não"
      " Essenciais"
  )
  p_col1, p_col2, p_col3 = st.columns(3)

  with p_col1:
    df_macro = pd.DataFrame({
        "Grupo": ["Despesas Essenciais", "Despesas Não Essenciais"],
        "Valor": [total_essenciais, total_nao_essenciais],
    })
    fig_p1 = px.pie(
        df_macro,
        names="Grupo",
        values="Valor",
        hole=0.45,
        title="Proporção Geral de Despesas",
        color="Grupo",
        color_discrete_map={
            "Despesas Essenciais": "#001089",
            "Despesas Não Essenciais": "#9918ed",
        },
    )
    fig_p1.update_layout(paper_bgcolor="#FFFFFF", font_color="#001089")
    st.plotly_chart(fig_p1, use_container_width=True)

  with p_col2:
    df_ess = pd.DataFrame([
        {"Item": k, "Valor": v}
        for k, v in st.session_state.essenciais.items()
        if v > 0
    ])
    if not df_ess.empty:
      fig_p2 = px.pie(
          df_ess,
          names="Item",
          values="Valor",
          hole=0.45,
          title="Detalhamento: Despesas Essenciais",
          color_discrete_sequence=[
              "#001089",
              "#6e1aac",
              "#9918ed",
              "#b9c2f9",
              "#dfd3ea",
          ],
      )
      fig_p2.update_layout(paper_bgcolor="#FFFFFF", font_color="#001089")
      st.plotly_chart(fig_p2, use_container_width=True)

  with p_col3:
    df_ness = pd.DataFrame([
        {"Item": k, "Valor": v}
        for k, v in st.session_state.nao_essenciais.items()
        if v > 0
    ])
    if not df_ness.empty:
      fig_p3 = px.pie(
          df_ness,
          names="Item",
          values="Valor",
          hole=0.45,
          title="Detalhamento: Não Essenciais",
          color_discrete_sequence=[
              "#9918ed",
              "#6e1aac",
              "#001089",
              "#b9c2f9",
              "#dfd3ea",
          ],
      )
      fig_p3.update_layout(paper_bgcolor="#FFFFFF", font_color="#001089")
      st.plotly_chart(fig_p3, use_container_width=True)

with aba_metas:
  st.subheader("Metas de Economia Mensal vs. Gastos Reais")
  todas_categorias_despesa = {
      **st.session_state.essenciais,
      **st.session_state.nao_essenciais,
  }

  with st.expander("➕ Adicionar Nova Meta de Economia"):
    m_titulo = st.text_input("Descrição da Meta (ex: Economizar em Lazer)")
    m_cat = st.selectbox(
        "Categoria Vinculada",
        ["SOBRA_MENSAL"] + list(todas_categorias_despesa.keys()),
    )
    m_valor = st.number_input(
        "Valor da Meta / Teto (R$)", min_value=10.0, value=500.0, step=50.0
    )
    if st.button("Salvar Meta"):
      st.session_state.metas_economia.append({
          "titulo": m_titulo or f"Meta {m_cat}",
          "categoria": m_cat,
          "meta": float(m_valor),
      })
      st.rerun()

  for idx, meta in enumerate(list(st.session_state.metas_economia)):
    cat = meta["categoria"]
    alvo = meta["meta"]
    real = (
        max(0.0, sobra_mensal)
        if cat == "SOBRA_MENSAL"
        else todas_categorias_despesa.get(cat, 0.0)
    )
    pct = min(1.0, real / alvo) if alvo > 0 else 0.0
    st.markdown(
        f"**{meta['titulo']}** — Atual: {format_brl(real)} / Meta:"
        f" {format_brl(alvo)}"
    )
    st.progress(pct)
