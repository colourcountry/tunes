#!/bin/sh

mkdir -p split
cd split
cat ../sessions/*.abc | csplit -s -n 3 - '/^X:/' '{*}'

for FILE in `egrep '^X:' xx* --files-with-match`
do
  mv $FILE "`head -n 1 $FILE | sed -e 's/X://'`.abc"
done

