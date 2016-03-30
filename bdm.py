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

def locale_scraper(verbose=False):

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

def extract_digits(text):
    m = re.match('.*?(\d{1,}).*?',text)
    if m:
        return m.group(1)
    else:
        return text

# compare remote and locale

## Testing stuff
rem = remote_scraper(verbose=False)
loc = locale_scraper(verbose=False)
# ch = '8'
# print rem_dict[ch]
# # int
# # [168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179]
# print loc_dict[ch+'.cbz']
# # strings
# ['images/0168.png', 'images/0169.png', 'images/0170.png', 'images/0171.png', 'images/0172.png', 'images/0173.png', 'images/0174.png', 'images/0175.png', 'images/0176.png', 'images/0177.png', 'images/0178.png', 'images/0179.png']
# loc_ch = [int(extract_digits(l)) for l in  loc_dict[ch+'.cbz']]
# # intersection of the two lists
# set(rem_dict[ch]).intersection(set(loc_ch))
# # difference of the two lists
# set(rem_dict[ch])- set(loc_ch)

def rem_loc_compare(rem_dict,loc_dict,verbose=False):
    rem_loc_diff = {}
    for k in rem_dict.keys():
        loc_ch = [int(extract_digits(l)) for l in  loc_dict[k+'.cbz']]
        tmp_diff = list(set(rem_dict[k])- set(loc_ch))
        if len(tmp_diff) > 0:
            rem_loc_diff[k] = tmp_diff
            if verbose:
                print 'remmote/locacle difference for ch.%s: %s ' % (k,tmp_diff)
    return rem_loc_diff

