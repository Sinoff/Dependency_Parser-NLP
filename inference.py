from features import get_feature_list
from edmonds import mst
import numpy as np


def inference(sentence, weights):
    weights_graph = {}
    # find best tree
    for p, parent in enumerate(sentence.words):
        for c, child in enumerate(sentence.words[1:], 1):
            if p != c:  # cannot have self edges
                if c == 1 or (p == 1 and c == 2):  # first edge added from this node
                    weights_graph[p] = {}
                weights_graph[p][c] = sum(weights[get_feature_list(sentence, p, c)])
    # call Edmonds - 0 is root
    mst(0, weights_graph)
    for p, parent in enumerate(weights_graph):
        for c, child in enumerate(weights_graph[p]):
            sentence.add_edge(p, c)
