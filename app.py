import streamlit as st
from pytube import Search

st.title("🎵 Player de Música Online")

musica = st.text_input("Digite o nome da música:")

if st.button("Tocar Música"):
    if musica.strip():
        with st.spinner("Buscando vídeo no YouTube..."):
            try:
                search = Search(musica)
                video = search.results[0]  # primeiro resultado
                video_url = video.watch_url
                st.success("Música encontrada! 🎶")
                st.video(video_url)
            except Exception:
                st.error("Não foi possível encontrar o vídeo.")
