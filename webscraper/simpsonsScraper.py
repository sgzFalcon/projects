import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.springfieldspringfield.co.uk/episode_scripts.php'
url = 'https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=the-simpsons&episode=s01e01'

def scrape(season,ep,url):
    data = {'tv-show':'the-simpsons', 'episode':'s{:02d}e{:02d}'.format(season,ep)}
    res = requests.post(url,data=data)
    if res.status_code != 200:
        return 0 #all episodes scraped 
    soup = BeautifulSoup(res.text, 'html.parser')
    script = soup.select('.scrolling-script-container')
    if len(script) >= 1:
        return script[0].get_text().strip()
    else:
        return 0

count = 0
scrapedData ={}
for season in range(1,30):
    scrapedData['s{:02d}'.format(season)] = {}
    for ep in range(1,26):
        script = scrape(season,ep,url)
        if script == 0:
            continue
        else:
            scrapedData['s{:02d}'.format(season)]['e{:02d}'.format(ep)] = script
            count +=1
            print('Episode #{:03d}'.format(count))
            print('s{:02d}e{:02d}'.format(season,ep))

    with open('data.json', 'w') as outfile:
        json.dump(scrapedData, outfile)

print('Episodes scraped: ',count)
