from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup

def main():

    xpath = '//*[@id="app"]/main/div/div[2]/div/div[2]/div/div/div/table'
    url = "https://provolleyball.com/teams/omaha-supernovas/statistics?tab=matchByMatch"

    driver = webdriver.Firefox()
    driver.get(url)

    element = driver.find_element(By.XPATH, xpath)
    html_element = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html_element, 'html.parser')

    headers = []
    rows = []

    for i, row in enumerate(soup.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    headers.insert(2,"H/A")

    value = rows[0][1][:2]
    value2 = rows[1][1][:2]
    print(value,"   ", value2)
    rows[0].insert(2, value)
    rows[1].insert(2, value2)
    rows[0][1] = rows[0][1][2:]
    rows[1][1] = rows[1][1][2:]
    
    df = pd.DataFrame(rows, columns=headers)
    print(df)
    df.to_csv('data/data.csv', index=False)
    driver.close()

if __name__ == "__main__":
    main()