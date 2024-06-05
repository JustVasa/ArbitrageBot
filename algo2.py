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
url = "https://ivibettin.com/cz/prematch"
driver.get(url)
driver.maximize_window()

time.sleep(5)

# Čekání na načtení stránky (volitelné, může se upravit podle potřeby)
driver.implicitly_wait(15)

# Seznam pro ukládání dat
team_data = []

def move_right_button():
    move_right = driver.find_element(By.XPATH, "//*[@id='platform']/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/button[2]")
    move_right.click()
    time.sleep(1)

def get_sport_name(xpath):
    sport_element = driver.find_element(By.XPATH, xpath)
    return sport_element.text

def function():
    global team_data
    i = 1
    while True:
        try:
            xpath = f"//*[@id='platform']/div[2]/div[2]/div/div[2]/div/div[3]/div/div[2]/div[1]/div/div/div/div/div/div/div[{i}]/div/div/div"
            sport = driver.find_element(By.XPATH, xpath)
            sport_name = get_sport_name(xpath)
            sport.click()
            time.sleep(1)
            scraper(sport_name)
            if i == 15 or i == 29 or i == 39:
                move_right_button()
            i += 2
            print(team_data)
        except:
            break

def scraper(sport_name):
    global team_data
    # Vyhledání prvků obsahujících názvy týmů
    team_elements = driver.find_elements(By.CSS_SELECTOR, ".event-table__team-name[data-test='teamName']")
    # Uložení názvů týmů do seznamu s názvem sportu
    for team_element in team_elements:
        team_data.append([sport_name, team_element.text])

# Spuštění hlavní funkce
function()

# Uložení dat do Excel souboru pomocí pandas
df = pd.DataFrame(team_data, columns=['Sport Name', 'Team Name'])
df.to_excel('teams.xlsx', index=False)

# Ukončení driveru
driver.quit()
