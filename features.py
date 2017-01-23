# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 22:30:07 2017

@author: okrupnik
"""

import pickle
import os
from classes import EdgeData

"""
FEATURES module: 
extracts fetaures from words, parse corpus, save feature tables
"""

num_feat_types = 13
num_features = 0
model = 'basic'

features = [{} for _ in xrange(num_feat_types + 1)]

    
get_feat_ind = [lambda e: (e.p_word, e.c_word), 
                lambda e: features[1][e.p_word][e.p_pos],
                lambda e: features[2][e.p_word],
                lambda e: features[3][e.p_pos],
                lambda e: features[4][e.c_word][e.c_pos],
                lambda e: features[5][e.c_word],
                lambda e: features[6][e.c_pos],
                lambda e: features[7][e.p_word][e.c_word][e.p_pos][e.c_pos],
                lambda e: features[8][e.c_word][e.p_pos][e.c_pos],
                lambda e: features[9][e.p_word][e.c_word][e.c_pos],
                lambda e: features[10][e.p_word][e.p_pos][e.c_pos],
                lambda e: features[11][e.p_word][e.c_word][e.p_pos],
                lambda e: features[12][e.p_word][e.c_word],
                lambda e: features[13][e.p_pos][e.c_pos]
                ]

feat_amounts = dict(zip(range(1,num_feat_types + 1), [0]*num_feat_types))


def set_f0(e, n):
    pass


def set_f1(e, n): 
    if e.p_word not in features[1]:
        features[1][e.p_word] = {}
    features[1][e.p_word][e.p_pos] = n


def set_f2(e, n): 
    features[2][e.p_word] = n


def set_f3(e, n): 
    features[3][e.p_pos] = n


def set_f4(e, n): 
    if e.c_word not in features[4]:
        features[4][e.c_word] = {}
    features[4][e.c_word][e.c_pos] = n


def set_f5(e, n):
    features[5][e.c_word] = n


def set_f6(e, n): 
    features[6][e.c_pos] = n


def set_f7(e, n): 
    if e.p_word not in features[7]:
        features[7][e.p_word] = {}
    if e.c_word not in features[7][e.p_word]:
        features[7][e.p_word][e.c_word] = {}
    if e.p_pos not in features[7][e.p_word][e.c_word]:
        features[7][e.p_word][e.c_word][e.p_pos] = {}
    features[7][e.p_word][e.c_word][e.p_pos][e.c_pos] = n


def set_f8(e, n): 
    if e.c_word not in features[8]:
        features[8][e.c_word] = {}
    if e.p_pos not in features[8][e.c_word]:
        features[8][e.c_word][e.p_pos] = {}    
    features[8][e.c_word][e.p_pos][e.c_pos] = n


def set_f9(e, n): 
    if e.p_word not in features[9]:
        features[9][e.p_word] = {}
    if e.c_word not in features[9][e.p_word]:
        features[9][e.p_word][e.c_word] = {}
    features[9][e.p_word][e.c_word][e.c_pos] = n


def set_f10(e, n): 
    if e.p_word not in features[10]:
        features[10][e.p_word] = {}
    if e.p_pos not in features[10][e.p_word]:
        features[10][e.p_word][e.p_pos] = {}
    features[10][e.p_word][e.p_pos][e.c_pos] = n


def set_f11(e, n): 
    if e.p_word not in features[11]:
        features[11][e.p_word] = {}
    if e.c_word not in features[11][e.p_word]:
        features[11][e.p_word][e.c_word] = {}
    features[11][e.p_word][e.c_word][e.p_pos] = n


def set_f12(e, n): 
    if e.p_word not in features[12]:
        features[12][e.p_word] = {}
    features[12][e.p_word][e.c_word] = n


def set_f13(e, n): 
    if e.p_pos not in features[13]:
        features[13][e.p_pos] = {}
    features[13][e.p_pos][e.c_pos] = n
    
set_feat_ind = [set_f0, set_f1, set_f2, set_f3, set_f4, set_f5, set_f6, set_f7,
                set_f8, set_f9, set_f10, set_f11, set_f12, set_f13]


def set_features(e_data):
    global num_features
    
    model_features = range(1, num_feat_types + 1)    
    if 'basic' in model:
        model_features = list(set(model_features) - set([7, 9, 11, 12]))

    edge_feats = []
    for ind in model_features:
        try:
            edge_feats.append(get_feat_ind[ind](e_data))
        except KeyError:            
            feat_amounts[ind] += 1
            set_feat_ind[ind](e_data, num_features)
            edge_feats.append(num_features)
            num_features += 1

    return edge_feats
    

def get_feature_list(sentence, p_ind, c_ind):
    try:
        e_data = sentence.edge_data[p_ind][c_ind]
    except KeyError:
        e_data = EdgeData(sentence, p_ind, c_ind)
    model_features = range(1, num_feat_types + 1)    

    if 'basic' in model:
        model_features = list(set(model_features) - set([7, 9, 11, 12]))
    
    feat_inds = []
    for i in model_features:
        try:
            feat_inds.append(get_feat_ind[i](e_data))
        except KeyError:
            # Feature never seen in corpus
            pass
    
    return feat_inds


def save_features(directory):
    f = open(os.path.join(directory, "features.dmp"), 'wb')
    pickle.dump(features, f)
    f.close()
