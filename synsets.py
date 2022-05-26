# filename: synsets.py
# author: Mathijs Afman
# description: A named entitiy recognizer using wordnet
# usage: python3 synsets.py filename

import sys
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from pprint import pprint
from ner import append_ner


def open_file(filename):
    """opens a file with name filename and returns
    a list of lists, split by spaces"""
    with open(filename) as inp:
        return [line.split() for line in inp.readlines()]


def format_text(line):
    """formats the lines to only contain the word and its pos-tag"""
    return line[3], line[4]


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return wn.NOUN


def append_lemma(token_pos):
    """takes a list of tagged tokens and appends
    the lemma for every token"""
    lemmatizer = WordNetLemmatizer()
    token = token_pos[0]
    pos_tag = token_pos[1]
    if pos_tag.startswith('J'):
        token_pos.append(lemmatizer.lemmatize(token, pos=wn.ADJ))
    elif pos_tag.startswith('V'):
        token_pos.append(lemmatizer.lemmatize(token, pos=wn.VERB))
    elif pos_tag.startswith('N'):
        token_pos.append(lemmatizer.lemmatize(token, pos=wn.NOUN))
    elif pos_tag.startswith('R'):
        token_pos.append(lemmatizer.lemmatize(token, pos=wn.ADV))
    else:
        token_pos.append(token)
    return token_pos


def append_synset(token_pos_lemma):
    """takes a list of tokens, pos tags and lemmas
    and appends a list of synsets for every token"""
    token_pos_lemma.append(wn.synsets(token_pos_lemma[2]))
    return token_pos_lemma


def main():
    lines = open_file(sys.argv[1])
    for line in lines:
        token_pos = [line[3], line[4]]
        token_pos_lemma = append_lemma(token_pos)
        token_pos_lemma_synset = append_synset(token_pos_lemma)
        token_pos_lemma_synset_ner = append_ner(token_pos_lemma_synset)
        print(token_pos_lemma_synset_ner[0], token_pos_lemma_synset_ner[1], token_pos_lemma_synset_ner[4])


if __name__ == "__main__":
    main()
