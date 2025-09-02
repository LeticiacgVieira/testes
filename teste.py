from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import shutil

def buscar_youtube(musica):
    # encontra caminho do chromium
    chrome_path = shutil.which("chromium-browser")
    driver_path = shutil.which("chromedriver")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.youtube.com")
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(musica)
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)

    first_video = driver.find_element(By.ID, "video-title")
    url = first_video.get_attribute("href")

    driver.quit()
    return url
