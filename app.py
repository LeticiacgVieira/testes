import streamlit as st
import requests
from bs4 import BeautifulSoup

def buscar_youtube(musica):
    query = musica.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")

    # Pega primeiro vídeo disponível
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "/watch?v=" in href:
            return f"https://www.youtube.com{href}"
    return None

# Interface do Streamlit
st.title("🎵 Player de Música Online")

musica = st.text_input("Digite o nome da música:")

if st.button("Tocar Música"):
    if musica.strip():
        with st.spinner("Buscando vídeo no YouTube..."):
            video_url = buscar_youtube(musica)
        
        if video_url:
            st.success("Música encontrada! 🎶")
            st.video(video_url)  # exibe o vídeo diretamente
        else:
            st.error("Não foi possível encontrar o vídeo.")
