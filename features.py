# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 22:30:07 2017

@author: okrupnik
"""

"""
FEATURES module: 
extracts fetaures from words, parse corpus, save feature tables
"""

num_feat_types = 13
model = 'basic'

features = [{} for _ in xrange(num_feat_types + 1)]

### parse corpus and make features work

get_feat_ind = [lambda p, c, p_pos, c_pos: (p, c), 
                lambda p, c, p_pos, c_pos: features[1][p][p_pos],
                lambda p, c, p_pos, c_pos: features[2][p],
                lambda p, c, p_pos, c_pos: features[3][p_pos],
                lambda p, c, p_pos, c_pos: features[4][c][c_pos],
                lambda p, c, p_pos, c_pos: features[5][c],
                lambda p, c, p_pos, c_pos: features[6][c_pos],
                lambda p, c, p_pos, c_pos: features[7][p][c][p_pos][c_pos],
                lambda p, c, p_pos, c_pos: features[8][c][p_pos][c_pos],
                lambda p, c, p_pos, c_pos: features[9][p][c][c_pos],
                lambda p, c, p_pos, c_pos: features[10][p][p_pos][c_pos],
                lambda p, c, p_pos, c_pos: features[11][p][c][p_pos],
                lambda p, c, p_pos, c_pos: features[12][p][c],
                lambda p, c, p_pos, c_pos: features[13][p_pos][c_pos]
                ]

def get_feature_list(sentence, p_ind, c_ind):
    p, p_pos = sentence.get_word_pos(p_ind)
    c, c_pos = sentence.get_word_pos(c_ind)
    model_features = range(1, num_feat_types + 1)    

    if 'basic' in model:
        model_features = list(set(model_features) - set([7, 9, 11, 12]))
    
    return [get_feat_ind[i](p, c, p_pos, c_pos) for i in model_features]
    