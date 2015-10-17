#!/bin/sh

rm out/*

python ../src/indexer.py ids -i ../src/index.csv -k name |\
python ./formatter.py -p preamble.mobile.ly.fragment -
lilypond -o out/out out/tunes.ly
pdfjam --landscape --nup '1x2' -o out/out-tmp.pdf -- out/out.pdf -

mv out/out-tmp.pdf complete.pdf
# Nook doesn't support landscape, so rotate the source file
#pdfjam --angle '90' --fitpaper 'true' --rotateoversize 'true' -o complete.pdf -- out/out-tmp.pdf -
echo 'Wrote complete.pdf'
