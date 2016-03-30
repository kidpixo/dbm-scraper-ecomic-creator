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
            chapter_dict[ch_filename] = sorted( [f for f in zf.namelist() if re.match(r'.*/\d{4}\..*', f)] )
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


def download_remote(to_download):

    import requests
    import shutil

    for element in to_download:

        filename = str(rem_loc_diff_flat[0]).zfill(4)
        extension = '.png'
        baseurl = 'http://www.dragonball-multiverse.com/en/pages/final/' + filename

        res = requests.get(baseurl + extension, stream=True)

        try:
            res.raise_for_status()
        except Exception as exc:
            print('Png file does not exist, tryng jpg. Error code : %s' % (exc))
            del res
            extension = '.jpg'
            res = requests.get(baseurl + extension, stream=True)

        with open('images/'+filename+extension, 'wb') as out_file:
            shutil.copyfileobj(res.raw, out_file)

        print '%s downloaded and saved' % ( filename+extension )
        del res

## Testing stuff

# get remote status
rem = remote_scraper(verbose=False)

# get locale status
loc = locale_scraper(verbose=False)

# compare the two
rem_loc_diff = rem_loc_compare(rem,loc,verbose=True)
print rem_loc_diff
# {'51': [1161]}
:w

# flatten the dictionary of lists :
rem_loc_diff_flat = [item for sublist in rem_loc_diff.values() for item in sublist]

download_remote(rem_loc_diff_flat)

import os

for ch in rem_loc_diff.keys():
    print loc[k+'.cbz']
    print rem[k]
    if not os.path.isfile('images/%s.cbz' % k) :
        create file based on rem[k] list
    else:
        append missing file from rem_loc_diff[k]

