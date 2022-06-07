# File name: measures.py
# This program opens files and reutilizes the given measures.py script to
# modify it to our fit.
# Date: 22-05-2022
# Authors: Mathijs Afman, Maxim van der Maesen de Sombreff, Thijmen Adam
# usage: python3 measures.py folder/ folder2/
# example: python3 measures.py dev/ results/

from collections import Counter
from nltk.metrics import ConfusionMatrix
import sys
import os


def open_files(path_name):
    """
    Opens all files in the folder with name folder_name
    example of a folder_name: 'dev/'
    and returns a list of all split lines of all files
    """

    ent_list = []
    aut_list = []
    directory = sys.argv[1]
    directory2 = sys.argv[2]
    folders = os.listdir(directory)
    folders2 = os.listdir(directory2)
    for folder in folders:
        with open(f'{directory}/{folder}/en.tok.off.pos.ent',
                  encoding='utf-8') as inp:
            for line in inp.readlines():
                ent_list.append(line.split())

    for folder2 in folders2:
        with open(f'{directory2}/{folder2}/en.tok.off.pos.ent',
                  encoding='utf-8') as inp:
            for line in inp.readlines():
                aut_list.append(line.split())

    return ent_list, aut_list


def check_tagged(line):
    """Checks if the line is longer than 5 items."""
    if len(line) > 5:
        return True


def check_tagged2(line):
    """Checks if the line is longer than 6 items."""
    if len(line) > 6:
        return True


def classified(annot1, annot2):
    """returns a list of tags for both files"""
    ref = []
    tagged = []
    for i in range(len(annot1)):
        if check_tagged(annot1[i]):
            ref.append(annot1[i][5])
        else:
            ref.append('NONE')
        if check_tagged(annot2[i]):
            tagged.append(annot2[i][5])
        else:
            tagged.append('NONE')

    return ref, tagged


def wikified(annot1, annot2):
    """returns a list of tags (wiki) for both files"""
    ref = []
    tagged = []
    for i in range(len(annot1)):
        if check_tagged2(annot1[i]):
            ref.append(annot1[i][6])
        else:
            ref.append('NONE')
        if check_tagged2(annot2[i]):
            tagged.append(annot2[i][6])
        else:
            tagged.append('NONE')

    return ref, tagged


def find_true_pos(cm, labels):
    """takes a confusion matrix and all its labels and returns
    true-positives, false-negatives and false-positives
    """

    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cm[i, j]
            else:
                false_negatives[i] += cm[i, j]
                false_positives[j] += cm[i, j]

    return true_positives, false_negatives, false_positives


def main():

    annot1, annot2 = open_files(sys.argv[1])
    tagged1 = []
    tagged2 = []

    for i in range(len(annot1)):
        if check_tagged(annot1[i]) and check_tagged(annot2[i]):
            tagged1.append((annot1[i][3], annot1[i][5]))
            tagged2.append((annot2[i][3], annot2[i][5]))

    tagged_set1 = [tag for word, tag in tagged1]
    tagged_set2 = [tag for word, tag in tagged2]
    cm = ConfusionMatrix(tagged_set1, tagged_set2)

    print("Confusion matrix and f-score for "
          "interesting entities vs non-interesting entities:")
    print(cm)

    labels = set(tagged_set1 + tagged_set2)

    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cm[i, j]
            else:
                false_negatives[i] += cm[i, j]
                false_positives[j] += cm[i, j]

    print("TP:", sum(true_positives.values()), true_positives)
    print("FN:", sum(false_negatives.values()), false_negatives)
    print("FP:", sum(false_positives.values()), false_positives)
    print()

    fscore_list = []
    for i in sorted(labels):
        if true_positives[i] == 0:
            fscore = 0
        else:
            precision = true_positives[i] / float(true_positives[i] +
                                                  false_positives[i])

            recall = true_positives[i] / float(true_positives[i] +
                                               false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)
            print("precision: ", i, precision)
            print("recall: ", i, recall)
        print("f-score:", i, fscore)
        print()

        fscore_list.append(fscore)

    print("average f-score: ", sum(fscore_list) / len(fscore_list))

    print()
    print()
    print("Confusion matrix and f-score for every entity:")
    tagged1, tagged2 = classified(annot1, annot2)
    cm = ConfusionMatrix(tagged1, tagged2)
    print(cm)
    lbs = set(tagged1 + tagged2)

    true_positives, false_negatives, false_positives = find_true_pos(cm, lbs)

    print("TP:", sum(true_positives.values()), true_positives)
    print("FN:", sum(false_negatives.values()), false_negatives)
    print("FP:", sum(false_positives.values()), false_positives)
    print()

    fscore_list2 = []
    for i in sorted(lbs):
        if true_positives[i] == 0:
            fscore = 0
        else:
            precision = true_positives[i] / float(true_positives[i] +
                                                  false_positives[i])
            recall = true_positives[i] / float(true_positives[i] +
                                               false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)
            print("precision: ", i, precision)
            print("recall: ", i, recall)
        print("f-score:", i, fscore)
        print()
        fscore_list2.append(fscore)

    print("average f-score: ", sum(fscore_list2) / len(fscore_list2))

    print()
    print("Score if a wikipedia link was tagged and "
          "average f-score for every wikipedia link:")
    tagged1_wiki, tagged2_wiki = wikified(annot1, annot2)
    cm = ConfusionMatrix(tagged1_wiki, tagged2_wiki)

    lbs = set(tagged1_wiki + tagged2_wiki)

    true_positives, false_negatives, false_positives = find_true_pos(cm, lbs)

    # print("TP:", sum(true_positives.values()), true_positives)
    # print("FN:", sum(false_negatives.values()), false_negatives)
    # print("FP:", sum(false_positives.values()), false_positives)
    print()

    fscore_wiki = []
    for i in sorted(lbs):
        if true_positives[i] == 0:
            fscore = 0
        else:
            precision = true_positives[i] / float(true_positives[i] +
                                                  false_positives[i])
            recall = true_positives[i] / float(true_positives[i] +
                                               false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)

        fscore_wiki.append(fscore)

    print("average f-score: ", sum(fscore_wiki) / len(fscore_wiki))

    wikilist = []
    for item in annot1:
        if len(item) > 6 and item[6] != "":
            wikilist.append(item)

    wikilist2 = []
    for item2 in annot2:
        if len(item2) > 6 and item2[6] != "":
            wikilist2.append(item)

    print()
    print("How many times a link was predicted by us when "
          "there shouldn't have been one: ",
          len(wikilist2) - len(wikilist))
    # TODO:
    #   Calculate not predicting a link when there should
    #   be one (check step 1 for checking wikipedia links in the assignment)


if __name__ == "__main__":
    main()
