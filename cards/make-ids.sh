#!/bin/sh

rm out/*

python ./formatter.py -p preamble.a4-by-4.ly.fragment -i "$1" -
lilypond -o out/out out/tunes.ly
pdfnup --nup 1x2 --suffix main out/out.pdf

