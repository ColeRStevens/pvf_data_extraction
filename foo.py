import requests
import pandas as pd
from bs4 import BeautifulSoup




def main():

    url = "https://provolleyball.com/teams/omaha-supernovas/statistics?tab=matchByMatch"

    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    #print(soup.prettify())
    #tables = soup.find('div', class_="team-statistic-table")



    
    print('Classes of each table:')
    for table in soup.find_all('table'):
        print(table.get('class'))



    # data = []
    # for row in tables.find_all('tr'):
    #     cols = row.find_all('td')
    #     cols = [col.text.strip() for col in cols]
    #     data.append([col for col in cols if col])

    # df = pd.DataFrame(data)
    # print(df)

if __name__ == "__main__":
    main()