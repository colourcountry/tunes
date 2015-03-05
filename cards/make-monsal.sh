#!/bin/sh

rm out/*

grep 'X:' ../src/new/monsal.abc | sed -e 's/X://' |\
python ./formatter.py -p preamble.a4-by-4.ly.fragment -S -O -N -
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape --suffix main out/out.pdf

mv out-main.pdf monsal.pdf

