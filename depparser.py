# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:56:03 2017

@author: okrupnik
"""

from classes import Sentence
import features


def parse(filename, training):
    with open(filename, 'r') as f:
        sen_blocks = f.read().split('\n\n')
        if not len(sen_blocks[-1]):
            del sen_blocks[-1]
        
    sentences = []
    for block in sen_blocks:
        sentence = Sentence(block, training)
        if training:
            for p, c in sentence.edges:
                f_inds = features.set_features(sentence.get_word_pos(p),
                                               sentence.get_word_pos(c))
                for f in f_inds:
                    if f in sentence.feat_inds:
                        sentence.feat_inds[f] += 1
                    else:
                        sentence.feat_inds[f] = 1
                        
        sentences.append(sentence)
        
    return sentences



def parse_for_comparison(file1, file2):
    sen_blocks = [[], []]    
    for ind, filename in enumerate([file1, file2]):
        with open(filename, 'r') as f:
            sen_blocks[ind] = f.read().split('\n\n')
            if not len(sen_blocks[ind][-1]):
                del sen_blocks[ind][-1]
        
    total_edges = 0
    wrong_edges = 0        
    for block1, block2 in zip(*sen_blocks):
        sentence1 = Sentence(block1, True)
        sentence2 = Sentence(block2, True)
        assert((sentence1.words == sentence2.words) and 
               (sentence1.pos == sentence2.pos)), "Files compared have different sentences"
        
        for h1, h2 in zip(sentence1.heads, sentence2.heads):
            total_edges += 1
            if h1 != h2:
                wrong_edges += 1
        
    return 100.0 * wrong_edges / total_edges