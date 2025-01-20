from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

url = "https://provolleyball.com/teams/omaha-supernovas/statistics?tab=matchByMatch"

xpath_table = '//*[@id="app"]/main/div/div[2]/div/div[2]/div/div/div/table'
xpath_2024_click = '//*[@id="app"]/main/div/div[2]/div/div[1]/div/select/option[1]'
xpath_year_switch= '//*[@id="app"]/main/div/div[2]/div/div[1]/div'

driver = webdriver.Firefox()
driver.get(url)

driver.find_element(By.XPATH,xpath_year_switch).click()
driver.find_element(By.XPATH,xpath_2024_click).click()
driver.implicitly_wait(1)
element = driver.find_element(By.XPATH,xpath_table)
html_element = element.get_attribute('innerHTML')
soup = BeautifulSoup(html_element, 'html.parser')

headers = []
rows = []

for i, row in enumerate(soup.find_all('tr')):
    if i == 0:
        headers = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])

headers.insert(2,"Location")

    
for row in rows:
    value = row[1][:2]
    if value == "vs":
        row.insert(2, "Home")
    elif value == "at":
        row.insert(2, "Away")

    rows[rows.index(row)][1] = rows[rows.index(row)][1][2:]
    rows[rows.index(row)][11] = rows[rows.index(row)][11][:-1]


print(headers)

df = pd.DataFrame(rows, columns=headers)
print(df)
df.to_csv('data/data.csv', index=False)
driver.close()

