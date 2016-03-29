##  Scraper, updater and creator of ecomic (cbz) from dbm

This repository goal is to scrape, update and create ecomic (cbz) from dbm.

## Logic 

1. Check the pages+chapters from remote (code actually in `bs4_scrape_chapters.py` ) 

in/out

- INPUT  <- remote URL
- OUTPUT -> chapter + pages list , {'chapter' : pages } pyton dict maybe?


2. Check the local data (recover some code from `chapters_maker.py`) :

Case 1. :

- INPUT  <- directory with .cbz files
- OUTPUT -> list of .cbz files (== chapters) and pages within like in 1.OUTPUT


Case 2. : 

- INPUT  <- directory with images
- OUTPUT -> lst of local pages


3. Compare remote and locale lists

Case:

- remote.chapter.page == locale.chapter.page : do nothing.
- remote.chapter.page > locale.chapter.page :

    - list al the missing pages
    - download them 
        - using python request try first the page.png , if exception try page.jpg


4. Assemble the .cbz (recover some code from `chapters_maker.py`)

- Check for each chapter if remote.chapter.page == locale.chapter.page
    - if not: 
        - if .cbz exist : append missing pages
        - if .cbz doens't exist : create cbz with remote.chapter.page
