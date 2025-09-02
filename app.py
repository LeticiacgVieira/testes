import streamlit as st
import json
import os

ARQUIVO = "musicas.json"

def salvar_musica(musica):
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            dados = json.load(f)
    else:
        dados = []

    dados.append(musica)

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f)

st.title("🎵 Registrar música")

musica = st.text_input("Digite o nome da música:")

if st.button("Salvar"):
    if musica.strip() != "":
        salvar_musica(musica)
        st.success(f"Música '{musica}' registrada com sucesso!")
