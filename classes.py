# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:52:35 2017

@author: okrupnik
"""

class Sentence(object):
    def __init__(self, sen_block):
        # parse sentence block from input file into data structure
        pass
    
    def get_word_pos(self, ind):
        return self.words(ind), self.pos(ind)