#!/bin/sh

rm out/*

# Start with the specially chosen easy tunes

python ./formatter.py -p preamble.mobile.ly.fragment -S -X - < ids/easy.ids
lilypond -o out/out out/tunes.ly
pdfnup --nup 1x2 --papersize '{3.6in,6.4in}' -o out/out-easy.pdf out/out.pdf

# Get all WFS tunes with high popularity and format them in full (without chords)

#python ../src/indexer.py ids -s ../src/index.csv -p 6 -f WFS -k name > ids/main.ids
python ./formatter.py -p preamble.mobile.ly.fragment -S -X - < ids/main.ids
lilypond -o out/out out/tunes.ly
pdfnup --nup 1x2 --papersize '{3.6in,6.4in}' -o out/out-main.pdf out/out.pdf

# Make crib sheets for tunes with medium popularity

#python ../src/indexer.py ids -s ../src/index.csv -p 2 -f WFS -k name > ids/crib.ids
python ./formatter.py -p preamble.crib.mobile.ly.fragment -c - < ids/crib.ids
lilypond -o out/out-crib out/tunes.ly

# Stitch up with front page of original tune book

pdfjam out/out-easy.pdf out/out-main.pdf out/out-crib.pdf --papersize '{6.4in,3.6in}' -o walthamstow-tunebook-mobile.pdf

#pdfjam walthamstow-folk-tune-book.pdf 1 out-main.pdf out-crib.pdf -o out.pdf

#lilypond -f png -dresolution=300 -o out/out out/out.ly
#eog out/*.png
