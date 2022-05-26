# filename: 
# author: 
# description: short script that tries to find a wikipedia
# page for a given term
# usage: python3 wiki.py
# edited line 389 of $HOME/.local/lib/python3.10/site-packages/wikipedia/wikipedia.py
# for the BeautifulSoup constructor to have features='lxml' as an argument

import wikipedia as wk
from time import time


def find_wiki_link(string):
    """tries to find a wikipedia link for a string,
     returns the link if found,
     returns 'ambiguous' if the string was ambiguous"""
    try:
        return wk.page(wk.search(string)[0]).url
    except wk.exceptions.DisambiguationError:
        return 'ambiguous'
    except wk.exceptions.PageError:
        return 'no page found'


def main():
    terms = 'at-least-three'.split()
    for term in terms:
        start = time()
        link = find_wiki_link(term)
        end = time()
        print(f'{term}, {link}, took {end-start:.1f} seconds')


if __name__ == "__main__":
    main()
