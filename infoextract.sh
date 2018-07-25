#!/bin/bash

pip install --user nltk
unzip stanford-corenlp-full-2017-06-09.zip
pip install --user stanfordcorenlp
python nltk_download.py

python infoextract.py $1
