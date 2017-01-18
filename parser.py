# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:56:03 2017

@author: okrupnik
"""

from classes import Sentence
import features


def corpus_parser(filename):
    with open(filename, 'r') as f:
        sen_blocks = f.read().split('\n\n')
        
    sentences = []
    for block in sen_blocks:
        sentence = Sentence(block)  
        for p, c in sentence.edges:
            sentence.feat_inds += features.set_features(sentence.get_word_pos(p), 
                                                        sentence.get_word_pos(c))
        sentences.append(sentence)
        
    return features.num_features, sentences
    