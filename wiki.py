# filename: 
# author: 
# description: short script that tries to find a wikipedia
# page for a given term
# usage: python3 wiki.py
# edited line 389 of $HOME/.local/lib/python3.10/site-packages/wikipedia/wikipedia.py
# for the BeautifulSoup constructor to have features='lxml' as an argument

import wikipedia as wk
from time import time
from random import random


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


def find_page_contents(term):
    """"""
    try:
        summary =  wk.page(wk.search(term)[0]).summary
        if 'country' in summary:
            return 'COU'
        else:
            return 'CIT'

    # page not found or page is ambiguous
    except wk.exceptions.DisambiguationError or wk.exceptions.PageError:
        return 'not sure'


def main():
    terms = 'Venezuela'.split()
    for term in terms:
        start = time()
        link = find_wiki_link(term)
        summary = find_page_contents(term)
        end = time()
        print(f'{term}, {link}, took {end-start:.1f} seconds')
        print(summary)


if __name__ == "__main__":
    main()
