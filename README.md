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
Run the wikificator.py file to loop through folders.
```commandline
python3 wikificator.py folder
```
Make sure that the folder containing the folders with .pos files is a sibling of wikificatory.py  
example:
```commandline
python3 wikificator.py dev
```

This puts the .ent files in a 'results' folder which is a sibling of wikificator.py, remove the results folder to run the program again.

You can also use the wikificator_ui.py file.  
```commandline
streamlit run wikificator_ui.py
```

You can use this and upload both a .raw and .pos file from the same folder and see the results in a simple ui.