import requests
from bs4 import BeautifulSoup as bs
import urllib2

URL = 'https://www.bundestag.de/ajax/filterlist/de/service/opendata/-/543410/h_19781ab49efed1a651eb3566a051a4ae?limit=5&noFilterSet=true'
BASE_URL = 'https://www.bundestag.de'
r = requests.get(URL)

soup = bs(r.text, features="html.parser")
urls = []
names = []
for i, link in enumerate(soup.findAll('a')):
    FULL_URL = BASE_URL + link.get('href')
    if FULL_URL[-4:] == '.xml':
        print(FULL_URL)
        urls.append(FULL_URL)
        names.append(soup.select('a')[i].attrs['href'][-14:])

names_url = zip(names, urls)

for name, url in names_url:
    print url
    rq = urllib2.Request(url)
    res = urllib2.urlopen(rq)
    txt = open('files/' + name, 'wb')
    txt.write(res.read())
    txt.close()