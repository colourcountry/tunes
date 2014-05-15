#!/bin/sh

rm out/*
python ./formatter.py "$@" > out/out.ly
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape out/out.pdf

#lilypond -f png -dresolution=300 -o out/out out/out.ly
#eog out/*.png
