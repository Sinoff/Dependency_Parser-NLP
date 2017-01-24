# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:52:35 2017

@author: okrupnik
"""


class EdgeData(object):
    def __init__(self, sentence, p_ind, c_ind):
        self.p_ind = p_ind
        self.c_ind = c_ind
        self.p_word = sentence.words[p_ind]
        self.p_pos = sentence.pos[p_ind]
        self.c_word = sentence.words[c_ind]
        self.c_pos = sentence.pos[c_ind]
        self.dist = c_ind - p_ind
        self.sen_len = len(sentence.words) - 1
        if p_ind > 1:  # root is not interesting
            self.p_pre_pos = sentence.pos[p_ind-1]
        if p_ind < self.sen_len - 1:  # root is not interesting
            self.p_next_pos = sentence.pos[p_ind + 1]
        if c_ind > 1:  # root is not interesting
            self.c_pre_pos = sentence.pos[c_ind-1]
        if c_ind < self.sen_len - 1:  # root is not interesting
            self.c_next_pos = sentence.pos[c_ind + 1]

class Sentence(object):
    def __init__(self, sen_block, training):
        # parse sentence block from input file into data structure
        lines = [line.split('\t') for line in sen_block.split('\n') 
                 if line != '']
        properties = zip(*lines)
        self.words = ['ROOT'] + list(properties[1])
        self.pos = ['ROOT'] + list(properties[3])
        self.edges = []
        self.edge_data = {}
        self.heads = ['_']*len(self.words)
        if training:
            for c, p in enumerate(properties[6], 1):
                self.add_edge(int(p), c)

        self.feat_inds = {}
        
        
    def get_word_pos(self, ind):
        return self.words[ind], self.pos[ind]
        
    def add_edge(self, p_ind, c_ind):
        self.heads[c_ind] = p_ind
        self.edges.append((p_ind, c_ind))
        if p_ind in self.edge_data:
            self.edge_data[p_ind][c_ind] = EdgeData(self, p_ind, c_ind)
        else:
            self.edge_data[p_ind] = {c_ind : EdgeData(self, p_ind, c_ind)}
        
    def __repr__(self):
        # implement sentence print        
        emptys = ['_']*len(self.words[1:])
        data = zip(range(1, len(self.words) + 1), self.words[1:], emptys, 
                   self.pos[1:], emptys, emptys, self.heads[1:], emptys,
                   emptys, emptys)
        text = '\n'.join(['\t'.join([str(obj) for obj in 
                          line]) for line in data])
        return text
        
    def __str__(self):
        # Easy debug representation of sentence
        return ' '.join([word + '_' + pos for word, pos in 
                         zip(self.words, self.pos)[1:]]) + '\n'