#!/bin/sh

rm out/*

python ../src/indexer.py ids -s ../src/index.csv -k name |\
python ./formatter.py -p preamble.a4-by-4.ly.fragment -
lilypond -o out/out out/tunes0.ly
pdfjam --landscape --nup '1x2' -o out/out-tmp.pdf -- out/out.pdf -

# Nook doesn't support landscape, so rotate the source file
pdfjam --angle '90' --fitpaper 'true' --rotateoversize 'true' -o complete.pdf -- out/out-tmp.pdf -

