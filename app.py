import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from pytube import Search, YouTube
import time

# ---------- Autenticação usando Streamlit Secrets ----------
service_account_info = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(credentials)

# Abrir a planilha
sheet = client.open("FilaMusicas").sheet1

# ---------- Funções ----------
def adicionar_fila(musica):
    sheet.append_row([musica])

def pegar_proxima():
    lista = sheet.get_all_values()
    if lista:
        proxima = lista[0][0]
        sheet.delete_row(1)
        return proxima
    return None

def ver_fila():
    lista = sheet.get_all_values()
    return [item[0] for item in lista]

def buscar_video(musica):
    search = Search(musica)
    video = search.results[0]
    yt = YouTube(video.watch_url)
    return yt.watch_url, yt.length

# ---------- Interface ----------
st.title("🎵 Player Contínuo com Fila Compartilhada")

# Adicionar música
musica = st.text_input("Digite o nome da música:")
if st.button("Adicionar à fila"):
    if musica.strip():
        adicionar_fila(musica)
        st.success(f"Música '{musica}' adicionada à fila!")

# Mostra fila
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

if not st.session_state.tocando and fila_atual:
    st.session_state.tocando = True
    while True:
        proxima = pegar_proxima()
        if proxima:
            try:
                video_url, duracao = buscar_video(proxima)
                st.success(f"Tocando: {proxima}")
                st.video(video_url)
                time.sleep(duracao + 1)
            except Exception:
                st.error(f"Não foi possível tocar '{proxima}'.")
        else:
            st.info("Fila vazia. Adicione mais músicas!")
            st.session_state.tocando = False
            break
