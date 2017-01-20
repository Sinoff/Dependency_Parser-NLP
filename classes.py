# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:52:35 2017

@author: okrupnik
"""

class Sentence(object):
    def __init__(self, sen_block):
        # parse sentence block from input file into data structure
        lines = [line.split('\t') for line in sen_block.split('\n')]
        properties = zip(*lines)
        self.words = ['ROOT'] + list(properties[1])
        self.pos = ['ROOT'] + list(properties[3])
        self.edges = []
        self.heads = ['_']*len(self.words)
        if '_' not in properties[6]:
            for c, p in enumerate(properties[6], 1):
                self.add_edge(int(p), c)
                self.heads[c] = [int(p)]
    
        self.feat_inds = []
        
        
    def get_word_pos(self, ind):
        return self.words[ind], self.pos[ind]
        
    def add_edge(self, p_ind, c_ind):
        self.edges.append((p_ind, c_ind))
        
    def __repr__(self):
        # implement sentence print        
        emptys = ['_']*len(self.words)
        data = zip(range(1, len(self.words) + 1), self.words, emptys, self.pos, 
                   emptys, emptys, self.heads, emptys, emptys)
        text = '\n'.join(['\t'.join([str(obj) for obj in line]) for line in data])
        return text
        
    def __str__(self):
        # Easy debug representation of sentence
        return ' '.join([word + '_' + pos for word, pos in 
                         zip(self.words, self.pos)[1:]]) + '\n'