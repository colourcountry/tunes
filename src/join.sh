#!/bin/sh

./split.sh

python ./indexer.py filenames | xargs -d '\n' cat


