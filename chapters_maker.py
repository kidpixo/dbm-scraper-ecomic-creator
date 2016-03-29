import numpy as np
import os
import zipfile
import re

chapters = np.loadtxt("chapters.txt", comments="#", delimiter=",", unpack=False,dtype=int)
# filter only files starting with digits
files =  [f for f in  os.listdir('./images/')  if re.match(r'\d{4}\.', f)]
files = [int(i.split('.')[0]) for i in files]

chapters_plus_one = np.append( chapters[1:]-1 , files[-1])

for chapter,ini,end in zip(np.arange(1,chapters.size+1),chapters,chapters_plus_one):
    print chapter,ini,end
    # some pages are doubled and the number is not present
    tozip =  list(set(np.arange(ini,end+1)).intersection(set(files)))
    tozip = ['images/'+str(el).zfill(4)+'.png' for el in tozip]
    # create an end page
    if not os.path.isfile('images/end_ch_{ch}.png'.format(ch=chapter)):
        os.system("convert  -background black -fill white -gravity Center -font komika_text/KOMTXKBI.ttf  -size 600x861 label:'End of\n Chapter #{ch}' images/end_ch_{ch}.png".format(ch=chapter))
        tozip.append('images/end_ch_{ch}.png'.format(ch=chapter))

    print 'creating archive for chapter %s' % chapter

    with zipfile.ZipFile('comics/%s.cbz' % chapter, mode='w') as zf:
        for page in tozip:
            zf.write(page,compress_type=zipfile.ZIP_DEFLATED)

    print 'chapter %s done!' % chapter
