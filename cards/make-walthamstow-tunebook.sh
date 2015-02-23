#!/bin/sh

rm out/*

# Start with the specially chosen easy tunes

python ./formatter.py -p preamble.a4-by-4.ly.fragment -S - < ids/easy.ids
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape --suffix easy out/out.pdf

# Get all WFS tunes with high popularity and format them in full (without chords)

#python ../src/indexer.py ids -s ../src/index.csv -p 6 -f WFS -k name 
python ./formatter.py -p preamble.a4-by-4.ly.fragment -S -C - < ids/main.ids
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape --suffix main out/out.pdf

# Make crib sheets for tunes with medium popularity

#python ../src/indexer.py ids -s ../src/index.csv -p 4 -P 6 -f WFS -k name
python ./formatter.py -p preamble.crib.a4-by-4.ly.fragment -c - < ids/crib.ids
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape --suffix crib out/out.pdf

# Stitch up with front page of original tune book

pdfjam out-easy.pdf out-main.pdf out-crib.pdf -o walthamstow-tunebook.pdf

rm out-easy.pdf out-main.pdf out-crib.pdf

#pdfjam walthamstow-folk-tune-book.pdf 1 out-main.pdf out-crib.pdf -o out.pdf

#lilypond -f png -dresolution=300 -o out/out out/out.ly
#eog out/*.png
