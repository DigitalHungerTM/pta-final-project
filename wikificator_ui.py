# filename: wikificator.py
# author: Mathijs Afman, Maxim van der Maesen de Sombreff, Thijmen Adam
# description: ner tags and wikificates a file, input on the streamlit
# Should be a .raw file and a .pos file from the same directory.
# usage: streamlit run wikificator_ui.py
# date: 05-06-2022

import spacy
import wikipedia as wk
from io import StringIO
import streamlit as st
from random import random
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

NER = spacy.load('en_core_web_sm')


def find_wiki_link(string):
    """tries to find a wikipedia link for a string,
     returns the link if found,
     returns 'ambiguous' if the string was ambiguous
     returns 'no_page_found' if no page was found"""
    try:
        return wk.page(wk.search(string)[0]).url
    except wk.exceptions.DisambiguationError:
        return 'ambiguous'
    except wk.exceptions.PageError:
        return 'no_page_found'


def disambiguate_gpe(term):
    try:
        summary = wk.page(wk.search(term)[0]).summary
        # the definition is usually mentioned first
        for word in summary.split():
            if word == 'city' or word == 'town':
                return 'CIT'
            elif word == 'country':
                return 'COU'

        if random() >= 0.5:
            return 'CIT'
        else:
            return 'COU'
    # if page not found it guesses
    except wk.exceptions.DisambiguationError:
        if random() >= 0.5:
            return 'CIT'
        else:
            return 'COU'
    except wk.exceptions.PageError:
        if random() >= 0.5:
            return 'CIT'
        else:
            return 'COU'


def spacy_gen_ner_wiki(ent):
    """formats an entity in the same way as en.tok.off.pos
    and appends an ner tag and a wiki link using spacy"""
    ent_start = ent.start_char
    token_start = ent_start
    ent_tokens = ent.text.split()
    spans = []
    spacy_label_lut = {
        'PERSON': 'PER',
        'GPE': 'GPE',
        'LOC': 'NAT',  # klopt misschien niet helemaal
        'ORG': 'ORG',
        'NORP': 'ORG',  # neemt nationalities (zoals 'lebanese') ook mee
    }
    # filters on only wanted NER tags
    if ent.label_ in 'PERSON GPE LOC ORG NORP'.split():
        for token in ent_tokens:
            spans.append([token_start,
                          token_start + len(token),
                          spacy_label_lut[ent.label_],
                          find_wiki_link(ent.text)])
            token_start += len(token) + 1

        for span in spans:
            if span[2] == 'GPE':
                span[2] = disambiguate_gpe(ent.text)
        return spans
    return []


def append_spacy_ner_wiki(lines, tagged_spans):
    """appends the ner tag and wiki link
    to the lines with the correct character spans"""
    for line in lines:
        for span in tagged_spans:
            if int(line[0]) == int(span[0]):
                line.append(span[2])
                line.append(span[3])
    return lines


def hypernym_of(synset1, synset2):
    """ Returns True if synset2 is a hypernym of
    synset1, or if they are the same synset.
    Returns False otherwise. """
    if synset1 == synset2:
        return True
    for hypernym in synset1.hypernyms():
        if synset2 == hypernym:
            return True
        if hypernym_of(hypernym, synset2):
            return True
    return False


def wordnet_gen_ner_wiki(lines):
    """takes a list of tokens and pos-tags and appends
    ner tags and wikis for lines that haven't already
    been tagged using wordnet

    this tagger only works for nouns (for now?)"""
    lemmatizer = WordNetLemmatizer()
    hypernym_dict = {
        'ANIMAL': wn.synset('animal.n.01'),
        'SPORT': wn.synset('sport.n.01'),
        'ENTERTAINMENT': wn.synset('book.n.01'),
        'ENTERTAINMENT1': wn.synset('movie.n.01'),
        'ENTERTAINMENT2': wn.synset('newspaper.n.01'),
        'ENTERTAINMENT3': wn.synset('magazine.n.01')
    }
    for line in lines:
        if len(line) > 4:
            word = line[3]
            pos_tag = line[4]
            if len(line) == 5:  # only un-tagged lines
                if pos_tag.startswith('N'):  # word is a noun
                    lemma = lemmatizer.lemmatize(word)
                    for synset in wn.synsets(lemma):
                        for ner_tag in hypernym_dict:
                            if hypernym_of(synset, hypernym_dict[ner_tag]):
                                line.append(ner_tag[:3])
                                line.append(find_wiki_link(word))
                                break
                                # to prevent a word from getting bot tags
                        break
    return lines


def main():

    st.title("Wikificator, Project Text Analysis")
    st.write("Mathijs Afman, Maxim van der Maesen de Sombreff, Thijmen Adam")
    st.write("For this streamlit UI you will have to upload both a .pos file"
             " and a .raw file in the corresponding upload boxes. These "
             "files should be in the same directory and the pos-tagged file "
             "has to be a pos-tagged file adapted from the .raw file. Once you have"
             " uploaded the files it will run the program and showcase the wikified"
             " clickable links in a text. It will not be 100\% accurate.")
    lines = st.file_uploader("Please upload a .pos file here", type=["pos"])
    raw_text = st.file_uploader("Please upload a .raw file here", type=["raw"])
    stringio = StringIO(lines.getvalue().decode("utf-8"))


    if lines is not None and raw_text is not None:
        lines = [line.split() for line in stringio.readlines()]
        ner_text = NER(raw_text.read().decode('UTF-8'))

        tagged_spans = []
        for ent in ner_text.ents:
            ner_wiki_spans = spacy_gen_ner_wiki(ent)
            for line in ner_wiki_spans:
                tagged_spans.append(line)

        spacy_ner_wiki_lines = append_spacy_ner_wiki(lines, tagged_spans)

        complete_ner_wiki_lines = wordnet_gen_ner_wiki(spacy_ner_wiki_lines)

        line_list = []

        for line in complete_ner_wiki_lines:
            line_list.append(line)

        print_string = ""

        for item in line_list:
            if len(item) > 4:
                if len(item) > 5:
                    if "https" in item[6]:
                        print_string += " ["+ item[3] +"]("+ item[6]+ ")"
                else:
                    print_string += " " + item[3]

        st.write(print_string)

                # TODO:
                #  ondersteuning voor missende tags toevoegen
                #    alleen nog entertainment
                # TODO:
                #  onderscheiden van country en city in de GPE tag
                #    misschien door definition van de wiki page te checken
                # TODO:
                #  voor delen van namen misschien de wiki pagina kopieren
                #  genoemde namen


if __name__ == "__main__":
    main()
