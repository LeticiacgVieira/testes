import streamlit as st
from pytube import Search, YouTube
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# ---------- Configuração Google Sheets ----------
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)
sheet = client.open("FilaMusicas").sheet1  # nome do Sheet

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
    return yt.watch_url, yt.length  # retorna URL e duração em segundos

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
                # Espera a duração do vídeo antes de tocar o próximo
                time.sleep(duracao + 1)  # +1 segundo de segurança
            except Exception:
                st.error(f"Não foi possível tocar '{proxima}'.")
        else:
            st.info("Fila vazia. Adicione mais músicas!")
            st.session_state.tocando = False
            break
