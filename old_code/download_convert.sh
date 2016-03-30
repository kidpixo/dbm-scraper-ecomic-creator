#!/bin/bash

mkdir images
# download the jpg/colors pages,skipping the error
curl -f "http://www.dragonball-multiverse.com/en/pages/final/[0000-1160].jpg" -o "images/#1.jpg"

# dowload the bulk png pages, skipping errors
 curl -f "http://www.dragonball-multiverse.com/en/pages/final/[0000-1160].png" -o "images/#1.png"

mkdir trash

for i in $( ls images/*.jpg ); do
    echo item: $i
    convert $i `echo $i | cut -d"." -f 1`.png
    mv $i trash/
done

mkdir comics
