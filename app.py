import streamlit as st
from pytube import Search
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

def buscar_youtube(musica):
    search = Search(musica)
    video = search.results[0]
    return video.watch_url

# ---------- Interface ----------
st.title("🎵 Player de Música Online Contínuo")

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
            with st.spinner(f"Tocando '{proxima}'..."):
                try:
                    video_url = buscar_youtube(proxima)
                    st.video(video_url)
                    time.sleep(5)  # espera o tempo aproximado do vídeo
                except Exception:
                    st.error(f"Não foi possível tocar '{proxima}'.")
        else:
            st.info("Fila vazia. Adicione mais músicas!")
            st.session_state.tocando = False
            break
