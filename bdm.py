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
    import re
    m = re.match('.*?(\d{1,}).*?',text)
    if m:
        return m.group(1)
    else:
        return text

# compare remote and locale

def rem_loc_compare(rem_dict,loc_dict,verbose=False):
    rem_loc_diff = {}
    for k in rem_dict.keys():

        # Check if loc_dict has the chapter / keys k!
        if k+'.cbz' in loc_dict:
        # do the rem vs loc comparison
            loc_ch = [int(extract_digits(l)) for l in  loc_dict[k+'.cbz']]
            tmp_diff = list(set(rem_dict[k])- set(loc_ch))
            if len(tmp_diff) > 0:
                rem_loc_diff[k] = tmp_diff
                if verbose:
                    print 'remmote/locacle difference for ch.%s: %s ' % (k,tmp_diff)
        else:
        # add all rem[k] to rem_diff
            rem_loc_diff[k] = rem_dict[k]

    return rem_loc_diff


def download_remote(to_download):

    import requests
    import shutil
    import os

    to_download_flat = [item for sublist in rem_loc_diff.values() for item in sublist]
    rem_down = {}
    # don't need to flatten the list, add a iteritems on the rem_loc_diff
    # and create a copy / modify it with the actual file dowloaded
    for chapter,pages in to_download.iteritems():
        pages_down = []
        for page in pages:

            filename = str(page).zfill(4)

            # test if file already exist
            if ( os.path.isfile('images/'+str(filename)+'.png') | os.path.isfile('images/'+str(filename)+'.jpg') ):
                extension =  '.jpg' if os.path.isfile('images/'+str(filename)+'.jpg') else '.png'
                out_filename = filename+extension
                print '%s already downloaded skippyng' % ( filename+extension )

            else:
                baseurl = 'http://www.dragonball-multiverse.com/en/pages/final/' + filename

                extension = '.png'
                res = requests.get(baseurl + extension, stream=True)
                try:
                    res.raise_for_status()
                    out_filename = filename+extension
                except Exception as exc:
                    print('Png file does not exist, tryng jpg. Error code : %s' % (exc))
                    del res
                    extension = '.jpg'
                    res = requests.get(baseurl + extension, stream=True)
                    try:
                        res.raise_for_status()
                        out_filename = filename+extension
                    except Exception as exc:
                        print('Png AND jpg file does not exist, skipping. Error code : %s' % (exc))
                        del res
                        out_filename = 'error_downloading.png'

                if 'error' not in out_filename :
                    with open('images/'+filename+extension, 'wb') as out_file:
                        shutil.copyfileobj(res.raw, out_file)
                print '%s downloaded and saved' % ( filename+extension )

            # build the actual downloaded file list
            pages_down.append(out_filename)
        # update the difference dictionary with the actual downloaded file list
        to_download[chapter] = pages_down

def cbz_assembler(rem_loc_diff_dict,verbose=False,remove=False):

    import os
    import zipfile

    for ch in rem_loc_diff_dict.keys():
        if not os.path.isfile('comics/%s.cbz' % ch) :
            # create file based on rem[ch] list
            mode='w'
            if verbose:
                print 'comics/%s.cbz does not exist, creating' % ch
        else:
            # append missing file from rem_loc_diff_dict[ch]
            mode='a'
            if verbose:
                print 'comics/%s.cbz does exist, appending' % ch

        with zipfile.ZipFile('comics/%s.cbz' % ch, mode=mode) as zf:
            for page in rem_loc_diff_dict[ch]:
                zf.write('images/'+page,compress_type=zipfile.ZIP_DEFLATED)
                if remove:
                    os.remove('images/'+page)
                    print 'Deleting images/'+page

## Testing stuff

# get remote status
rem = remote_scraper(verbose=False)

# get locale status
loc = locale_scraper(verbose=False)

# compare the two
rem_loc_diff = rem_loc_compare(rem,loc,verbose=True)

# this alter the rem_loc_diff dictionary with
# the actual file to compress in the cbz
download_remote(rem_loc_diff)

cbz_assembler(rem_loc_diff,verbose=True,remove=True)
