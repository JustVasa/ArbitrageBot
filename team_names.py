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
team_data = []

def scraper():
    global team_data
    team_elements = driver.find_elements(By.CSS_SELECTOR, ".event-table__team-name[data-test='teamName']")
    for team_element in team_elements:
        team_data.append(team_element.text)

scraper()

# Pairs the teams into two columns: Team1 and Team2
paired_teams = []
for i in range(0, len(team_data), 2):
    paired_teams.append([team_data[i], team_data[i + 1]])

df = pd.DataFrame(paired_teams, columns=['Team1', 'Team2'])
df.to_excel('teams.xlsx', index=False)

driver.quit()
