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

num_feat_types = 46
num_features = 0
# model = 'basic'
model_features = range(1, num_feat_types + 1)

def set_model_features(feat_file):
    global model_features
    global num_feat_types
    with open(feat_file, 'r') as ff:
        model_features = [int(x) for x in ff.read().split()]
    
    print("Feature types used: " + str(model_features))



features = [{} for _ in xrange(num_feat_types + 1)]

    
get_feat_ind = [
                # unigrams features
                lambda e: (e.p_word, e.c_word),
                lambda e: features[1][e.p_word][e.p_pos],
                lambda e: features[2][e.p_word],
                lambda e: features[3][e.p_pos],
                lambda e: features[4][e.c_word][e.c_pos],
                lambda e: features[5][e.c_word],
                lambda e: features[6][e.c_pos],
                # bigrams features
                lambda e: features[7][e.p_word][e.c_word][e.p_pos][e.c_pos],
                lambda e: features[8][e.c_word][e.p_pos][e.c_pos],
                lambda e: features[9][e.p_word][e.c_word][e.c_pos],
                lambda e: features[10][e.p_word][e.p_pos][e.c_pos],
                lambda e: features[11][e.p_word][e.c_word][e.p_pos],
                lambda e: features[12][e.p_word][e.c_word],
                lambda e: features[13][e.p_pos][e.c_pos],
                # index features - unigrams
                lambda e: features[14][e.p_word][e.p_ind],
                lambda e: features[15][e.p_pos][e.p_ind],
                lambda e: features[16][e.c_word][e.c_ind],
                lambda e: features[17][e.c_pos][e.c_ind],
                lambda e: features[18][e.p_word][e.p_pos][e.p_ind],
                lambda e: features[19][e.c_word][e.c_pos][e.c_ind],
                # index features - bigrams
                lambda e: features[20][e.p_pos][e.c_pos][e.p_ind],
                lambda e: features[21][e.p_pos][e.c_pos][e.c_ind],
                lambda e: features[22][e.p_pos][e.c_pos][e.p_ind][e.c_ind],
                # distance features
                lambda e: features[23][e.p_word][e.c_word][e.dist],
                lambda e: features[24][e.p_pos][e.c_pos][e.dist],
                lambda e: features[25][e.p_word][e.p_pos][e.c_pos][e.dist],
                lambda e: features[26][e.c_word][e.p_pos][e.c_pos][e.dist],
                # features with sentence length
                lambda e: features[27][e.p_word][e.c_word][e.dist][e.sen_len],
                lambda e: features[28][e.p_pos][e.c_pos][e.dist][e.sen_len],
                lambda e: features[29][e.p_word][e.p_pos][e.dist][e.sen_len],
                lambda e: features[30][e.c_word][e.c_pos][e.dist][e.sen_len],
                lambda e: features[31][e.p_word][e.p_pos][e.c_pos][e.dist][e.sen_len],
                lambda e: features[32][e.c_word][e.p_pos][e.c_pos][e.dist][e.sen_len],
                lambda e: features[33][e.p_ind][e.c_ind][e.sen_len],
                lambda e: features[34][e.p_pos][e.p_ind][e.c_ind][e.sen_len],
                lambda e: features[35][e.c_pos][e.p_ind][e.c_ind][e.sen_len],
                # surroundings features
                lambda e: features[36][e.p_pos][e.c_pos][e.p_next_pos][e.c_next_pos],
                lambda e: features[37][e.p_pos][e.c_pos][e.p_next_pos][e.c_pre_pos],
                lambda e: features[38][e.p_pos][e.c_pos][e.p_pre_pos][e.c_next_pos],
                lambda e: features[39][e.p_pos][e.c_pos][e.p_pre_pos][e.c_pre_pos],
                lambda e: features[40][e.p_pos][e.c_pos][e.p_next_pos][e.c_next_pos][e.dist],
                lambda e: features[41][e.p_pos][e.c_pos][e.p_next_pos][e.c_pre_pos][e.dist],
                lambda e: features[42][e.p_pos][e.c_pos][e.p_pre_pos][e.c_next_pos][e.dist],
                lambda e: features[43][e.p_pos][e.c_pos][e.p_pre_pos][e.c_pre_pos][e.dist],
                # amount of brothers features
                lambda e: features[44][e.p_pos][e.c_pos][len(e.p_out_edges)][e.dist][e.sen_len],
                lambda e: features[45][e.p_pos][e.c_pos][len(e.p_out_edges)],
                lambda e: features[46][e.p_pos][e.c_pos][len(e.p_out_edges)][e.dist]
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


def set_f14(e, n):
    if e.p_word not in features[14]:
        features[14][e.p_word] = {}
    features[14][e.p_word][e.p_ind] = n


def set_f15(e, n):
    if e.p_pos not in features[15]:
        features[15][e.p_pos] = {}
    features[15][e.p_pos][e.p_ind] = n


def set_f16(e, n):
    if e.c_word not in features[16]:
        features[16][e.c_word] = {}
    features[16][e.c_word][e.c_ind] = n


def set_f17(e, n):
    if e.c_pos not in features[17]:
        features[17][e.c_pos] = {}
    features[17][e.c_pos][e.c_ind] = n


def set_f18(e, n):
    if e.p_word not in features[18]:
        features[18][e.p_word] = {}
    if e.p_pos not in features[18][e.p_word]:
        features[18][e.p_word][e.p_pos] = {}
    features[18][e.p_word][e.p_pos][e.p_ind] = n


def set_f19(e, n):
    if e.c_word not in features[19]:
        features[19][e.c_word] = {}
    if e.c_pos not in features[19][e.c_word]:
        features[19][e.c_word][e.c_pos] = {}
    features[19][e.c_word][e.c_pos][e.c_ind] = n


def set_f20(e, n):
    if e.p_pos not in features[20]:
        features[20][e.p_pos] = {}
    if e.c_pos not in features[20][e.p_pos]:
        features[20][e.p_pos][e.c_pos] = {}
    features[20][e.p_pos][e.c_pos][e.p_ind] = n


def set_f21(e, n):
    if e.p_pos not in features[21]:
        features[21][e.p_pos] = {}
    if e.c_pos not in features[21][e.p_pos]:
        features[21][e.p_pos][e.c_pos] = {}
    features[21][e.p_pos][e.c_pos][e.c_ind] = n


def set_f22(e, n):
    if e.p_pos not in features[22]:
        features[22][e.p_pos] = {}
    if e.c_pos not in features[22][e.p_pos]:
        features[22][e.p_pos][e.c_pos] = {}
    if e.p_ind not in features[22][e.p_pos][e.c_pos]:
        features[22][e.p_pos][e.c_pos][e.p_ind] = {}
    features[22][e.p_pos][e.c_pos][e.p_ind][e.c_ind] = n


def set_f23(e, n):
    if e.p_word not in features[23]:
        features[23][e.p_word] = {}
    if e.c_word not in features[23][e.p_word]:
        features[23][e.p_word][e.c_word] = {}
    features[23][e.p_word][e.c_word][e.dist] = n


def set_f24(e, n):
    if e.p_pos not in features[24]:
        features[24][e.p_pos] = {}
    if e.c_pos not in features[24][e.p_pos]:
        features[24][e.p_pos][e.c_pos] = {}
    features[24][e.p_pos][e.c_pos][e.dist] = n


def set_f25(e, n):
    if e.p_word not in features[25]:
        features[25][e.p_word] = {}
    if e.p_pos not in features[25][e.p_word]:
        features[25][e.p_word][e.p_pos] = {}
    if e.c_pos not in features[25][e.p_word][e.p_pos]:
        features[25][e.p_word][e.p_pos][e.c_pos] = {}
    features[25][e.p_word][e.p_pos][e.c_pos][e.dist] = n


def set_f26(e, n):
    if e.c_word not in features[26]:
        features[26][e.c_word] = {}
    if e.p_pos not in features[26][e.c_word]:
        features[26][e.c_word][e.p_pos] = {}
    if e.c_pos not in features[26][e.c_word][e.p_pos]:
        features[26][e.c_word][e.p_pos][e.c_pos] = {}
    features[26][e.c_word][e.p_pos][e.c_pos][e.dist] = n


def set_f27(e, n):
    if e.p_word not in features[27]:
        features[27][e.p_word] = {}
    if e.c_word not in features[27][e.p_word]:
        features[27][e.p_word][e.c_word] = {}
    if e.dist not in features[27][e.p_word][e.c_word]:
        features[27][e.p_word][e.c_word][e.dist] = {}
    features[27][e.p_word][e.c_word][e.dist][e.sen_len] = n


def set_f28(e, n):
    if e.p_pos not in features[28]:
        features[28][e.p_pos] = {}
    if e.c_pos not in features[28][e.p_pos]:
        features[28][e.p_pos][e.c_pos] = {}
    if e.dist not in features[28][e.p_pos][e.c_pos]:
        features[28][e.p_pos][e.c_pos][e.dist] = {}
    features[28][e.p_pos][e.c_pos][e.dist][e.sen_len] = n


def set_f29(e, n):
    if e.p_word not in features[29]:
        features[29][e.p_word] = {}
    if e.p_pos not in features[29][e.p_word]:
        features[29][e.p_word][e.p_pos] = {}
    if e.dist not in features[29][e.p_word][e.p_pos]:
        features[29][e.p_word][e.p_pos][e.dist] = {}
    features[29][e.p_word][e.p_pos][e.dist][e.sen_len] = n


def set_f30(e, n):
    if e.c_word not in features[30]:
        features[30][e.c_word] = {}
    if e.c_pos not in features[30][e.c_word]:
        features[30][e.c_word][e.c_pos] = {}
    if e.dist not in features[30][e.c_word][e.c_pos]:
        features[30][e.c_word][e.c_pos][e.dist] = {}
    features[30][e.c_word][e.c_pos][e.dist][e.sen_len] = n


def set_f31(e, n):
    if e.p_word not in features[31]:
        features[31][e.p_word] = {}
    if e.p_pos not in features[31][e.p_word]:
        features[31][e.p_word][e.p_pos] = {}
    if e.c_pos not in features[31][e.p_word][e.p_pos]:
        features[31][e.p_word][e.p_pos][e.c_pos] = {}
    if e.dist not in features[31][e.p_word][e.p_pos][e.c_pos]:
        features[31][e.p_word][e.p_pos][e.c_pos][e.dist] = {}
    features[31][e.p_word][e.p_pos][e.c_pos][e.dist][e.sen_len] = n


def set_f32(e, n):
    if e.c_word not in features[32]:
        features[32][e.c_word] = {}
    if e.p_pos not in features[32][e.c_word]:
        features[32][e.c_word][e.p_pos] = {}
    if e.c_pos not in features[32][e.c_word][e.p_pos]:
        features[32][e.c_word][e.p_pos][e.c_pos] = {}
    if e.dist not in features[32][e.c_word][e.p_pos][e.c_pos]:
        features[32][e.c_word][e.p_pos][e.c_pos][e.dist] = {}
    features[32][e.c_word][e.p_pos][e.c_pos][e.dist][e.sen_len] = n


def set_f33(e, n):
    if e.p_ind not in features[33]:
        features[33][e.p_ind] = {}
    if e.c_ind not in features[33][e.p_ind]:
        features[33][e.p_ind][e.c_ind] = {}
    features[33][e.p_ind][e.c_ind][e.sen_len] = n


def set_f34(e, n):
    if e.p_pos not in features[34]:
        features[34][e.p_pos] = {}
    if e.p_ind not in features[34][e.p_pos]:
        features[34][e.p_pos][e.p_ind] = {}
    if e.c_ind not in features[34][e.p_pos][e.p_ind]:
        features[34][e.p_pos][e.p_ind][e.c_ind] = {}
    features[34][e.p_pos][e.p_ind][e.c_ind][e.sen_len] = n


def set_f35(e, n):
    if e.c_pos not in features[35]:
        features[35][e.c_pos] = {}
    if e.p_ind not in features[35][e.c_pos]:
        features[35][e.c_pos][e.p_ind] = {}
    if e.c_ind not in features[35][e.c_pos][e.p_ind]:
        features[35][e.c_pos][e.p_ind][e.c_ind] = {}
    features[35][e.c_pos][e.p_ind][e.c_ind][e.sen_len] = n


def set_f36(e, n):
    global num_features
    if e.p_next_pos == "NONE" or e.c_next_pos == "NONE":
        num_features -= 1
        feat_amounts[36] -= 1
        return

    if e.p_pos not in features[36]:
        features[36][e.p_pos] = {}
    if e.c_pos not in features[36][e.p_pos]:
        features[36][e.p_pos][e.c_pos] = {}
    if e.p_next_pos not in features[36][e.p_pos][e.c_pos]:
        features[36][e.p_pos][e.c_pos][e.p_next_pos] = {}
    features[36][e.p_pos][e.c_pos][e.p_next_pos][e.c_next_pos] = n


def set_f37(e, n):
    global num_features
    if e.p_next_pos == "NONE" or e.c_pre_pos == "NONE":
        num_features -= 1
        feat_amounts[37] -= 1
        return

    if e.p_pos not in features[37]:
        features[37][e.p_pos] = {}
    if e.c_pos not in features[37][e.p_pos]:
        features[37][e.p_pos][e.c_pos] = {}
    if e.p_next_pos not in features[37][e.p_pos][e.c_pos]:
        features[37][e.p_pos][e.c_pos][e.p_next_pos] = {}
    features[37][e.p_pos][e.c_pos][e.p_next_pos][e.c_pre_pos] = n


def set_f38(e, n):
    global num_features
    if e.p_pre_pos == "NONE" or e.c_next_pos == "NONE":
        num_features -= 1
        feat_amounts[38] -= 1
        return

    if e.p_pos not in features[38]:
        features[38][e.p_pos] = {}
    if e.c_pos not in features[38][e.p_pos]:
        features[38][e.p_pos][e.c_pos] = {}
    if e.p_pre_pos not in features[38][e.p_pos][e.c_pos]:
        features[38][e.p_pos][e.c_pos][e.p_pre_pos] = {}
    features[38][e.p_pos][e.c_pos][e.p_pre_pos][e.c_next_pos] = n


def set_f39(e, n):
    global num_features
    if e.p_pre_pos == "NONE" or e.c_pre_pos == "NONE":
        num_features -= 1
        feat_amounts[39] -= 1
        return

    if e.p_pos not in features[39]:
        features[39][e.p_pos] = {}
    if e.c_pos not in features[39][e.p_pos]:
        features[39][e.p_pos][e.c_pos] = {}
    if e.p_pre_pos not in features[39][e.p_pos][e.c_pos]:
        features[39][e.p_pos][e.c_pos][e.p_pre_pos] = {}
    features[39][e.p_pos][e.c_pos][e.p_pre_pos][e.c_pre_pos] = n


def set_f40(e, n):
    global num_features
    if e.p_next_pos == "NONE" or e.c_next_pos == "NONE":
        num_features -= 1
        feat_amounts[40] -= 1
        return

    if e.p_pos not in features[40]:
        features[40][e.p_pos] = {}
    if e.c_pos not in features[40][e.p_pos]:
        features[40][e.p_pos][e.c_pos] = {}
    if e.p_next_pos not in features[40][e.p_pos][e.c_pos]:
        features[40][e.p_pos][e.c_pos][e.p_next_pos] = {}
    if e.c_next_pos not in features[40][e.p_pos][e.c_pos][e.p_next_pos]:
        features[40][e.p_pos][e.c_pos][e.p_next_pos][e.c_next_pos] = {}
    features[40][e.p_pos][e.c_pos][e.p_next_pos][e.c_next_pos][e.dist] = n


def set_f41(e, n):
    global num_features
    if e.p_next_pos == "NONE" or e.c_pre_pos == "NONE":
        num_features -= 1
        feat_amounts[41] -= 1
        return

    if e.p_pos not in features[41]:
        features[41][e.p_pos] = {}
    if e.c_pos not in features[41][e.p_pos]:
        features[41][e.p_pos][e.c_pos] = {}
    if e.p_next_pos not in features[41][e.p_pos][e.c_pos]:
        features[41][e.p_pos][e.c_pos][e.p_next_pos] = {}
    if e.c_pre_pos not in features[41][e.p_pos][e.c_pos][e.p_next_pos]:
        features[41][e.p_pos][e.c_pos][e.p_next_pos][e.c_pre_pos] = {}
    features[41][e.p_pos][e.c_pos][e.p_next_pos][e.c_pre_pos][e.dist] = n


def set_f42(e, n):
    global num_features
    if e.p_pre_pos == "NONE" or e.c_next_pos == "NONE":
        num_features -= 1
        feat_amounts[42] -= 1
        return

    if e.p_pos not in features[42]:
        features[42][e.p_pos] = {}
    if e.c_pos not in features[42][e.p_pos]:
        features[42][e.p_pos][e.c_pos] = {}
    if e.p_pre_pos not in features[42][e.p_pos][e.c_pos]:
        features[42][e.p_pos][e.c_pos][e.p_pre_pos] = {}
    if e.c_next_pos not in features[42][e.p_pos][e.c_pos][e.p_pre_pos]:
        features[42][e.p_pos][e.c_pos][e.p_pre_pos][e.c_next_pos] = {}
    features[42][e.p_pos][e.c_pos][e.p_pre_pos][e.c_next_pos][e.dist] = n


def set_f43(e, n):
    global num_features
    if e.p_pre_pos == "NONE" or e.c_pre_pos == "NONE":
        num_features -= 1
        feat_amounts[43] -= 1
        return

    if e.p_pos not in features[43]:
        features[43][e.p_pos] = {}
    if e.c_pos not in features[43][e.p_pos]:
        features[43][e.p_pos][e.c_pos] = {}
    if e.p_pre_pos not in features[43][e.p_pos][e.c_pos]:
        features[43][e.p_pos][e.c_pos][e.p_pre_pos] = {}
    if e.c_pre_pos not in features[43][e.p_pos][e.c_pos][e.p_pre_pos]:
        features[43][e.p_pos][e.c_pos][e.p_pre_pos][e.c_pre_pos] = {}
    features[43][e.p_pos][e.c_pos][e.p_pre_pos][e.c_pre_pos][e.dist] = n


def set_f44(e, n):
    if e.p_pos not in features[44]:
        features[44][e.p_pos] = {}
    if e.c_pos not in features[44][e.p_pos]:
        features[44][e.p_pos][e.c_pos] = {}
    if len(e.p_out_edges) not in features[44][e.p_pos][e.c_pos]:
        features[44][e.p_pos][e.c_pos][len(e.p_out_edges)] = {}
    if e.dist not in features[44][e.p_pos][e.c_pos][len(e.p_out_edges)]:
        features[44][e.p_pos][e.c_pos][len(e.p_out_edges)][e.dist] = {}
    features[44][e.p_pos][e.c_pos][len(e.p_out_edges)][e.dist][e.sen_len] = n


def set_f45(e, n):
    if e.p_pos not in features[45]:
        features[45][e.p_pos] = {}
    if e.c_pos not in features[45][e.p_pos]:
        features[45][e.p_pos][e.c_pos] = {}
    features[45][e.p_pos][e.c_pos][len(e.p_out_edges)] = n


def set_f46(e, n):
    global num_features
    if e.p_ind != 0:
        num_features -= 1
        feat_amounts[46] -= 1
        return

    if e.p_pos not in features[46]:
        features[46][e.p_pos] = {}
    if e.c_pos not in features[46][e.p_pos]:
        features[46][e.p_pos][e.c_pos] = {}
    if len(e.p_out_edges) not in features[46][e.p_pos][e.c_pos]:
        features[46][e.p_pos][e.c_pos][len(e.p_out_edges)] = {}
    features[46][e.p_pos][e.c_pos][len(e.p_out_edges)][e.dist] = n


set_feat_ind = [set_f0, set_f1, set_f2, set_f3, set_f4, set_f5, set_f6, set_f7,
                set_f8, set_f9, set_f10, set_f11, set_f12, set_f13, set_f14,
                set_f15, set_f16, set_f17, set_f18, set_f19, set_f20, set_f21,
                set_f22, set_f23, set_f24, set_f25, set_f26, set_f27, set_f28,
                set_f29, set_f30, set_f31, set_f32, set_f33, set_f34, set_f35,
                set_f36, set_f37, set_f38, set_f39, set_f40, set_f41, set_f42,
                set_f43, set_f44, set_f45, set_f46]


def set_features(e_data):
    global num_features
    global model_features
    
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
    global model_features
    
    try:
        e_data = sentence.edge_data[p_ind][c_ind]
    except KeyError:
        e_data = EdgeData(sentence, p_ind, c_ind)
    model_features = range(1, num_feat_types + 1)    

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
