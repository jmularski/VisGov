import requests
from bs4 import BeautifulSoup as bs
import urllib.request, urllib.error, urllib.parse
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

for offset in range(0, 91, 5):

        URL = 'https://www.bundestag.de/ajax/filterlist/de/services/opendata/543410-543410/h_1fd5ee62865616a005ea2f6d4bc98824?limit=5&noFilterSet=true&offset=' + str(offset)
        BASE_URL = 'https://www.bundestag.de'


        r = requests.get(URL)

        soup = bs(r.text, features="html.parser")
        urls = []
        names = []
        for data in soup.findAll(class_='bt-documents-description'):
                FULL_URL = BASE_URL + data.ul.li.a.get('href')
                if FULL_URL[-4:] == '.xml':
                        urls.append(FULL_URL)
                        date = data.p.strong.string.split('dem ')[1].replace('.', '')
                        names.append(datetime.strptime(date, "%d %B %Y").strftime("%d.%m.%Y") + '.xml')

        names_url = list(zip(names, urls))

        for name, url in names_url:
                rq = urllib.request.Request(url)
                res = urllib.request.urlopen(rq)
                txt = open('../files/' + name, 'a+')
                txt.write(res.read().decode('utf-8'))
                txt.close()
