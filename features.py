# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 22:30:07 2017

@author: okrupnik
"""

import pickle
import os

"""
FEATURES module: 
extracts fetaures from words, parse corpus, save feature tables
"""

num_feat_types = 13
num_features = 0
model = 'basic'

features = [{} for _ in xrange(num_feat_types + 1)]

    
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

feat_amounts = dict(zip(range(1,num_feat_types + 1), [0]*num_feat_types))


def set_f0(p, c, p_pos, c_pos, n):
    pass


def set_f1(p, c, p_pos, c_pos, n): 
    if p not in features[1]:
        features[1][p] = {}
    features[1][p][p_pos] = n


def set_f2(p, c, p_pos, c_pos, n): 
    features[2][p] = n


def set_f3(p, c, p_pos, c_pos, n): 
    features[3][p_pos] = n


def set_f4(p, c, p_pos, c_pos, n): 
    if c not in features[4]:
        features[4][c] = {}
    features[4][c][c_pos] = n


def set_f5(p, c, p_pos, c_pos, n):
    features[5][c] = n


def set_f6(p, c, p_pos, c_pos, n): 
    features[6][c_pos] = n


def set_f7(p, c, p_pos, c_pos, n): 
    if p not in features[7]:
        features[7][p] = {}
    if c not in features[7][p]:
        features[7][p][c] = {}
    if p_pos not in features[7][p][c]:
        features[7][p][c][p_pos] = {}
    features[7][p][c][p_pos][c_pos] = n


def set_f8(p, c, p_pos, c_pos, n): 
    if c not in features[8]:
        features[8][c] = {}
    if p_pos not in features[8][c]:
        features[8][c][p_pos] = {}    
    features[8][c][p_pos][c_pos] = n


def set_f9(p, c, p_pos, c_pos, n): 
    if p not in features[9]:
        features[9][p] = {}
    if c not in features[9][p]:
        features[9][p][c] = {}
    features[9][p][c][c_pos] = n


def set_f10(p, c, p_pos, c_pos, n): 
    if p not in features[10]:
        features[10][p] = {}
    if p_pos not in features[10][p]:
        features[10][p][p_pos] = {}
    features[10][p][p_pos][c_pos] = n


def set_f11(p, c, p_pos, c_pos, n): 
    if p not in features[11]:
        features[11][p] = {}
    if c not in features[11][p]:
        features[11][p][c] = {}
    features[11][p][c][p_pos] = n


def set_f12(p, c, p_pos, c_pos, n): 
    if p not in features[12]:
        features[12][p] = {}
    features[12][p][c] = n


def set_f13(p, c, p_pos, c_pos, n): 
    if p_pos not in features[13]:
        features[13][p_pos] = {}
    features[13][p_pos][c_pos] = n
    
set_feat_ind = [set_f0, set_f1, set_f2, set_f3, set_f4, set_f5, set_f6, set_f7,
                set_f8, set_f9, set_f10, set_f11, set_f12, set_f13]


def set_features(parent_tup, child_tup):
    global num_features    
    p, p_pos = parent_tup
    c, c_pos = child_tup
    
    model_features = range(1, num_feat_types + 1)    
    if 'basic' in model:
        model_features = list(set(model_features) - set([7, 9, 11, 12]))

    edge_feats = []
    for ind in model_features:
        try:
            edge_feats.append(get_feat_ind(p, c, p_pos, c_pos))
        except KeyError:
            num_features += 1            
            feat_amounts[ind] += 1
            set_feat_ind[ind](p, c, p_pos, c_pos, num_features)
            edge_feats.append(num_features)

    return edge_feats
    

def get_feature_list(sentence, p_ind, c_ind):
    p, p_pos = sentence.get_word_pos(p_ind)
    c, c_pos = sentence.get_word_pos(c_ind)
    model_features = range(1, num_feat_types + 1)    

    if 'basic' in model:
        model_features = list(set(model_features) - set([7, 9, 11, 12]))
    
    return [get_feat_ind[i](p, c, p_pos, c_pos) for i in model_features]


def save_features(directory):
    pickle.dump(features, open(os.path.join(directory, "features"), 'wb'))


def load_features(directory):
    features.features = pickle.load(open(os.path.join(directory, "features"), 'rb'))
