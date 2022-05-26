# filename: ner.py
# author: Mathijs Afman
# description: a helper script that provides functions for ner tagging
# usage: python3 ner.py filename

from nltk.corpus import wordnet as wn

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


def append_ner(token_pos_lemma_synsets):
    hypernym_dict = {
        'COUNTRY': [wn.synset("country.n.01"), wn.synset('country.n.02')],
        'PERSON': [wn.synset('person.n.01'), wn.synset('person.n.02')],
        'NATURAL': [wn.synset('geological_formation.n.01'), wn.synset('body_of_water.n.01'), wn.synset('vegetation.n.01')],
        'CITY': [wn.synset('city.n.01'), wn.synset('city.n.02'), wn.synset('city.n.03')],
        'ORGANIZATION': [wn.synset('social_group.n.01')],
        'ANIMAL': [wn.synset('animal.n.01')],
        'SPORT': [wn.synset('sport.n.01')],
        'ENTERTAINMENT': [wn.synset('book.n.01'), wn.synset('movie.n.01')]
    }

    synsets = token_pos_lemma_synsets[3]
    for ner_tag in hypernym_dict:
        for hypernym in hypernym_dict[ner_tag]:
            for synset in synsets:
                if hypernym_of(synset, hypernym):
                    token_pos_lemma_synsets.append(ner_tag[:3])
                    break
    if len(token_pos_lemma_synsets) != 5:
        token_pos_lemma_synsets.append('NONE')
    return token_pos_lemma_synsets


def main():
    return


if __name__ == "__main__":
    main()
