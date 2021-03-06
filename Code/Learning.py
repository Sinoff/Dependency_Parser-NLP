from random import shuffle
from features import get_feature_list
import numpy as np
from edmonds import mst
import os


def learning_algorithm(iteration_num, sentences, feature_num, directory):
    """
    learning_algorithm:
    function for learning, using the Perceptron algorithm
    arguments: iteration_num = amount of desired iterations (epochs).
               sentences = list of Sentence objects, created from corpus.
               feature_num = total amount of features found in corpus.
    returns: weights = a numpy array representing the final weights calculated 
             by the Perceptron.
    """    
    weights = np.zeros(feature_num)  # initializing weights
    for iteration in range(1, iteration_num+1):
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
                    if p != c:  # cannot have self edges
                        feature_graph[p][c] = get_feature_list(sentence, p, c)
                        # calc weight of edge for weights_graph
                        weights_graph[p][c] = -np.sum(weights[feature_graph[p][c]])
            # call Edmonds - 0 is root
            weights_tree = mst(0, weights_graph)
            # Update weights:
            # First, add according to golden model
            weights[sentence.feat_inds.keys()] += sentence.feat_inds.values()  
            for parent in weights_tree.keys():
                for child in weights_tree[parent].keys():
                    # Then, reduce according to wrong prediction                    
                    weights[feature_graph[parent][child]] -= 1

        # save weights during running
        if iteration == 20:
            np.save(os.path.join(directory, "weights20"), weights)
            np.savetxt(os.path.join(directory, "weights20.txt"), weights)
        elif iteration == 50:
                np.save(os.path.join(directory, "weights50"), weights)
                np.savetxt(os.path.join(directory, "weights50.txt"), weights)
        elif iteration == 80:
            np.save(os.path.join(directory, "weights80"), weights)
            np.savetxt(os.path.join(directory, "weights80.txt"), weights)
        elif iteration == 100:
            np.save(os.path.join(directory, "weights100"), weights)
            np.savetxt(os.path.join(directory, "weights100.txt"), weights)
    return weights
