from random import shuffle
from features import get_feature_list
import numpy as np
from edmonds import mst
import time

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
        shuffle(sentences)
        for sentence in sentences:           
            feature_graph = {}
            weights_graph = {}
            # create complete graph
            for p, parent in enumerate(sentence.words):
                feature_graph[p] = {}
                weights_graph[p] = {}
                for c, child in enumerate(sentence.words[1:], 1):
                    # print("parent={}, child={}".format(parent, child)) # todo: delete
                    if p != c:  # cannot have self edges
                        feature_graph[p][c] = get_feature_list(sentence, p, c)
                        # calc weight of edge for weights_graph
                        # print (get_feature_list(sentence, p, c)) # todo: delete
                        # print (weights[feature_graph[p][c]]) # todo: delete
                        # print np.sum(weights[feature_graph[p][c]]) # todo: delete

                        weights_graph[p][c] = -np.sum(weights[feature_graph[p][c]])
            # call Edmonds - 0 is root
            weights_tree = mst(0, weights_graph)
            print(weights_tree) # todo: delete
            # update weights
            weights[sentence.feat_inds] += 1  # add according to golden model
            np.savetxt("weights_before.txt", weights) # todo: delete
            for parent in weights_tree.keys():
                for child in weights_tree[parent].keys():
                    print("parent={}, child={}".format(parent, child))
                    weights[feature_graph[parent][child]] -= 1
                    print (feature_graph[parent][child]) # todo: delete
                    np.savetxt("weights.txt", weights) # todo: delete
                    time.sleep(5)  # todo: delete
    return weights
