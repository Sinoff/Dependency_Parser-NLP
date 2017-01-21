from random import shuffle
from features import get_feature_list
from edmonds import mst
import numpy as np

"""
    learning_algorithm:
    function for learning, using the Perceptron algorithm
    arguments:
            iteration_num = amount of desired iterations (epochs).
            sentences = list of Sentence objects, created from corpus.
            feature_num = total amount of features found in corpus.
    returns:
            weights = a numpy array representing the final weights calculated by the Perceptron.
"""


def learning_algorithm(iteration_num, sentences, feature_num):
    weights = np.zeros(feature_num)  # initializing weights
    for iteration in range(iteration_num):
        print("Starting iteration {}...".format(iteration))        
        feature_graph = {}
        weights_graph = {}
        shuffle(sentences)
        for sentence in sentences:
            # create complete graph
            for p, parent in enumerate(sentence.words[1:], 1):
                feature_graph[p] = {}
                weights_graph[p] = {}
                for c, child in enumerate(sentence.words[1:], 1):
                    if p != c:  # cannot have self edges
                        feature_graph[p][c] = get_feature_list(sentence, p, c)
                        # calc weight of edge for weights_graph
                        weights_graph[p][c] = -np.sum(weights[feature_graph[p][c]])
            # add root to all others
            print(weights_graph)
            weights_graph[0] = {}
            for c, child in enumerate(sentence.words[1:], 1):
                weights_graph[0][c] = 100000000
            # call Edmonds - 0 is root
            weights_tree = mst(0, weights_graph)
            # print(weights_tree)
            # update weights
            weights[sentence.feat_inds] += 1  # add according to golden model
            for parent in weights_tree.keys()[1:]:
                for child in weights_tree[parent].keys()[1:]:
                    if parent == child:
                        continue
                    weights[feature_graph[parent][child]] -= 1
    return weights
