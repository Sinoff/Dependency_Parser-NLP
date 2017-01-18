from random import shuffle
from features import get_feature_list
from edmonds import mst
import numpy as np

def learning_algorithm(iteration_num, sentences, feature_num):
    weights = np.zeros(feature_num)  # initializing weights
    for iteration in range(iteration_num):
        feature_graph = {}
        weights_graph = {}
        for sentence in sentences.shuffle():
            # create complete graph
            for p , parent in enumerate(sentence.words):
                for c, child in enumerate(sentence.words[1:], 1):
                    if p != c: # cannot have self edges
                        if c == 1 or (p == 1 and c == 2): # first edge added from this node
                            feature_graph[p] = {}
                            weights_graph[p] = {}
                        feature_graph[p][c]= get_feature_list(sentence, p, c)
                        # calc weight of edge for weights_graph
                        weights_graph[p][c] = sum(weights[feature_graph[p][c]])
            # call Edmonds - 0 is root
            mst(0 , weights_graph)
            # update weights
            weights[sentence.feat_inds] += 1 # add according to golden model
            for p, parent in enumerate(weights_graph):
                for c,child in enumerate(weights_graph[p]):
                    weights[feature_graph[p][c]] -= 1
    return weights

