import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Lista para armazenar músicas pesquisadas
musicas_guardadas = []

def abrir_youtube(musica, headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get("https://www.youtube.com")

        # Faz pesquisa
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(musica)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        # Pega o primeiro vídeo
        first_video = driver.find_element(By.ID, "video-title")
        first_video.click()  # Abre o vídeo

        # Abre nova guia (só funciona fora do headless)
        driver.execute_script("window.open('https://www.youtube.com', '_blank');")

        return True

    except Exception as e:
        print("Erro:", e)
        return False


# ------------------ Streamlit Interface ------------------
st.title("🎵 Buscador de Música")

musica = st.text_input("Digite o nome da música:")

if st.button("Salvar e Abrir no YouTube"):
    if musica.strip() != "":
        musicas_guardadas.append(musica)
        st.success(f"Música '{musica}' salva!")

        # Aqui abre o YouTube com Selenium
        ok = abrir_youtube(musica, headless=False)  # 👉 headless=False abre guia real
        if ok:
            st.write("O YouTube foi aberto no navegador pelo Selenium.")
        else:
            st.error("Erro ao abrir o YouTube com Selenium.")
