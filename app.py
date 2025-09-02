import streamlit as st
from pytube import Search

st.title("🎵 Player de Música Online com Fila")

# Inicializa a fila na sessão
if "fila" not in st.session_state:
    st.session_state.fila = []

# Input para adicionar música
musica = st.text_input("Digite o nome da música:")

if st.button("Adicionar à fila"):
    if musica.strip():
        st.session_state.fila.append(musica)
        st.success(f"Música '{musica}' adicionada à fila!")

# Mostra a fila
st.subheader("Fila atual:")
if st.session_state.fila:
    for i, m in enumerate(st.session_state.fila, start=1):
        st.write(f"{i}. {m}")
else:
    st.write("A fila está vazia.")

# Botão para tocar a próxima música
if st.button("Tocar próxima música"):
    if st.session_state.fila:
        proxima = st.session_state.fila.pop(0)  # remove a primeira música
        with st.spinner(f"Buscando '{proxima}' no YouTube..."):
            try:
                search = Search(proxima)
                video = search.results[0]
                video_url = video.watch_url
                st.success(f"Tocando: {proxima}")
                st.video(video_url)
            except Exception:
                st.error(f"Não foi possível encontrar '{proxima}'.")
    else:
        st.warning("Não há músicas na fila.")
