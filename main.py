from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup

teams = ["https://provolleyball.com/teams/indy-ignite/statistics?tab=matchByMatch",
         "https://provolleyball.com/teams/atlanta-vibe/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/omaha-supernovas/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/columbus-fury/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/grand-rapids-rise/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/orlando-valkyries/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/san-diego-mojo/statistics?tab=matchByMatch",
        "https://provolleyball.com/teams/vegas-thrill/statistics?tab=matchByMatch"
        ]
teams.sort()
def extract_data(url):

    xpath_table = '//*[@id="app"]/main/div/div[2]/div/div[2]/div/div/div/table'
    xpath_2024_click = '//*[@id="app"]/main/div/div[2]/div/div[1]/div/select/option[1]'
    xpath_year_switch= '//*[@id="app"]/main/div/div[2]/div/div[1]/div'
    team_name_xpath = '//*[@id="app"]/main/div/section/div[2]/div/h1'

    driver = webdriver.Firefox()
    driver.get(teams[0])

    try:
        element = driver.find_element(By.XPATH, xpath_table)
        html_element = element.get_attribute('innerHTML')
        team_name = driver.find_element(By.XPATH, team_name_xpath).text
        soup = BeautifulSoup(html_element, 'html.parser')

    except:
         print("path not found")
         pass
    
    headers = []
    rows = []

    for i, row in enumerate(soup.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])
    try:
        driver.find_element(By.XPATH,xpath_year_switch).click()
        driver.find_element(By.XPATH,xpath_2024_click).click()
        driver.implicitly_wait(2)
        element = driver.find_element(By.XPATH,xpath_table)
        html_element = element.get_attribute('innerHTML')
        soup = BeautifulSoup(html_element, 'html.parser')
    except:
        print("path not found")
        pass

    for i, row in enumerate(soup.find_all('tr')):
            if i == 0:
                headers = [el.text.strip() for el in row.find_all('th')]
            else:
                rows.append([el.text.strip() for el in row.find_all('td')])

    for row in rows:
            value = row[1][:2]
            if value == "vs":
                row.insert(2, "Home")
            elif value == "at":
                row.insert(2, "Away")

            rows[rows.index(row)][1] = rows[rows.index(row)][1][2:]
            rows[rows.index(row)][11] = rows[rows.index(row)][11][:-1]
            rows[rows.index(row)].insert(1, team_name[:-11])

    headers.insert(2,"Location")
    headers.insert(1,"Team")

   
    driver.close()

    return rows,headers

def main():
    rows = []

    for team in teams:
        row,headers = extract_data(team)
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    print(df)
    df.to_csv('data/data.csv', index=False)

if __name__ == "__main__":
    main()