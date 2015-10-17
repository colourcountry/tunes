#!/bin/sh

rm out/*

echo '' | python ./formatter.py -p preamble.a4-by-4.ly.fragment -i "$1" -v - 2>out/fail.abc
lilypond -o out/out out/tunes.ly
#pdfjam --landscape --nup '1x2' -o out/out-tmp.pdf -- out/out.pdf -
pdfjam --nup '1x4' -o out/out-tmp.pdf --no-tidy -- out/out.pdf -

cp out/out-tmp.pdf "$(basename $1 .abc).pdf"
echo "Wrote $(basename $1 .abc).pdf"

# Nook doesn't support landscape, so rotate the source file
#pdfjam --angle '90' --fitpaper 'true' --rotateoversize 'true' -o complete.pdf -- out/out-tmp.pdf -

