# File name: measures.py
# This program opens files and reutilizes the given measures.py script to
# modify it to our fit.
# Date: 22-05-2022
# Authors: Mathijs Afman, Maxim van der Maesen de Sombreff, Thijmen Adam

from collections import Counter
from nltk.metrics import ConfusionMatrix
import sys
import os


def open_files(path_name):
    """Opens all the needed files with the needed input.
    Input has to be /[folder_name]
    """
    cur_path = os.getcwd()
    group_path = cur_path + path_name

    final_lst = []
    for files in os.walk(group_path):
        for file in files:
            directory = files[0]
            if 'en.tok.off.pos.ent' in file:
                with open(directory + '/' + file[5], encoding='utf-8') as f:
                    sent_list = f.readlines()
                    for sent in sent_list:
                        lst = sent.split()
                        final_lst.append(lst)

    final_lst2 = []
    for files in os.walk(group_path):
        for file in files:
            directory = files[0]
            if 'en.tok.off.pos.aut' in file:
                with open(directory + '/' + file[4], encoding='utf-8') as f:
                    sent_list = f.readlines()
                    for sent in sent_list:
                        lst = sent.split()
                        final_lst2.append(lst)

    return final_lst, final_lst2


def check_tagged(line):
    """Checks if the line is longer than 5 items."""
    if len(line) > 5:
        return True


def check_tagged2(line):
    """Checks if the line is longer than 6 items."""
    if len(line) > 6:
        return True


def classified(annot1, annot2):
    """returns a list of tags for both annotators"""
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
    """returns a list of tags for both annotators"""
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
        fscore_list2.append(fscore)

    print("average f-score: ", sum(fscore_list2) / len(fscore_list2))

    print()
    print()
    print("If a wikipedia link was tagged and average f-score for every wikipedia link:")
    tagged1_wiki, tagged2_wiki = wikified(annot1, annot2)
    cm = ConfusionMatrix(tagged1_wiki, tagged2_wiki)

    lbs = set(tagged1_wiki + tagged2_wiki)

    true_positives, false_negatives, false_positives = find_true_pos(cm, lbs)

    # print("TP:", sum(true_positives.values()), true_positives)
    # print("FN:", sum(false_negatives.values()), false_negatives)
    # print("FP:", sum(false_positives.values()), false_positives)
    print()

    # wiki_list1 = []
    # wiki_list2 = []

    # for item in tagged1_wiki:
    #     if item != 'NONE':
    #         wiki_list1.append(item)

    # for item in tagged2_wiki:
    #     if item != 'NONE':
    #         wiki_list2.append(item)

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

    # TODO:
    #   Calculate not predicting a link when there should
    #   be one (check step 1 for checking wikipedia links in the assignment)

if __name__ == "__main__":
    main()
