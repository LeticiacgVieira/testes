import streamlit as st
from pytube import Search, YouTube
import gspread
from google.oauth2.service_account import Credentials
import time

# ---------- CONFIGURAÇÃO ----------
# Substitua pelo ID da sua planilha no Google Sheets
SHEET_ID = "1ROB_zfZjpSPyaMuLOix5m146RDvkAiAoqPYuc4zNNN8"

# ---------- Autenticação usando Streamlit Secrets ----------
service_account_info = st.secrets["gcp_service_account"]

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(credentials)

# Abrir a planilha pelo ID
sheet = client.open_by_key(SHEET_ID).sheet1

# ---------- Funções ----------
def adicionar_fila(musica):
    sheet.append_row([musica])

def pegar_proxima():
    lista = sheet.get_all_values()
    if lista:
        proxima = lista[0][0]
        # Apaga a primeira linha corretamente
        sheet.batch_update([{
            'range': '1:1',
            'values': [[''] * len(lista[0])]  # mantém o número de colunas
        }])
        return proxima
    return None

def ver_fila():
    lista = sheet.get_all_values()
    return [item[0] for item in lista]

def buscar_video(musica):
    search = Search(musica)
    if not search.results:
        return None, None  # Nenhum vídeo encontrado
    video = search.results[0]
    yt = YouTube(video.watch_url)
    return yt.watch_url, yt.length  # URL e duração em segundos

# ---------- Interface ----------
st.title("🎵 Player Contínuo com Fila Compartilhada")

# Adicionar música
musica = st.text_input("Digite o nome da música:")
if st.button("Adicionar à fila"):
    if musica.strip():
        adicionar_fila(musica)
        st.success(f"Música '{musica}' adicionada à fila!")
        # Atualiza fila e força checagem do player
        fila_atual = ver_fila()
        st.session_state.tocando = False

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

# Inicia player se houver música e não estiver tocando
if fila_atual and not st.session_state.tocando:
    st.session_state.tocando = True
    while True:
        proxima = pegar_proxima()
        if proxima:
            video_url, duracao = buscar_video(proxima)
            if video_url is None:
                st.error(f"Não foi possível encontrar nenhum vídeo para '{proxima}'.")
                continue  # passa para a próxima música
            try:
                st.success(f"Tocando: {proxima}")
                st.video(video_url)
                time.sleep(duracao + 1)  # espera o tempo real do vídeo
            except Exception:
                st.error(f"Erro ao tocar '{proxima}'.")
        else:
            st.info("Fila vazia. Adicione mais músicas!")
            st.session_state.tocando = False
            break
