# pta-final-project

## Installation of packages:
```commandline
pip3 install --upgrade setuptools wheel
pip3 install wikipedia
pip3 install lxml
pip3 install nltk
python3 -m nltk.downloader wordnet
pip3 install spacy
python3 -m spacy download en_core_web_sm
```
in Ubuntu go to $HOME/.local/lib/python3.8/site-packages/wikipedia
and edit wikipedia.py. Edit line 389 for the BeautifulSoup constructor
to have ```"features='lxml'"``` as an argument so that the line reads:
```lis = BeautifulSoup(html, features='lxml').find_all('li')```
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
