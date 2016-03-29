import requests, os, bs4
import re

url = "http://www.dragonball-multiverse.com/en/chapters.html"
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)

# search all div with defined ch attribute that is contains only digits
chapters = soup.findAll(name='div',ch=re.compile("^-?[0-9]+$"))

for ch in chapters:
    print ch.name,ch['ch'],':',
    for l in ch.findAll('a',{'class': ''},text=re.compile("^-?[0-9]+$")):
        print int(l.get_text()),',',
    print

