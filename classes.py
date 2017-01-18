# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:52:35 2017

@author: okrupnik
"""

class Sentence(object):
    def __init__(self, sen_block):
        # parse sentence block from input file into data structure
        lines = [line.split('\t') for line in sen_block.split('\n')]
        properties = zip(lines)
        self.words = ['ROOT'] + list(properties[1])
        self.pos = ['ROOT'] + list(properties[3])
        self.edges = []
        if '_' not in properties[6]:
            for c, p in enumerate(properties[6], 1):
                self.add_edge(p, c)
    
        self.feat_inds = []
        
        
    def get_word_pos(self, ind):
        return self.words(ind), self.pos(ind)
        
    def add_edge(self, p_ind, c_ind):
        self.edges.append((p_ind, c_ind))
        
    def print_sentence(self):
        # implement sentence print        
        
        pass