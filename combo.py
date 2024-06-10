from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Inicializace WebDriveru
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Otevření stránky
url = "https://ivibettin.com/prematch/football"
driver.get(url)
driver.set_window_size(800, 1000)

time.sleep(5)

# Čekání na načtení stránky (volitelné, může se upravit podle potřeby)
driver.implicitly_wait(15)
number_data = []

def scraper():
    global number_data
    # Používání CSS selektoru pro více tříd
    number_elements = driver.find_elements(By.CSS_SELECTOR, ".snake-loader_Wrapper__eWJsB.event-table__col.event-table__col--factor.event-table-markets_snakeLoaderWrapper__Axo9h")
    for number_element in number_elements:
        number_data.append(number_element.text)

scraper()

print(number_data)

driver.quit()
