# pta-final-project

## Installation of packages:
```commandline
pip install --upgrade setuptools wheel
pip install wikipedia
pip install nltk
python3 -m ntlk.downloader wordnet
pip install spacy
python3 -m spacy download en_core_web_sm
```
## Usage:
make sure the ner_spacy.py file is a sibling
of the folder containing the folders containing
the files and run
```commandline
python3 ner_spacy.py folder/folder/
```
example:
```commandline
python3 ner_spacy.py group9/d0056/
```