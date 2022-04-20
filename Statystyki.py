import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import re
import requests
import openpyxl

URL_BASE = "https://rozgrywki.pzkosz.pl/liga/2/druzyny.html"

page = get(URL_BASE)
bs = BeautifulSoup(page.content, 'html.parser')


links = []
for link in bs.findAll('a', href=True):
    links.append(link.get('href'))


team_link = [ "https://rozgrywki.pzkosz.pl" + teams[0:-5] + "/statystyki_zawodnikow.html"
              for teams in links if "/liga/2/druzyny/d" in teams]

headers = []
data1 = []
for team in range(1, len(team_link)):
    req = requests.get(team_link[team])
    soup = BeautifulSoup(req.text, 'html.parser')
    stat_table = soup.find('table', class_='stattype')
    for i in stat_table.find_all('th'):
        [headers.append(i.text.strip()) for title in i if i.text.strip() not in headers]

    for row in stat_table.find_all('tr')[1:]:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]
        data1.append(row_data)


df = pd.DataFrame(data1, columns = headers)
df.dropna(inplace = True)


new = df['2P'].str.split(' / ', expand = True)
df['2PA'] = new[1]
df['2PM'] = new[0]
df.drop(columns =['2P'], inplace = True)

print(df.head(7))

student_result = pd.ExcelWriter('plk.xlsx')
df.to_excel("plk.xlsx")






