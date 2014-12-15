#!/usr/bin/python
#
#  File name:   dp1.py
#  Author:      Melanie Tosik
#  Platform:    OS X (10.9.5)
#  Description: Statistics on semantic dependency graphs

from __future__ import division
import sys
import string
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np 

class Sim(object):
    """ Provides some basic statistics on semantic dependency graphs """

    def __init__(self, simfile):
        # Dictionary {indegree=outdegree : number of words with inoutdegree}
        self.inoutdegree = {}
        self.numbers(simfile)
        self.plots()

    def numbers(self, simfile):

        # f = open(simfile, 'a')
        # f.write('\n\n')
        # f.close()

        # Contains current sentence
        sentence = []
        # Set of different edge labels
        label_set = set()
        # Count number of sentences
        number_of_sentences = 0
        # Count number of words
        number_of_words = 0
        # Count number of predicates
        number_of_predicates = 0
        # Count number of singletons
        number_of_singletons = 0

        with open(simfile, 'r+') as f:
            for line in f:
                # Gets single sentences
                if line.strip(): #< DEBUG: file ending with '\n\n'
                    sentence.append(line.split('\t'))
                else:
                    number_of_sentences += 1
                    # Processes current sentence
                    for field_line in sentence:
                        # Ignores sentence prefixes
                        if len(field_line) > 1:

                            # Fields 1-4: id, form, lemma, pos
                            if field_line[1] not in string.punctuation:
                                number_of_words += 1

                                # Indegree = outdegree = number of pred-arg roles
                                arg_cnt = 0
                                for field in field_line[6:]:
                                    if field.strip() not in string.punctuation:
                                        arg_cnt += 1

                                if arg_cnt in self.inoutdegree.keys():
                                    self.inoutdegree[arg_cnt] = self.inoutdegree[arg_cnt] + 1
                                else:
                                    self.inoutdegree[arg_cnt] = 1

                            # Fields 5,6: top, pred
                            if field_line[5] == '+':
                                number_of_predicates += 1    

                            # Additional fields starting from 7: pred-arg roles
                            for field in field_line[6:]:
                                if field.strip() not in string.punctuation:
                                    label_set.add(field.strip())

                            # Singletons
                            # Neither top nor pred and no pred-arg roles
                            if field_line[4:6] == ['-','-'] and all(field.strip() == '_' for field in field_line[6:]):
                                number_of_singletons += 1

                    sentence = []

            print 'Number of graphs:', number_of_sentences
            print 'Number of words:', number_of_words
            print 'Number of different edge labels:', len(label_set)
            print 'Average number of predicates per sentence:', round((number_of_predicates/number_of_sentences),1)
            print 'Average number of singletons per sentence:', round((number_of_singletons/number_of_sentences),1)
            #print self.inoutdegree

    def plots(self):
        histogram = sorted(self.inoutdegree.items(), key=itemgetter(0), reverse=False)
        inout_max = histogram[-1][0]

        hist_dict = dict(histogram)
        print hist_dict

        fig = plt.figure()
        x_axis = []
        y_axis = []

        for i in hist_dict.keys():
            x_axis.append(i)
            y_axis.append(hist_dict[i])

        plt.xticks(x_axis)

        out = plt.subplot(111)
        out.bar(x_axis, y_axis, width=0.25, align='center')

        out.set_xlabel('indegree=outdegree')
        out.set_ylabel('number of words')
        plt.show()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sim = Sim(sys.argv[1])
    else:
        print 'Usage: python dp1.py <file>'