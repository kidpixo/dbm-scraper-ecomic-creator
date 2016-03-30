##  Scraper, updater and creator of ecomic (cbz) from dbm

This repository goal is to scrape, update and create ecomic (cbz) from dbm.

Merging all the code in bdm.py 

## Logic 

Step 1. Check the pages+chapters from remote (code actually in `bs4_scrape_chapters.py` )

STATUS : **DONE**

in/out

- INPUT  <- remote URL
- OUTPUT -> chapter + pages list , {'chapter' : pages } pyton dict maybe?


Step 2. Check the local data (recover some code from `chapters_maker.py`) :

Case 1. :

STATUS : **DONE**

- INPUT  <- directory with .cbz files
- OUTPUT -> list of .cbz files (== chapters) and pages within like in 1.OUTPUT


Case 2. : 

STATUS : WTF? Is this useful?

- INPUT  <- directory with images
- OUTPUT -> lst of local pages


Step 3. Compare remote and locale lists

STATUS : **DONE**

Case:

- remote.chapter.page == locale.chapter.page : do nothing.
- remote.chapter.page > locale.chapter.page :

    - list al the missing pages
    - download them 
        - using python request try first the page.png , if exception try page.jpg


Step 4. Assemble the .cbz (recover some code from `chapters_maker.py`)

- Check for each chapter if remote.chapter.page == locale.chapter.page
    - if not: 
        - if .cbz exist : append missing pages
        - if .cbz doens't exist : create cbz with remote.chapter.page
