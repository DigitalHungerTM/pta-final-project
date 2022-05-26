# filename: ner_spacy.py
# author: Mathijs Afman
# description: ner tags and wikificates a file
# usage: python3 ner_spacy.py filename
# this script only writes files if
# it is a sibling of the group 9 folder

import spacy
import wikipedia as wk
import sys
NER = spacy.load('en_core_web_sm')


def open_file(filename):
    """opens a file"""
    with open(filename) as inp:
        return [line.split() for line in inp.readlines()]


def find_wiki_link(string):
    """tries to find a wikipedia link for a string,
     returns the link if found,
     returns 'ambiguous' if the string was ambiguous
     returns 'no page found' if no page was found"""
    try:
        return wk.page(wk.search(string)[0]).url
    except wk.exceptions.DisambiguationError:
        return 'ambiguous'
    except wk.exceptions.PageError:
        return 'no page found'


def gen_ner_wiki(ent):
    """formats an entity in the same way as en.tok.off.pos"""
    ent_start = ent.start_char
    token_start = ent_start
    ent_tokens = ent.text.split()
    spans = []
    spacy_label_lut = {
        'PERSON': 'PER',
        'GPE': 'CIT/COU',
        'LOC': 'NAT',  # klopt misschien niet helemaal
        'ORG': 'ORG',
        'NORP': 'ORG',  # neemt nationalities (zoals 'lebanese') ook mee
    }
    # spacy is missing ANIMAL, SPORT and ENTERTAINMENT
    # ANIMAL and SPORT are easy to tag with wordnet
    if ent.label_ in 'PERSON GPE LOC ORG NORP'.split():
        for token in ent_tokens:
            spans.append([token_start,
                          token_start + len(token),
                          spacy_label_lut[ent.label_],
                          find_wiki_link(ent.text)])
            token_start += len(token) + 1
        return spans
    return []


def append_ner_wiki(lines, tagged_spans):
    """appends the ner tag and wiki link
    to the lines with the correct character spans"""
    for line in lines:
        for span in tagged_spans:
            if int(line[0]) == int(span[0]):
                line.append(span[2])
                line.append(span[3])
    return lines


def write_file(filename, lines):
    """writes lines to a file"""
    with open(filename, 'w') as out:
        out.write('\n'.join([' '.join(line) for line in lines]))


def main():
    lines = open_file(sys.argv[1])
    tokens = [line[3] for line in lines]
    raw_text = ' '.join(tokens)
    ner_text = NER(raw_text)

    tagged_spans = []
    for ent in ner_text.ents:
        ner_wiki_spans = gen_ner_wiki(ent)
        for line in ner_wiki_spans:
            tagged_spans.append(line)

    ner_wiki_lines = append_ner_wiki(lines, tagged_spans)

    # this line only works if the script is run as sibling of group 9 folder
    write_file(sys.argv[1] + '.aut', ner_wiki_lines)

    # for line in ner_wiki_lines:
    #     print(line)

    # TODO:
    #  ondersteuning voor missende tags toevoegen
    #  onderscheiden van country en city in de GPE tag
    #    misschien door definition van de wiki page te checken
    #  ' '.join() is niet goed voor punctuation, introduceert bugs
    #    mogelijke oplossing is om de raw file te gebruiken
    #    of om spaties voor punctuation weg te halen


if __name__ == "__main__":
    main()
