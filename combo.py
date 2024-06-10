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
number_data = []


def scraper():
    global team_data, number_data
    team_elements = driver.find_elements(By.CSS_SELECTOR, ".event-table__team-name[data-test='teamName']")
    number_elements = driver.find_elements(By.CSS_SELECTOR, ".snake-loader_Wrapper__eWJsB.event-table__col.event-table__col--factor.event-table-markets_snakeLoaderWrapper__Axo9h")

    for team_element in team_elements:
        team_data.append(team_element.text)

    for number_element in number_elements:
        number_data.append(number_element.text)


scraper()

# Pairs the teams into two columns: Team1 and Team2
paired_teams = []
for i in range(0, len(team_data), 2):
    if i + 1 < len(team_data):
        paired_teams.append([team_data[i], team_data[i + 1]])

# Pairs the odds into three columns: Team1_Odd, Draw_Odd, Team2_Odd
paired_odds = []
for i in range(0, len(number_data), 3):
    if i + 2 < len(number_data):
        paired_odds.append([number_data[i], number_data[i + 1], number_data[i + 2]])

# Ensure both lists have the same length
min_length = min(len(paired_teams), len(paired_odds))

# Combine teams and odds into one DataFrame
combined_data = []
for i in range(min_length):
    combined_data.append(paired_teams[i] + paired_odds[i])

df = pd.DataFrame(combined_data, columns=['Team1', 'Team2', 'Team1_Odd', 'Draw_Odd', 'Team2_Odd'])
df.to_excel('teams_and_odds.xlsx', index=False)

driver.quit()
