#!/bin/sh

rm out/*

python ./formatter.py -p preamble.a4-by-4.ly.fragment -S -O -N -C - < ids/stoneydown.ids
lilypond -o out/out out/tunes0.ly
pdfnup --nup 1x4 --no-landscape --suffix main out/out.pdf

