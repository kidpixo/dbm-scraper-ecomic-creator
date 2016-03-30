def remote_scraper(verbose=False):

    import requests, os, bs4
    import re

    url = "http://www.dragonball-multiverse.com/en/chapters.html"
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,"lxml")

    # to play with a local file
    # with open('chapters.htm', 'r') as f:
        # webpage = f.read().decode('utf-8')
    # soup = bs4.BeautifulSoup(webpage, "lxml")

    # search all div with defined ch attribute that is contains only digits
    chapters = soup.findAll(name='div',ch=re.compile("^-?[0-9]+$"))

    chapter_dict = {}
    for ch in chapters:
        pages = [int(l.get_text()) for l in ch.findAll('a',{'class': ''},text=re.compile("^-?[0-9]+$"))]
        chapter_dict[ch['ch']] = pages
        if verbose:
            print ch.name,ch['ch'],':'
            print pages
            print '-'*20

    return chapter_dict

def locale_scraper(verbose=False)

    import os
    import zipfile
    import re

    files = [f for f in  os.listdir('./comics/')  if re.match(r'.*.cbz$', f)]

    chapter_dict = {}
    for ch_filename in files:
        with zipfile.ZipFile('comics/'+ch_filename, mode='r') as zf:
            # getting only the files with path 'images/four digits'
            chapter_dict[ch_filename] = [f for f in zf.namelist() if re.match(r'.*/\d{4}\..*', f)]
        if verbose:
            print 'chapter %s : ' % ch_filename
            print chapter_dict[ch_filename]
            print '-'*20

        return chapter_dict
