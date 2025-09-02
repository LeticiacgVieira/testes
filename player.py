from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

def abrir_youtube(musica):
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com")

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(musica)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    first_video = driver.find_element(By.ID, "video-title")
    first_video.click()

# Lê última música salva
with open("musicas.json", "r") as f:
    musicas = json.load(f)

if musicas:
    ultima = musicas[-1]
    print(f"Abrindo: {ultima}")
    abrir_youtube(ultima)
else:
    print("Nenhuma música registrada ainda.")
