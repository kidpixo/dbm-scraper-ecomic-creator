import os
import zipfile
import re

files = [f for f in  os.listdir('./comics/')  if re.match(r'.*.cbz$', f)]

chapter_dict = {}
for ch_filename in files:
    with zipfile.ZipFile('comics/'+ch_filename, mode='r') as zf:
        # getting only the files with path 'images/four digits'
        chapter_dict[ch_filename] = [f for f in zf.namelist() if re.match(r'.*/\d{4}\..*', f)]
    print 'chapter %s : ' % ch_filename
    print chapter_dict[ch_filename]
    print '-'*20
