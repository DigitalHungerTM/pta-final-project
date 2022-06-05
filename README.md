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
Run the wikificator.py file to loop through folders. Once an error pops, a mistake has been found in one of the folders. It says which folder you were working on. Delete that folder and rerun the wikificator.py until it works fine.
```commandline
python3 wikificator.py folder/
```
example:
```commandline
python3 wikificator.py dev/
```

You can also use the wikificator_ui.py file.  
```commandline
streamlit run wikificator_ui.py
```

You can use this and upload both a .raw and .pos file from the same folder and see the results in a simple ui.
