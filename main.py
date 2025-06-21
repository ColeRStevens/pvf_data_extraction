from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import os,sys

teams = ["https://provolleyball.com/teams/indy-ignite/statistics?tab=matchByMatch",
         "https://provolleyball.com/teams/atlanta-vibe/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/omaha-supernovas/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/columbus-fury/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/grand-rapids-rise/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/orlando-valkyries/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/san-diego-mojo/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/vegas-thrill/statistics?tab=matchByMatch"]

def extract_data(url):

    # xpaths for various elements
    xpath_table = '//*[@id="app"]/main/div/div[2]/div/div[2]/div/div/div/table'
    xpath_2024_click = '//*[@id="app"]/main/div/div[2]/div/div[1]/div/select/option[1]'
    xpath_year_switch= '//*[@id="app"]/main/div/div[2]/div/div[1]/div'

    name = url[32:].split('/')[0].replace('-', ' ')
    name = name.title()

    co = Options()
    co.add_argument("--headless")
    driver = webdriver.Chrome(options=co)

    driver.get(url)
    
   # wait for the table to load
    element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_table)))
    html_element = element.get_attribute('innerHTML')
    soup = BeautifulSoup(html_element, 'html.parser')
    print("2025 data found for ",name)
    
    headers = []
    rows = []

    # extract the data
    for i, row in enumerate(soup.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])
   
    driver.find_element(By.XPATH,xpath_year_switch).click()
    driver.find_element(By.XPATH,xpath_2024_click).click()
    
    # wait for the table to load
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_table)))
        html_element = element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_element, 'html.parser')
        print("2024 data found for",name)
    except:
        print(f"No 2024 data found for",name)
        for row in rows:
            value = row[1][:2]
            if value == "vs":
                row.insert(2, "Home")
            elif value == "at":
                row.insert(2, "Away")

            rows[rows.index(row)][1] = rows[rows.index(row)][1][2:]
            rows[rows.index(row)][11] = rows[rows.index(row)][11][:-1]
            rows[rows.index(row)].insert(1, name)

        headers.insert(2,"Location")
        headers.insert(1,"Team")
        
        driver.close()

        return rows,headers
        
    # extract the data
    for i, row in enumerate(soup.find_all('tr')):
            if i == 0:
                headers = [el.text.strip() for el in row.find_all('th')]
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])
    # clean up the data
    for row in rows:
            value = row[1][:2]
            if value == "vs":
                row.insert(2, "Home")
            elif value == "at":
                row.insert(2, "Away")

            rows[rows.index(row)][1] = rows[rows.index(row)][1][2:]
            rows[rows.index(row)][11] = rows[rows.index(row)][11][:-1]
            rows[rows.index(row)].insert(1, name)

    headers.insert(2,"Location")
    headers.insert(1,"Team")

    driver.close()

    return rows,headers

def sort_data(i,rows):

    return sorted(rows, key=lambda x: x[int(i)])
    
def main():

    index = sys.argv[1];
    if index == None:
        index = 0
    print("The index is : " + index)

    team_rows = []
    header = []

    for team in teams:
        rows,headers = extract_data(team)
        if header == []:
            header = headers
        team_rows.extend(rows)

    # See sort_data function
    team_rows = sort_data(index,team_rows)

    df = pd.DataFrame(team_rows, columns=headers)
    print(df)

    if not os.path.exists("./data"):
        os.makedirs("./data")
    
    df.to_csv(f"./data/data.csv",index=False)

if __name__ == "__main__":
    main()