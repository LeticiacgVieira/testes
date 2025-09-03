import streamlit as st
from pytube import Search, YouTube
import gspread
from google.oauth2.service_account import Credentials
import time

# ---------- CONFIGURAÇÃO ----------
SHEET_ID = "SEU_ID_DA_PLANILHA_AQUI"

# ---------- Autenticação usando Streamlit Secrets ----------
service_account_info = st.secrets["gcp_service_account"]

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(credentials)

sheet = client.open_by_key(SHEET_ID).sheet1

# ---------- Funções ----------
def adicionar_fila(musica):
    sheet.append_row([musica])

def pegar_proxima():
    primeira_linha = sheet.row_values(1)  # pega apenas a primeira linha
    if primeira_linha:
        proxima = primeira_linha[0]
        # limpa a primeira linha para "remover" a música da fila
        sheet.update('A1', '')  # só limpa a célula
        return proxima
    return None

@st.cache_data(ttl=5)
def ver_fila():
    """Retorna todas as músicas da fila, cache por 5 segundos."""
    lista = sheet.get_all_values()
    return [item[0] for item in lista if item]

def buscar_video(musica):
    search = Search(musica)
    if not search.results:
        return None, None
    video = search.results[0]
    yt = YouTube(video.watch_url)
    return yt.watch_url, yt.length

# ---------- Interface ----------
st.title("🎵 Player Contínuo Otimizado")

# Adicionar música
musica = st.text_input("Digite o nome da música:")
if st.button("Adicionar à fila") and musica.strip():
    adicionar_fila(musica)
    st.success(f"Música '{musica}' adicionada à fila!")
    st.session_state.tocando = False  # força checagem do player

# Mostrar fila
st.subheader("Fila atual:")
fila_atual = ver_fila()
if fila_atual:
    for i, m in enumerate(fila_atual, start=1):
        st.write(f"{i}. {m}")
else:
    st.write("A fila está vazia.")

# ---------- Player contínuo ----------
if "tocando" not in st.session_state:
    st.session_state.tocando = False

if fila_atual and not st.session_state.tocando:
    st.session_state.tocando = True
    while True:
        proxima = pegar_proxima()
        if proxima:
            video_url, duracao = buscar_video(proxima)
            if video_url is None:
                st.error(f"Não foi possível encontrar nenhum vídeo para '{proxima}'.")
                continue
            try:
                st.success(f"Tocando: {proxima}")
                st.video(video_url)
                time.sleep(duracao + 1)
            except Exception:
                st.error(f"Erro ao tocar '{proxima}'.")
        else:
            st.info("Fila vazia. Adicione mais músicas!")
            st.session_state.tocando = False
            break
