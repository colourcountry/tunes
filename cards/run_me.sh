#!/bin/sh

rm out/*.png
python ./formatter.py "$@" > out/out.ly
lilypond -o out/out out/tunes0.ly
#lilypond -f png -dresolution=300 -o out/out out/out.ly
#eog out/*.png
