#!/bin/sh

rm out/*

python ./formatter.py -p preamble.a4-by-4.ly.fragment -i ../src/manuscripts -
lilypond -o out/out out/tunes.ly
pdfjam --landscape --nup '1x2' -o out/out-tmp.pdf -- out/out.pdf -

cp out/out.pdf manuscripts.pdf

# Nook doesn't support landscape, so rotate the source file
#pdfjam --angle '90' --fitpaper 'true' --rotateoversize 'true' -o complete.pdf -- out/out-tmp.pdf -

