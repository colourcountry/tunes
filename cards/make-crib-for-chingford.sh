#!/bin/sh

rm out/*

# Make crib sheets for all tunes

python ./formatter.py -p preamble.crib.mobile.ly.fragment -c - < chingford-morris-tunes.txt
#python ../src/indexer.py ids -s ../src/index.csv -k name | python ./formatter.py -p preamble.crib.mobile.ly.fragment -C -c -
lilypond -o out/out out/tunes.ly
mv out/out.pdf crib-for-chingford.pdf

#pdfjam walthamstow-folk-tune-book.pdf 1 out-main.pdf out-crib.pdf -o out.pdf

#lilypond -f png -dresolution=300 -o out/out out/out.ly
#eog out/*.png
